"""
Interface Gráfica Moderna do Auto Clicker Pro
Módulo responsável pela criação e gerenciamento da interface do usuário
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

try:
    from .config import UI_CONFIG, MESSAGES
except ImportError:
    from config import UI_CONFIG, MESSAGES


class ModernUI:
    """
    Interface gráfica moderna para o Auto Clicker Pro
    
    Utiliza design moderno com cards, cores consistentes e layout responsivo
    """
    
    def __init__(self, root: tk.Tk):
        """
        Inicializa a interface
        
        Args:
            root: Janela principal do Tkinter
        """
        self.root = root
        self.colors = UI_CONFIG['colors']
        self.fonts = UI_CONFIG['font_sizes']
        
        # Variáveis da interface
        self.monitor_interval = tk.DoubleVar(root, value=0.5)
        self.debug_var = tk.BooleanVar(root)
        
        # Labels que serão atualizados
        self.status_indicator: Optional[tk.Label] = None
        self.status_text: Optional[tk.Label] = None
        self.click_counter_label: Optional[tk.Label] = None
        self.session_time_label: Optional[tk.Label] = None
        self.interval_value_label: Optional[tk.Label] = None
        self.success_rate_label: Optional[tk.Label] = None
        self.avg_time_label: Optional[tk.Label] = None
        
        # Botões de controle
        self.start_btn: Optional[tk.Button] = None
        self.stop_btn: Optional[tk.Button] = None
        
        # Callbacks (serão definidos externamente)
        self.start_callback: Optional[Callable] = None
        self.stop_callback: Optional[Callable] = None
        self.interval_change_callback: Optional[Callable] = None
        
        self._setup_window()
        self._setup_styles()
        self._create_interface()
        self._center_window()
    
    def _setup_window(self) -> None:
        """Configura as propriedades básicas da janela"""
        self.root.title("🎯 Auto Clicker Pro - Detector de Botão Azul")
        self.root.geometry(UI_CONFIG['window_size'])
        self.root.resizable(True, True)
        self.root.minsize(*UI_CONFIG['min_size'])
        self.root.configure(bg=self.colors['background'])
    
    def _setup_styles(self) -> None:
        """Configura estilos modernos para a interface"""
        style = ttk.Style()
        
        # Usar tema moderno se disponível
        try:
            style.theme_use('clam')
        except Exception:
            pass
        
        # Configurar estilos customizados
        style.configure('Title.TLabel', 
                       font=(UI_CONFIG['font_family'], self.fonts['title'], 'bold'),
                       foreground=self.colors['dark'])
        
        style.configure('Subtitle.TLabel', 
                       font=(UI_CONFIG['font_family'], self.fonts['subtitle'], 'normal'),
                       foreground=self.colors['dark'])
        
        style.configure('Card.TFrame', 
                       background=self.colors['card_bg'],
                       relief='flat',
                       borderwidth=1)
    
    def _center_window(self) -> None:
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_interface(self) -> None:
        """Cria toda a interface do usuário"""
        # Container principal
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, 
                           padx=UI_CONFIG['padding'], pady=UI_CONFIG['padding'])
        
        # Seções da interface
        self._create_header(main_container)
        self._create_content_area(main_container)
    
    def _create_header(self, parent: tk.Widget) -> None:
        """Cria a seção do cabeçalho"""
        header_frame = tk.Frame(parent, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título principal
        title_frame = tk.Frame(header_frame, bg=self.colors['background'])
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(
            title_frame,
            text="🎯 Auto Clicker Pro",
            font=(UI_CONFIG['font_family'], self.fonts['title'], 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['background']
        )
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(
            title_frame,
            text="Detector Inteligente de Botões Azuis",
            font=(UI_CONFIG['font_family'], self.fonts['subtitle'], 'normal'),
            fg=self.colors['dark'],
            bg=self.colors['background']
        )
        subtitle_label.pack(anchor='w', pady=(5, 0))
    
    def _create_content_area(self, parent: tk.Widget) -> None:
        """Cria a área de conteúdo principal"""
        content_frame = tk.Frame(parent, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Layout de duas colunas
        left_column = tk.Frame(content_frame, bg=self.colors['background'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        right_column = tk.Frame(content_frame, bg=self.colors['background'])
        right_column.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        
        # Criar cards
        self._create_monitor_card(left_column)
        self._create_status_card(right_column)
        self._create_settings_card(left_column)
        self._create_stats_card(right_column)
        self._create_instructions_card(parent)
    
    def _create_card(self, parent: tk.Widget, title: str, height: Optional[int] = None) -> tk.Widget:
        """
        Cria um card moderno
        
        Args:
            parent: Widget pai
            title: Título do card
            height: Altura fixa (opcional)
            
        Returns:
            Frame do conteúdo do card
        """
        card_frame = tk.Frame(
            parent,
            bg=self.colors['card_bg'],
            relief='solid',
            bd=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        card_frame.pack(fill=tk.X, pady=(0, 15))
        
        if height:
            card_frame.configure(height=height)
            card_frame.pack_propagate(False)
        
        # Cabeçalho do card
        header = tk.Frame(card_frame, bg=self.colors['card_bg'])
        header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        title_label = tk.Label(
            header,
            text=title,
            font=(UI_CONFIG['font_family'], self.fonts['header'], 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['card_bg']
        )
        title_label.pack(side=tk.LEFT)
        
        # Conteúdo do card
        content = tk.Frame(card_frame, bg=self.colors['card_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        return content
    
    def _create_monitor_card(self, parent: tk.Widget) -> None:
        """Cria o card de controle de monitoramento"""
        content = self._create_card(parent, "🔍 Controle de Monitoramento")
        
        # Indicador de status
        status_display = tk.Frame(content, bg=self.colors['card_bg'])
        status_display.pack(fill=tk.X, pady=(0, 15))
        
        self.status_indicator = tk.Label(
            status_display,
            text="●",
            font=(UI_CONFIG['font_family'], 20),
            fg=self.colors['danger'],
            bg=self.colors['card_bg']
        )
        self.status_indicator.pack(side=tk.LEFT)
        
        self.status_text = tk.Label(
            status_display,
            text=MESSAGES['status']['stopped'],
            font=(UI_CONFIG['font_family'], self.fonts['body'], 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['card_bg']
        )
        self.status_text.pack(side=tk.LEFT, padx=(10, 0))
        
        # Botões de controle
        self._create_control_buttons(content)
    
    def _create_control_buttons(self, parent: tk.Widget) -> None:
        """Cria os botões de controle"""
        button_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botão iniciar
        self.start_btn = tk.Button(
            button_frame,
            text="▶ Iniciar Monitoramento",
            font=(UI_CONFIG['font_family'], self.fonts['button'], 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=12,
            cursor='hand2',
            command=self._on_start_clicked
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão parar
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Parar",
            font=(UI_CONFIG['font_family'], self.fonts['button'], 'bold'),
            bg=self.colors['danger'],
            fg='white',
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=12,
            cursor='hand2',
            state=tk.DISABLED,
            command=self._on_stop_clicked
        )
        self.stop_btn.pack(side=tk.LEFT)
    
    def _create_status_card(self, parent: tk.Widget) -> None:
        """Cria o card de status do sistema"""
        content = self._create_card(parent, "📊 Status do Sistema", height=160)
        
        # Contador de cliques
        self._create_counter_row(content, "Cliques:", "click_counter_label")
        
        # Tempo de sessão
        self._create_counter_row(content, "Tempo:", "session_time_label", 
                               default_value="00:00", top_margin=15)
    
    def _create_counter_row(self, parent: tk.Widget, label: str, attr_name: str, 
                          default_value: str = "0", top_margin: int = 10) -> None:
        """Cria uma linha de contador"""
        counter_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        counter_frame.pack(fill=tk.X, pady=(top_margin, 0))
        
        tk.Label(
            counter_frame,
            text=label,
            font=(UI_CONFIG['font_family'], self.fonts['body']),
            fg=self.colors['dark'],
            bg=self.colors['card_bg']
        ).pack(side=tk.LEFT)
        
        label_widget = tk.Label(
            counter_frame,
            text=default_value,
            font=(UI_CONFIG['font_family'], 18 if attr_name == "click_counter_label" else 14, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['card_bg']
        )
        label_widget.pack(side=tk.RIGHT)
        
        setattr(self, attr_name, label_widget)
    
    def _create_settings_card(self, parent: tk.Widget) -> None:
        """Cria o card de configurações"""
        content = self._create_card(parent, "⚙️ Configurações")
        
        # Configuração de intervalo
        self._create_interval_setting(content)
        
        # Modo debug
        self._create_debug_setting(content)
    
    def _create_interval_setting(self, parent: tk.Widget) -> None:
        """Cria a configuração de intervalo"""
        interval_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        interval_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Labels do intervalo
        label_frame = tk.Frame(interval_frame, bg=self.colors['card_bg'])
        label_frame.pack(fill=tk.X)
        
        tk.Label(
            label_frame,
            text="Intervalo de Verificação",
            font=(UI_CONFIG['font_family'], self.fonts['body'], 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['card_bg']
        ).pack(side=tk.LEFT)
        
        self.interval_value_label = tk.Label(
            label_frame,
            text="0.5s",
            font=(UI_CONFIG['font_family'], self.fonts['body']),
            fg=self.colors['primary'],
            bg=self.colors['card_bg']
        )
        self.interval_value_label.pack(side=tk.RIGHT)
        
        # Slider
        self.interval_scale = tk.Scale(
            interval_frame,
            from_=0.1,
            to=5.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.monitor_interval,
            bg=self.colors['card_bg'],
            fg=self.colors['dark'],
            highlightthickness=0,
            troughcolor=self.colors['border'],
            activebackground=self.colors['primary'],
            command=self._on_interval_changed
        )
        self.interval_scale.pack(fill=tk.X, pady=(5, 0))
    
    def _create_debug_setting(self, parent: tk.Widget) -> None:
        """Cria a configuração de debug"""
        debug_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        debug_frame.pack(fill=tk.X, pady=(10, 0))
        
        debug_check = tk.Checkbutton(
            debug_frame,
            text="🐛 Modo Debug (Salvar capturas)",
            variable=self.debug_var,
            font=(UI_CONFIG['font_family'], self.fonts['small']),
            fg=self.colors['dark'],
            bg=self.colors['card_bg'],
            selectcolor=self.colors['success'],
            activebackground=self.colors['card_bg'],
            cursor='hand2'
        )
        debug_check.pack(anchor='w')
    
    def _create_stats_card(self, parent: tk.Widget) -> None:
        """Cria o card de estatísticas"""
        content = self._create_card(parent, "📈 Estatísticas", height=130)
        
        # Taxa de sucesso
        self._create_stat_row(content, "Taxa de Sucesso:", "success_rate_label", 
                            "N/A", self.colors['success'])
        
        # Tempo médio
        self._create_stat_row(content, "Tempo Médio:", "avg_time_label", 
                            "N/A", self.colors['primary'], top_margin=15)
    
    def _create_stat_row(self, parent: tk.Widget, label: str, attr_name: str, 
                       default_value: str, color: str, top_margin: int = 10) -> None:
        """Cria uma linha de estatística"""
        stat_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        stat_frame.pack(fill=tk.X, pady=(top_margin, 0))
        
        tk.Label(
            stat_frame,
            text=label,
            font=(UI_CONFIG['font_family'], self.fonts['small']),
            fg=self.colors['dark'],
            bg=self.colors['card_bg']
        ).pack(side=tk.LEFT)
        
        label_widget = tk.Label(
            stat_frame,
            text=default_value,
            font=(UI_CONFIG['font_family'], self.fonts['small'], 'bold'),
            fg=color,
            bg=self.colors['card_bg']
        )
        label_widget.pack(side=tk.RIGHT)
        
        setattr(self, attr_name, label_widget)
    
    def _create_instructions_card(self, parent: tk.Widget) -> None:
        """Cria o card de instruções"""
        content = self._create_card(parent, "💡 Como Usar")
        
        # Lista de instruções
        for i, instruction in enumerate(MESSAGES['instructions']):
            inst_label = tk.Label(
                content,
                text=instruction,
                font=(UI_CONFIG['font_family'], self.fonts['small']),
                fg=self.colors['dark'],
                bg=self.colors['card_bg'],
                justify=tk.LEFT,
                wraplength=520
            )
            inst_label.pack(anchor='w', pady=(3 if i > 0 else 0, 0))
        
        # Aviso de emergência
        self._create_emergency_warning(content)
    
    def _create_emergency_warning(self, parent: tk.Widget) -> None:
        """Cria o aviso de emergência"""
        warning_frame = tk.Frame(parent, bg='#FFF3CD', relief='solid', bd=1)
        warning_frame.pack(fill=tk.X, pady=(20, 0))
        
        warning_label = tk.Label(
            warning_frame,
            text="⚠️ EMERGÊNCIA: Mova o mouse para o canto superior esquerdo para parar",
            font=(UI_CONFIG['font_family'], 10, 'bold'),
            fg='#856404',
            bg='#FFF3CD',
            wraplength=500,
            justify=tk.CENTER
        )
        warning_label.pack(pady=10)
    
    # Métodos de callback
    def _on_start_clicked(self) -> None:
        """Callback para botão iniciar"""
        if self.start_callback:
            self.start_callback()
    
    def _on_stop_clicked(self) -> None:
        """Callback para botão parar"""
        if self.stop_callback:
            self.stop_callback()
    
    def _on_interval_changed(self, value: str) -> None:
        """Callback para mudança de intervalo"""
        if self.interval_value_label:
            self.interval_value_label.config(text=f"{float(value):.1f}s")
        if self.interval_change_callback:
            self.interval_change_callback(float(value))
    
    # Métodos públicos para atualização da interface
    def set_callbacks(self, start_callback: Callable, stop_callback: Callable, 
                     interval_callback: Optional[Callable] = None) -> None:
        """Define os callbacks da interface"""
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.interval_change_callback = interval_callback
    
    def update_status(self, status: str, color: str) -> None:
        """Atualiza o indicador de status"""
        if self.status_indicator:
            self.status_indicator.config(fg=color)
        if self.status_text:
            self.status_text.config(text=status)
    
    def update_click_counter(self, count: int) -> None:
        """Atualiza o contador de cliques"""
        if self.click_counter_label:
            self.click_counter_label.config(text=str(count))
    
    def update_session_time(self, time_str: str) -> None:
        """Atualiza o tempo de sessão"""
        if self.session_time_label:
            self.session_time_label.config(text=time_str)
    
    def update_success_rate(self, rate: float) -> None:
        """Atualiza a taxa de sucesso"""
        if self.success_rate_label:
            self.success_rate_label.config(text=f"{rate:.1f}%")
    
    def update_avg_time(self, time: float) -> None:
        """Atualiza o tempo médio"""
        if self.avg_time_label:
            self.avg_time_label.config(text=f"{time:.2f}s")
    
    def set_monitoring_state(self, is_monitoring: bool) -> None:
        """Define o estado dos botões de controle"""
        if is_monitoring:
            if self.start_btn:
                self.start_btn.config(state=tk.DISABLED)
            if self.stop_btn:
                self.stop_btn.config(state=tk.NORMAL)
        else:
            if self.start_btn:
                self.start_btn.config(state=tk.NORMAL)
            if self.stop_btn:
                self.stop_btn.config(state=tk.DISABLED)
    
    def get_monitor_interval(self) -> float:
        """Retorna o intervalo de monitoramento atual"""
        return self.monitor_interval.get()
    
    def get_debug_mode(self) -> bool:
        """Retorna se o modo debug está ativo"""
        return self.debug_var.get()
