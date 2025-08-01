"""
Sistema de Detecção de Botões Azuis
Módulo responsável pela detecção visual de botões azuis na tela
"""

import os
import time
from typing import Optional, Tuple, List, Dict, Any

import cv2
import numpy as np
import pyautogui
from PIL import Image

try:
    from .config import COLOR_DETECTION, BUTTON_DETECTION, DEBUG_CONFIG
except ImportError:
    from config import COLOR_DETECTION, BUTTON_DETECTION, DEBUG_CONFIG


class BlueButtonDetector:
    """
    Detector inteligente de botões azuis na tela
    
    Utiliza análise de cor HSV e filtros de forma para identificar
    botões azuis típicos de interfaces "Continue"
    """
    
    def __init__(self, debug_mode: bool = False):
        """
        Inicializa o detector
        
        Args:
            debug_mode: Se True, salva imagens de debug
        """
        self.debug_mode = debug_mode
        self.detection_count = 0
        self.successful_detections = 0
        
        # Criar diretório de debug se necessário
        if self.debug_mode:
            self._setup_debug_directory()
    
    def _setup_debug_directory(self) -> None:
        """Cria o diretório para salvar imagens de debug"""
        debug_dir = DEBUG_CONFIG['debug_dir']
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
            print(f"Diretório de debug criado: {debug_dir}")
    
    def detect_button(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Detecta botão azul na tela
        
        Returns:
            Tupla (center_x, center_y, width, height) se encontrado, None caso contrário
        """
        try:
            self.detection_count += 1
            
            # Capturar screenshot
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Encontrar candidatos a botão
            candidates = self._find_button_candidates(img)
            
            # Criar imagem de debug se necessário
            debug_img = img.copy() if self.debug_mode else None
            
            # Processar candidatos
            valid_candidates = self._process_candidates(candidates, img, debug_img)
            
            # Retornar melhor candidato
            if valid_candidates:
                best_candidate = max(valid_candidates, key=lambda c: c['score'])
                self.successful_detections += 1
                
                # Salvar debug image com resultado
                if debug_img is not None:
                    self._save_debug_image(debug_img, best_candidate, "detection")
                
                center_x, center_y = best_candidate['center']
                x, y, w, h = best_candidate['bounds']
                return (center_x, center_y, w, h)
            
            # Salvar debug image mesmo sem detecção
            if debug_img is not None:
                self._save_debug_image(debug_img, None, "no_detection")
            
            return None
            
        except Exception as e:
            print(f"Erro na detecção: {e}")
            return None
    
    def _find_button_candidates(self, img: np.ndarray) -> List[np.ndarray]:
        """
        Encontra contornos que podem ser botões azuis
        
        Args:
            img: Imagem BGR da tela
            
        Returns:
            Lista de contornos candidatos
        """
        # Converter para HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Criar máscaras para diferentes tons de azul
        masks = []
        for blue_range in COLOR_DETECTION['blue_ranges']:
            mask = cv2.inRange(hsv, blue_range['lower'], blue_range['upper'])
            masks.append(mask)
        
        # Combinar todas as máscaras
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask = cv2.bitwise_or(combined_mask, mask)
        
        # Remover ruído com operações morfológicas
        kernel = np.ones(COLOR_DETECTION['morphology_kernel_size'], np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(
            combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        return contours
    
    def _process_candidates(self, contours: List[np.ndarray], img: np.ndarray, 
                          debug_img: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
        """
        Processa contornos para encontrar botões válidos
        
        Args:
            contours: Lista de contornos encontrados
            img: Imagem original
            debug_img: Imagem para debug (opcional)
            
        Returns:
            Lista de candidatos válidos com seus scores
        """
        valid_candidates = []
        
        for contour in contours:
            # Calcular propriedades básicas
            area = cv2.contourArea(contour)
            
            # Filtro inicial por área
            if not (BUTTON_DETECTION['min_area'] < area < BUTTON_DETECTION['max_area']):
                continue
            
            # Obter retângulo delimitador
            x, y, w, h = cv2.boundingRect(contour)
            
            # Aplicar filtros de dimensão e forma
            if not self._is_valid_button_shape(x, y, w, h, img.shape):
                continue
            
            # Verificar se a região realmente contém um botão azul
            blue_ratio = self._calculate_blue_ratio(img, x, y, w, h)
            if blue_ratio < COLOR_DETECTION['min_blue_ratio']:
                continue
            
            # Calcular score do candidato
            score = self._calculate_candidate_score(x, y, w, h, blue_ratio, img.shape)
            
            # Criar candidato válido
            candidate = {
                'center': (x + w // 2, y + h // 2),
                'bounds': (x, y, w, h),
                'score': score,
                'blue_ratio': blue_ratio,
                'area': area
            }
            
            valid_candidates.append(candidate)
            
            # Desenhar debug se necessário
            if debug_img is not None:
                self._draw_debug_candidate(debug_img, candidate, len(valid_candidates))
        
        return valid_candidates
    
    def _is_valid_button_shape(self, x: int, y: int, w: int, h: int, 
                              img_shape: Tuple[int, int, int]) -> bool:
        """
        Verifica se as dimensões correspondem a um botão válido
        
        Args:
            x, y, w, h: Coordenadas e dimensões do retângulo
            img_shape: Forma da imagem (height, width, channels)
            
        Returns:
            True se as dimensões são válidas para um botão
        """
        img_height, img_width = img_shape[:2]
        
        # Verificar dimensões
        if not (BUTTON_DETECTION['min_width'] <= w <= BUTTON_DETECTION['max_width']):
            return False
        
        if not (BUTTON_DETECTION['min_height'] <= h <= BUTTON_DETECTION['max_height']):
            return False
        
        # Verificar proporção (aspect ratio)
        aspect_ratio = w / h if h > 0 else 0
        if not (BUTTON_DETECTION['min_aspect_ratio'] <= aspect_ratio <= BUTTON_DETECTION['max_aspect_ratio']):
            return False
        
        # Verificar posição (não muito próximo das bordas)
        margin = BUTTON_DETECTION['edge_margin']
        if x < margin or y < margin:
            return False
        
        if (x + w) > (img_width - margin) or (y + h) > (img_height - margin):
            return False
        
        return True
    
    def _calculate_blue_ratio(self, img: np.ndarray, x: int, y: int, w: int, h: int) -> float:
        """
        Calcula a proporção de pixels azuis na região do botão
        
        Args:
            img: Imagem BGR
            x, y, w, h: Coordenadas e dimensões da região
            
        Returns:
            Proporção de pixels azuis (0.0 a 1.0)
        """
        # Extrair região do botão
        button_region = img[y:y + h, x:x + w]
        
        # Converter para HSV
        button_hsv = cv2.cvtColor(button_region, cv2.COLOR_BGR2HSV)
        
        # Criar máscaras para tons de azul
        blue_pixels = np.zeros((h, w), dtype=np.uint8)
        
        for blue_range in COLOR_DETECTION['blue_ranges']:
            mask = cv2.inRange(button_hsv, blue_range['lower'], blue_range['upper'])
            blue_pixels = cv2.bitwise_or(blue_pixels, mask)
        
        # Calcular proporção
        total_pixels = w * h
        blue_pixel_count = np.sum(blue_pixels > 0)
        
        return blue_pixel_count / total_pixels if total_pixels > 0 else 0.0
    
    def _calculate_candidate_score(self, x: int, y: int, w: int, h: int, 
                                 blue_ratio: float, img_shape: Tuple[int, int, int]) -> float:
        """
        Calcula score do candidato baseado em múltiplos fatores
        
        Args:
            x, y, w, h: Coordenadas e dimensões
            blue_ratio: Proporção de pixels azuis
            img_shape: Forma da imagem
            
        Returns:
            Score do candidato (0.0 a 1.0)
        """
        img_height = img_shape[0]
        weights = BUTTON_DETECTION['score_weights']
        
        # Score baseado na proporção de azul
        blue_score = blue_ratio
        
        # Score baseado na posição (preferir parte inferior da tela)
        position_score = y / img_height
        
        # Score baseado no tamanho (normalizado)
        size_score = min((w * h) / 5000, 1.0)
        
        # Score total ponderado
        total_score = (
            blue_score * weights['blue_ratio'] +
            position_score * weights['position'] +
            size_score * weights['size']
        )
        
        return total_score
    
    def _draw_debug_candidate(self, debug_img: np.ndarray, candidate: Dict[str, Any], 
                            candidate_num: int) -> None:
        """
        Desenha informações de debug para um candidato
        
        Args:
            debug_img: Imagem de debug
            candidate: Dados do candidato
            candidate_num: Número do candidato
        """
        x, y, w, h = candidate['bounds']
        score = candidate['score']
        
        # Cor baseada no número do candidato
        color = (0, 255, 0) if candidate_num == 1 else (0, 255, 255)
        
        # Desenhar retângulo
        cv2.rectangle(debug_img, (x, y), (x + w, y + h), color, 2)
        
        # Adicionar texto com score
        text = f"Score: {score:.2f}"
        cv2.putText(debug_img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    def _save_debug_image(self, debug_img: np.ndarray, best_candidate: Optional[Dict[str, Any]], 
                         prefix: str) -> None:
        """
        Salva imagem de debug com timestamp
        
        Args:
            debug_img: Imagem de debug
            best_candidate: Melhor candidato encontrado (se houver)
            prefix: Prefixo do nome do arquivo
        """
        # Destacar o candidato selecionado
        if best_candidate:
            x, y, w, h = best_candidate['bounds']
            cv2.rectangle(debug_img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.putText(debug_img, "SELECTED", (x, y - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Salvar arquivo
        timestamp = time.strftime(DEBUG_CONFIG['timestamp_format'])
        filename = f"{prefix}_{timestamp}{DEBUG_CONFIG['image_format']}"
        filepath = os.path.join(DEBUG_CONFIG['debug_dir'], filename)
        
        cv2.imwrite(filepath, debug_img)
        print(f"Debug image saved: {filepath}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do detector
        
        Returns:
            Dicionário com estatísticas de detecção
        """
        success_rate = (self.successful_detections / self.detection_count * 100 
                       if self.detection_count > 0 else 0)
        
        return {
            'total_detections': self.detection_count,
            'successful_detections': self.successful_detections,
            'success_rate': success_rate,
            'debug_mode': self.debug_mode
        }
    
    def reset_statistics(self) -> None:
        """Reseta as estatísticas do detector"""
        self.detection_count = 0
        self.successful_detections = 0
