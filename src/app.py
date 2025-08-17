"""
Auto Clicker Pro - Aplicação Principal
Sistema moderno de detecção e clique automático em botões azuis
"""

import sys
import tkinter as tk
from typing import Any, Dict

try:
    from .config import MESSAGES, UI_CONFIG
    from .monitor import MonitoringManager
    from .ui import ModernUI
except ImportError:
    from config import MESSAGES
    from monitor import MonitoringManager
    from ui import ModernUI


class AutoClickerPro:
    """
    Aplicação principal do Auto Clicker Pro

    Coordena a interface gráfica e o sistema de monitoramento
    """

    def __init__(self):
        """Inicializa a aplicação"""
        # Criar janela principal
        self.root = tk.Tk()

        # Inicializar componentes
        self.ui = ModernUI(self.root)
        self.monitor = MonitoringManager()

        # Configurar callbacks
        self._setup_callbacks()

        # Timer para atualização de tempo
        self._schedule_time_update()

    def _setup_callbacks(self) -> None:
        """Configura todos os callbacks entre componentes"""
        # Callbacks da UI para o monitor
        self.ui.set_callbacks(
            start_callback=self._on_start_monitoring,
            stop_callback=self._on_stop_monitoring,
            interval_callback=self._on_interval_changed,
        )

        # Callbacks do monitor para a UI
        self.monitor.set_callbacks(
            status_callback=self._on_status_update,
            click_callback=self._on_click_update,
            stats_callback=self._on_stats_update,
        )

        # Configurar agendador de UI
        self.monitor.set_ui_scheduler(self._schedule_ui_update)

        # Callback para fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_start_monitoring(self) -> None:
        """Callback para início do monitoramento"""
        interval = self.ui.get_monitor_interval()
        debug_mode = self.ui.get_debug_mode()

        success = self.monitor.start_monitoring(interval, debug_mode)

        if success:
            self.ui.set_monitoring_state(True)
            print("✅ Monitoramento iniciado")
        else:
            print("❌ Erro ao iniciar monitoramento")

    def _on_stop_monitoring(self) -> None:
        """Callback para parada do monitoramento"""
        self.monitor.stop_monitoring()
        self.ui.set_monitoring_state(False)
        print("⏹ Monitoramento parado")

    def _on_interval_changed(self, interval: float) -> None:
        """Callback para mudança de intervalo"""
        self.monitor.update_interval(interval)

    def _on_status_update(self, status: str, color: str) -> None:
        """Callback para atualização de status"""
        self.ui.update_status(status, color)

    def _on_click_update(self, count: int) -> None:
        """Callback para atualização do contador de cliques"""
        self.ui.update_click_counter(count)

    def _on_stats_update(self, stats: Dict[str, Any]) -> None:
        """Callback para atualização de estatísticas"""
        if "success_rate" in stats:
            self.ui.update_success_rate(stats["success_rate"])

        if "avg_detection_time" in stats:
            self.ui.update_avg_time(stats["avg_detection_time"])

    def _schedule_ui_update(self, callback) -> None:
        """Agenda atualização na thread da UI"""
        self.root.after(0, callback)

    def _schedule_time_update(self) -> None:
        """Agenda próxima atualização do tempo de sessão"""
        if self.monitor.is_monitoring:
            session_time = self.monitor.get_session_time()
            minutes = int(session_time // 60)
            seconds = int(session_time % 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.ui.update_session_time(time_str)

        # Agendar próxima atualização
        self.root.after(1000, self._schedule_time_update)

    def _on_closing(self) -> None:
        """Callback para fechamento da aplicação"""
        # Parar monitoramento se estiver ativo
        if self.monitor.is_monitoring:
            self.monitor.stop_monitoring()

        # Fechar janela
        self.root.destroy()
        print("👋 Aplicação encerrada")

    def run(self) -> None:
        """Executa a aplicação"""
        try:
            print("🚀 Iniciando Auto Clicker Pro...")
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n⚠️ Interrupção detectada")
            self._on_closing()
        except Exception as e:
            print(f"❌ Erro na aplicação: {e}")
            self._on_closing()


def print_startup_messages() -> None:
    """Imprime mensagens de inicialização"""
    startup = MESSAGES["startup"]

    print(startup["title"])
    print(startup["initializing"])

    # Verificar se é macOS
    if sys.platform == "darwin":
        macos = MESSAGES["macos_permissions"]
        print(macos["warning"])
        for instruction in macos["instructions"]:
            print(instruction)

    print(f"\n{startup['modern_features']}")
    print(startup["detection"])
    print(startup["emergency"])
    print(startup["starting_gui"])


def main() -> None:
    """Função principal da aplicação"""
    try:
        # Imprimir mensagens de inicialização
        print_startup_messages()

        # Criar e executar aplicação
        app = AutoClickerPro()
        app.run()

    except ImportError as e:
        print(f"❌ Erro de dependência: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
