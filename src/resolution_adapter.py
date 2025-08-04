"""
Sistema de Adaptação de Resolução
Módulo responsável por adaptar parâmetros de detecção conforme a resolução da tela
"""

import math
from typing import Any, Dict, Optional, Tuple

import pyautogui

try:
    from .config import BUTTON_DETECTION, RESOLUTION_ADAPTATION
except ImportError:
    from config import BUTTON_DETECTION, RESOLUTION_ADAPTATION


class ResolutionAdapter:
    """
    Adaptador que ajusta parâmetros de detecção baseado na resolução atual da tela

    Resolve problemas quando a resolução muda, mantendo a detecção eficaz
    """

    def __init__(self):
        """Inicializa o adaptador de resolução"""
        self.config_cache: Dict[Tuple[int, int], Dict[str, Any]] = {}
        self.current_resolution: Optional[Tuple[int, int]] = None
        self.scale_factor_x: float = 1.0
        self.scale_factor_y: float = 1.0
        self._update_resolution()

    def _update_resolution(self) -> None:
        """Atualiza a resolução atual da tela"""
        try:
            # Obter tamanho da tela
            screen_width, screen_height = pyautogui.size()
            new_resolution = (screen_width, screen_height)

            # Verificar se a resolução mudou
            if new_resolution != self.current_resolution:
                self.current_resolution = new_resolution
                self._calculate_scale_factors()
                print(f"📐 Resolução detectada: {screen_width}x{screen_height}")
                print(
                    f"📏 Fatores de escala: X={self.scale_factor_x:.2f}, Y={self.scale_factor_y:.2f}"
                )

        except Exception as e:
            print(f"❌ Erro ao obter resolução da tela: {e}")
            # Usar resolução padrão se falhar
            self.current_resolution = (1920, 1080)
            self.scale_factor_x = 1.0
            self.scale_factor_y = 1.0

    def _calculate_scale_factors(self) -> None:
        """Calcula os fatores de escala baseado na resolução de referência"""
        if not self.current_resolution:
            return

        ref_width = RESOLUTION_ADAPTATION["reference_width"]
        ref_height = RESOLUTION_ADAPTATION["reference_height"]

        current_width, current_height = self.current_resolution

        # Calcular fatores de escala
        self.scale_factor_x = current_width / ref_width
        self.scale_factor_y = current_height / ref_height

        # Para área, usar a média geométrica dos fatores
        self.area_scale_factor = math.sqrt(self.scale_factor_x * self.scale_factor_y)

    def get_adapted_config(self) -> Dict[str, Any]:
        """
        Retorna configurações adaptadas para a resolução atual

        Returns:
            Dicionário com parâmetros adaptados para a resolução
        """
        # Verificar se a resolução mudou
        self._update_resolution()

        if not self.current_resolution:
            return self._get_default_config()

        # Verificar cache
        if (
            RESOLUTION_ADAPTATION["cache_enabled"]
            and self.current_resolution in self.config_cache
        ):
            return self.config_cache[self.current_resolution]

        # Gerar nova configuração adaptada
        adapted_config = self._generate_adapted_config()

        # Armazenar no cache
        if RESOLUTION_ADAPTATION["cache_enabled"]:
            self._update_cache(adapted_config)

        return adapted_config

    def _generate_adapted_config(self) -> Dict[str, Any]:
        """Gera configuração adaptada para a resolução atual"""
        config = {}

        # Adaptar dimensões se habilitado
        if RESOLUTION_ADAPTATION["scale_factors"]["dimensions"]:
            config["min_width"] = int(
                BUTTON_DETECTION["base_min_width"] * self.scale_factor_x
            )
            config["max_width"] = int(
                BUTTON_DETECTION["base_max_width"] * self.scale_factor_x
            )
            config["min_height"] = int(
                BUTTON_DETECTION["base_min_height"] * self.scale_factor_y
            )
            config["max_height"] = int(
                BUTTON_DETECTION["base_max_height"] * self.scale_factor_y
            )
        else:
            config["min_width"] = BUTTON_DETECTION["base_min_width"]
            config["max_width"] = BUTTON_DETECTION["base_max_width"]
            config["min_height"] = BUTTON_DETECTION["base_min_height"]
            config["max_height"] = BUTTON_DETECTION["base_max_height"]

        # Adaptar área se habilitado
        if RESOLUTION_ADAPTATION["scale_factors"]["area"]:
            config["min_area"] = int(
                BUTTON_DETECTION["base_min_area"] * self.area_scale_factor
            )
            config["max_area"] = int(
                BUTTON_DETECTION["base_max_area"] * self.area_scale_factor
            )
        else:
            config["min_area"] = BUTTON_DETECTION["base_min_area"]
            config["max_area"] = BUTTON_DETECTION["base_max_area"]

        # Proporções não mudam com resolução
        config["min_aspect_ratio"] = BUTTON_DETECTION["min_aspect_ratio"]
        config["max_aspect_ratio"] = BUTTON_DETECTION["max_aspect_ratio"]

        # Margem das bordas como percentual
        if self.current_resolution:
            width, height = self.current_resolution
            edge_margin_percent = BUTTON_DETECTION["edge_margin_percent"]
            config["edge_margin"] = int(min(width, height) * edge_margin_percent)
        else:
            config["edge_margin"] = 50

        # Pesos não mudam
        config["score_weights"] = BUTTON_DETECTION["score_weights"].copy()

        # Adicionar metadados
        config["resolution"] = self.current_resolution
        config["scale_factors"] = {
            "x": self.scale_factor_x,
            "y": self.scale_factor_y,
            "area": self.area_scale_factor,
        }

        return config

    def _get_default_config(self) -> Dict[str, Any]:
        """Retorna configuração padrão quando não é possível detectar resolução"""
        return {
            "min_width": BUTTON_DETECTION["base_min_width"],
            "max_width": BUTTON_DETECTION["base_max_width"],
            "min_height": BUTTON_DETECTION["base_min_height"],
            "max_height": BUTTON_DETECTION["base_max_height"],
            "min_area": BUTTON_DETECTION["base_min_area"],
            "max_area": BUTTON_DETECTION["base_max_area"],
            "min_aspect_ratio": BUTTON_DETECTION["min_aspect_ratio"],
            "max_aspect_ratio": BUTTON_DETECTION["max_aspect_ratio"],
            "edge_margin": 50,
            "score_weights": BUTTON_DETECTION["score_weights"].copy(),
            "resolution": (1920, 1080),
            "scale_factors": {"x": 1.0, "y": 1.0, "area": 1.0},
        }

    def _update_cache(self, config: Dict[str, Any]) -> None:
        """Atualiza o cache de configurações"""
        if not self.current_resolution:
            return

        # Limitar tamanho do cache
        max_size = RESOLUTION_ADAPTATION["max_cache_size"]
        if len(self.config_cache) >= max_size:
            # Remover entrada mais antiga (FIFO)
            oldest_key = next(iter(self.config_cache))
            del self.config_cache[oldest_key]

        # Adicionar nova entrada
        self.config_cache[self.current_resolution] = config

    def is_resolution_similar(
        self, resolution1: Tuple[int, int], resolution2: Tuple[int, int]
    ) -> bool:
        """
        Verifica se duas resoluções são suficientemente similares

        Args:
            resolution1: Primeira resolução (width, height)
            resolution2: Segunda resolução (width, height)

        Returns:
            True se as resoluções são similares dentro da tolerância
        """
        tolerance = RESOLUTION_ADAPTATION["resolution_tolerance"]

        w1, h1 = resolution1
        w2, h2 = resolution2

        # Calcular diferença percentual
        width_diff = abs(w1 - w2) / max(w1, w2)
        height_diff = abs(h1 - h2) / max(h1, h2)

        return width_diff <= tolerance and height_diff <= tolerance

    def get_resolution_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre a resolução atual

        Returns:
            Dicionário com informações da resolução
        """
        self._update_resolution()

        if not self.current_resolution:
            return {"error": "Não foi possível detectar a resolução"}

        width, height = self.current_resolution
        ref_width = RESOLUTION_ADAPTATION["reference_width"]
        ref_height = RESOLUTION_ADAPTATION["reference_height"]

        return {
            "current_resolution": f"{width}x{height}",
            "reference_resolution": f"{ref_width}x{ref_height}",
            "scale_factor_x": self.scale_factor_x,
            "scale_factor_y": self.scale_factor_y,
            "area_scale_factor": self.area_scale_factor,
            "is_reference": (width == ref_width and height == ref_height),
            "cache_size": len(self.config_cache),
            "dpi_scaling": pyautogui.screenshot().size != (width, height),
        }

    def clear_cache(self) -> None:
        """Limpa o cache de configurações"""
        self.config_cache.clear()
        print("🗑️ Cache de configurações de resolução limpo")

    def force_resolution_update(self) -> bool:
        """
        Força atualização da resolução (útil após mudanças manuais)

        Returns:
            True se a resolução mudou, False caso contrário
        """
        old_resolution = self.current_resolution
        self.current_resolution = None
        self._update_resolution()

        if old_resolution != self.current_resolution:
            print(
                f"🔄 Resolução atualizada: {old_resolution} → {self.current_resolution}"
            )
            return True
        return False


# Instância global do adaptador (singleton pattern)
_resolution_adapter = None


def get_resolution_adapter() -> ResolutionAdapter:
    """
    Retorna instância singleton do adaptador de resolução

    Returns:
        Instância do ResolutionAdapter
    """
    global _resolution_adapter
    if _resolution_adapter is None:
        _resolution_adapter = ResolutionAdapter()
    return _resolution_adapter
