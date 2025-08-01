"""
Sistema de Monitoramento do Auto Clicker Pro
Módulo responsável pelo gerenciamento do monitoramento e cliques automáticos
"""

import threading
import time
from typing import Optional, Callable, Dict, Any

import pyautogui

try:
    from .detector import BlueButtonDetector
    from .config import MONITORING_CONFIG, MESSAGES
except ImportError:
    from detector import BlueButtonDetector
    from config import MONITORING_CONFIG, MESSAGES


class MonitoringManager:
    """
    Gerenciador do sistema de monitoramento
    
    Coordena a detecção de botões e execução de cliques automáticos
    """
    
    def __init__(self):
        """Inicializa o gerenciador de monitoramento"""
        # Estado do monitoramento
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Configurações
        self.monitor_interval = MONITORING_CONFIG['default_interval']
        self.debug_mode = False
        
        # Estatísticas
        self.click_count = 0
        self.session_start_time: Optional[float] = None
        self.detection_times = []
        
        # Detector de botões
        self.detector: Optional[BlueButtonDetector] = None
        
        # Callbacks para UI
        self.status_callback: Optional[Callable[[str, str], None]] = None
        self.click_callback: Optional[Callable[[int], None]] = None
        self.stats_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        
        # Configurar PyAutoGUI
        self._setup_pyautogui()
    
    def _setup_pyautogui(self) -> None:
        """Configura as opções de segurança do PyAutoGUI"""
        pyautogui.FAILSAFE = MONITORING_CONFIG['failsafe_enabled']
        pyautogui.PAUSE = MONITORING_CONFIG['pause_between_actions']
    
    def set_callbacks(self, status_callback: Callable[[str, str], None],
                     click_callback: Callable[[int], None],
                     stats_callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Define os callbacks para comunicação com a UI
        
        Args:
            status_callback: Callback para atualização de status (status, color)
            click_callback: Callback para atualização do contador de cliques
            stats_callback: Callback para atualização de estatísticas
        """
        self.status_callback = status_callback
        self.click_callback = click_callback
        self.stats_callback = stats_callback
    
    def start_monitoring(self, interval: Optional[float] = None, debug_mode: bool = False) -> bool:
        """
        Inicia o monitoramento
        
        Args:
            interval: Intervalo entre verificações (opcional)
            debug_mode: Se deve salvar imagens de debug
            
        Returns:
            True se iniciou com sucesso, False caso contrário
        """
        if self.is_monitoring:
            return False
        
        # Atualizar configurações
        if interval is not None:
            self.monitor_interval = interval
        self.debug_mode = debug_mode
        
        # Inicializar detector
        self.detector = BlueButtonDetector(debug_mode=self.debug_mode)
        
        # Resetar estatísticas
        self._reset_statistics()
        
        # Iniciar monitoramento
        self.is_monitoring = True
        self.session_start_time = time.time()
        
        # Atualizar status
        self._update_status(MESSAGES['status']['monitoring'], "#F18F01")  # warning color
        
        # Iniciar thread de monitoramento
        self.monitor_thread = threading.Thread(
            target=self._monitor_worker, 
            daemon=MONITORING_CONFIG.get('daemon_threads', True)
        )
        self.monitor_thread.start()
        
        return True
    
    def stop_monitoring(self) -> None:
        """Para o monitoramento"""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        
        # Aguardar thread terminar
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1.0)
        
        # Atualizar status
        self._update_status(MESSAGES['status']['stopped'], "#C73E1D")  # danger color
        
        # Limpar referências
        self.monitor_thread = None
        self.detector = None
    
    def _monitor_worker(self) -> None:
        """Worker thread para o monitoramento contínuo"""
        try:
            while self.is_monitoring:
                self._monitoring_cycle()
                time.sleep(self.monitor_interval)
                
        except pyautogui.FailSafeException:
            # Parada de emergência acionada
            self._handle_emergency_stop()
        except Exception as e:
            print(f"Erro no monitoramento: {e}")
        finally:
            # Garantir que o monitoramento seja parado
            if self.is_monitoring:
                self._schedule_ui_update(self.stop_monitoring)
    
    def _monitoring_cycle(self) -> None:
        """Executa um ciclo completo de monitoramento"""
        if not self.detector:
            return
        
        try:
            # Medir tempo de detecção
            detection_start = time.time()
            button_info = self.detector.detect_button()
            detection_time = time.time() - detection_start
            
            # Armazenar tempo de detecção
            self.detection_times.append(detection_time)
            
            if button_info:
                # Botão encontrado
                self._handle_button_found(button_info)
            
            # Atualizar estatísticas
            self._update_statistics()
            
        except Exception as e:
            print(f"Erro no ciclo de monitoramento: {e}")
    
    def _handle_button_found(self, button_info: tuple) -> None:
        """
        Processa botão encontrado e executa clique
        
        Args:
            button_info: Tupla (center_x, center_y, width, height)
        """
        x, y, w, h = button_info
        
        # Atualizar status
        self._update_status(MESSAGES['status']['button_found'], "#A23B72")  # success color
        
        # Executar clique
        pyautogui.click(x, y)
        
        # Incrementar contador
        self.click_count += 1
        self._update_click_counter()
        
        # Aguardar após o clique
        time.sleep(MONITORING_CONFIG['post_click_delay'])
        
        # Voltar para status de monitoramento
        self._update_status(MESSAGES['status']['monitoring'], "#F18F01")  # warning color
    
    def _handle_emergency_stop(self) -> None:
        """Processa parada de emergência"""
        self._schedule_ui_update(
            lambda: self._update_status(MESSAGES['status']['emergency_stop'], "#C73E1D")
        )
        self._schedule_ui_update(self.stop_monitoring)
    
    def _reset_statistics(self) -> None:
        """Reseta todas as estatísticas"""
        self.click_count = 0
        self.detection_times = []
        if self.detector:
            self.detector.reset_statistics()
        self._update_click_counter()
    
    def _update_statistics(self) -> None:
        """Atualiza e envia estatísticas para a UI"""
        if not self.detector or not self.stats_callback:
            return
        
        # Obter estatísticas do detector
        detector_stats = self.detector.get_statistics()
        
        # Calcular estatísticas adicionais
        avg_detection_time = (
            sum(self.detection_times) / len(self.detection_times)
            if self.detection_times else 0
        )
        
        # Manter apenas os últimos 100 tempos para evitar uso excessivo de memória
        if len(self.detection_times) > 100:
            self.detection_times = self.detection_times[-100:]
        
        # Preparar estatísticas completas
        stats = {
            'click_count': self.click_count,
            'avg_detection_time': avg_detection_time,
            'success_rate': detector_stats['success_rate'],
            'total_detections': detector_stats['total_detections'],
            'successful_detections': detector_stats['successful_detections']
        }
        
        # Enviar para UI
        if self.stats_callback:
            self._schedule_ui_update(lambda: self.stats_callback(stats))
    
    def _update_status(self, status: str, color: str) -> None:
        """Atualiza status na UI"""
        if self.status_callback:
            self._schedule_ui_update(lambda: self.status_callback(status, color))
    
    def _update_click_counter(self) -> None:
        """Atualiza contador de cliques na UI"""
        if self.click_callback:
            self._schedule_ui_update(lambda: self.click_callback(self.click_count))
    
    def _schedule_ui_update(self, callback: Callable) -> None:
        """
        Agenda uma atualização da UI na thread principal
        
        Args:
            callback: Função para executar na thread principal
        """
        try:
            # Esta função deve ser sobrescrita pela aplicação principal
            # para usar root.after() do Tkinter
            callback()
        except Exception as e:
            print(f"Erro ao atualizar UI: {e}")
    
    def set_ui_scheduler(self, scheduler: Callable[[Callable], None]) -> None:
        """
        Define o agendador de atualizações da UI
        
        Args:
            scheduler: Função que agenda callbacks na thread da UI
        """
        self._schedule_ui_update = scheduler
    
    def update_interval(self, interval: float) -> None:
        """
        Atualiza o intervalo de monitoramento
        
        Args:
            interval: Novo intervalo em segundos
        """
        self.monitor_interval = max(
            MONITORING_CONFIG['min_interval'],
            min(interval, MONITORING_CONFIG['max_interval'])
        )
    
    def get_session_time(self) -> float:
        """
        Retorna o tempo de sessão atual
        
        Returns:
            Tempo de sessão em segundos
        """
        if self.session_start_time and self.is_monitoring:
            return time.time() - self.session_start_time
        return 0.0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas completas do sistema
        
        Returns:
            Dicionário com todas as estatísticas
        """
        detector_stats = self.detector.get_statistics() if self.detector else {}
        
        avg_detection_time = (
            sum(self.detection_times) / len(self.detection_times)
            if self.detection_times else 0
        )
        
        return {
            'is_monitoring': self.is_monitoring,
            'click_count': self.click_count,
            'session_time': self.get_session_time(),
            'monitor_interval': self.monitor_interval,
            'debug_mode': self.debug_mode,
            'avg_detection_time': avg_detection_time,
            **detector_stats
        }
