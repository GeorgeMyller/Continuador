"""
Configurações do Auto Clicker Pro
Centraliza todas as configurações e constantes do sistema
"""

import numpy as np

# Configurações de Interface
UI_CONFIG = {
    # Dimensões da janela
    "window_size": "650x750",
    "min_size": (600, 700),
    "padding": 20,
    # Fontes
    "font_family": "SF Pro Display",
    "font_sizes": {
        "title": 28,
        "subtitle": 14,
        "header": 16,
        "body": 12,
        "button": 12,
        "small": 11,
    },
    # Cores do tema
    "colors": {
        "primary": "#2E86AB",  # Azul
        "success": "#A23B72",  # Verde-rosa
        "warning": "#F18F01",  # Laranja
        "danger": "#C73E1D",  # Vermelho
        "dark": "#1A1A1A",  # Cinza escuro
        "light": "#F8F9FA",  # Cinza claro
        "background": "#FFFFFF",  # Branco
        "card_bg": "#F8F9FA",  # Fundo dos cards
        "border": "#E9ECEF",  # Cor da borda
    },
}

# Configurações de Detecção de Cor
COLOR_DETECTION = {
    # Faixas de cor azul em HSV
    "blue_ranges": [
        {
            "name": "standard_blue",
            "lower": np.array([105, 80, 80]),
            "upper": np.array([125, 255, 255]),
        },
        {
            "name": "light_blue",
            "lower": np.array([95, 60, 100]),
            "upper": np.array([115, 200, 255]),
        },
    ],
    # Configurações de processamento de imagem
    "morphology_kernel_size": (3, 3),
    "min_blue_ratio": 0.3,  # Mínimo 30% de pixels azuis para ser considerado botão
}

# Configurações de Detecção de Botão
BUTTON_DETECTION = {
    # Filtros de área (base para 1920x1080)
    "base_min_area": 1000,
    "base_max_area": 20000,
    # Filtros de dimensão (base para 1920x1080)
    "base_min_width": 50,
    "base_max_width": 300,
    "base_min_height": 20,
    "base_max_height": 80,
    # Filtros de proporção (não mudam com resolução)
    "min_aspect_ratio": 1.8,
    "max_aspect_ratio": 6.0,
    # Margem das bordas da tela (percentual da tela)
    "edge_margin_percent": 0.05,  # 5% da largura/altura da tela
    # Pesos para cálculo de score
    "score_weights": {"blue_ratio": 0.5, "position": 0.3, "size": 0.2},
}

# Configurações de Adaptação de Resolução
RESOLUTION_ADAPTATION = {
    # Resolução de referência para cálculos
    "reference_width": 1920,
    "reference_height": 1080,
    # Fatores de escala adaptativos
    "scale_factors": {
        "area": True,  # Escalar área com base na resolução
        "dimensions": True,  # Escalar largura/altura
        "position": True,  # Adaptar posições
    },
    # Cache de configurações por resolução
    "cache_enabled": True,
    "max_cache_size": 10,
    # Tolerância para considerar resoluções similares
    "resolution_tolerance": 0.1,  # 10% de diferença
    # Configurações de DPI
    "dpi_awareness": True,
    "scale_dpi": True,
}

# Configurações de Monitoramento
MONITORING_CONFIG = {
    # Intervalo de verificação
    "default_interval": 0.5,
    "min_interval": 0.1,
    "max_interval": 5.0,
    # Delay após clique
    "post_click_delay": 2.0,
    # Configurações de segurança
    "failsafe_enabled": True,
    "pause_between_actions": 0.1,
}

# Configurações de Debug
DEBUG_CONFIG = {
    "save_images": False,
    "debug_dir": "debug_images",
    "image_format": ".png",
    "timestamp_format": "%Y%m%d_%H%M%S",
}

# Configurações de Performance
PERFORMANCE_CONFIG = {
    # Configurações de thread
    "daemon_threads": True,
    # Timeouts
    "detection_timeout": 5.0,
    "ui_update_interval": 1000,  # ms
}

# Mensagens do Sistema
MESSAGES = {
    "startup": {
        "title": "=== Auto Clicker Pro - Interface Moderna ===",
        "initializing": "Iniciando aplicação com interface aprimorada...",
        "modern_features": "🎯 Interface moderna com estatísticas em tempo real",
        "detection": "🔵 Detecção inteligente de botões azuis",
        "emergency": "🖱️  Para parar em emergência: mova o mouse para o canto superior esquerdo",
        "starting_gui": "🚀 Iniciando interface gráfica...\n",
    },
    "macos_permissions": {
        "warning": "\n⚠️  IMPORTANTE para macOS:",
        "instructions": [
            "Você precisa conceder permissões de acessibilidade:",
            "1. Vá em Preferências do Sistema",
            "2. Segurança e Privacidade > Privacidade > Acessibilidade",
            "3. Adicione o Terminal ou Python à lista de aplicações permitidas",
            "4. Marque a caixa de seleção para ativar",
        ],
    },
    "status": {
        "stopped": "Sistema Parado",
        "monitoring": "Monitorando...",
        "button_found": "Botão encontrado! Clicando...",
        "emergency_stop": "Parada de Emergência!",
    },
    "instructions": [
        "• O sistema detecta botões azuis automaticamente na tela",
        "• Clica em botões que tenham formato típico de 'Continue'",
        "• Use o modo Debug para visualizar as detecções",
        "• Ajuste o intervalo conforme necessário",
        "• Para parada de emergência: canto superior esquerdo",
    ],
}

# Configurações específicas do PyAutoGUI
PYAUTOGUI_CONFIG = {"failsafe": True, "pause": 0.1}
