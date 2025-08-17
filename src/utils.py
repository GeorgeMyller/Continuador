"""
Utilitários do Auto Clicker Pro
Funções auxiliares e ferramentas de desenvolvimento
"""

import json
import os
import time
from datetime import datetime
from typing import Any, Dict, Optional


class PerformanceProfiler:
    """
    Profiler simples para medir performance de operações
    """

    def __init__(self):
        """Inicializa o profiler"""
        self.timings: Dict[str, list] = {}
        self.active_timers: Dict[str, float] = {}

    def start_timer(self, operation: str) -> None:
        """
        Inicia um timer para uma operação

        Args:
            operation: Nome da operação
        """
        self.active_timers[operation] = time.time()

    def end_timer(self, operation: str) -> Optional[float]:
        """
        Finaliza um timer e retorna o tempo decorrido

        Args:
            operation: Nome da operação

        Returns:
            Tempo decorrido em segundos ou None se timer não foi iniciado
        """
        if operation not in self.active_timers:
            return None

        elapsed = time.time() - self.active_timers[operation]

        # Armazenar timing
        if operation not in self.timings:
            self.timings[operation] = []
        self.timings[operation].append(elapsed)

        # Limpar timer ativo
        del self.active_timers[operation]

        return elapsed

    def get_statistics(self, operation: str) -> Dict[str, float]:
        """
        Retorna estatísticas de uma operação

        Args:
            operation: Nome da operação

        Returns:
            Dicionário com estatísticas (min, max, avg, count)
        """
        if operation not in self.timings or not self.timings[operation]:
            return {}

        times = self.timings[operation]
        return {
            "min": min(times),
            "max": max(times),
            "avg": sum(times) / len(times),
            "count": len(times),
            "total": sum(times),
        }

    def get_all_statistics(self) -> Dict[str, Dict[str, float]]:
        """
        Retorna estatísticas de todas as operações

        Returns:
            Dicionário com estatísticas de todas as operações
        """
        return {op: self.get_statistics(op) for op in self.timings.keys()}


class ConfigManager:
    """
    Gerenciador de configurações persistentes
    """

    def __init__(self, config_file: str = "config.json"):
        """
        Inicializa o gerenciador

        Args:
            config_file: Caminho do arquivo de configuração
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Carrega configurações do arquivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            self.config = {}

    def save_config(self) -> bool:
        """
        Salva configurações no arquivo

        Returns:
            True se salvou com sucesso
        """
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração

        Args:
            key: Chave da configuração
            default: Valor padrão se não encontrar

        Returns:
            Valor da configuração
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Define valor de configuração

        Args:
            key: Chave da configuração
            value: Valor a definir
        """
        self.config[key] = value

    def update(self, new_config: Dict[str, Any]) -> None:
        """
        Atualiza múltiplas configurações

        Args:
            new_config: Dicionário com novas configurações
        """
        self.config.update(new_config)


class Logger:
    """
    Sistema de logging simples
    """

    def __init__(self, log_file: str = "auto_clicker.log", max_size: int = 1024 * 1024):
        """
        Inicializa o logger

        Args:
            log_file: Arquivo de log
            max_size: Tamanho máximo do arquivo em bytes
        """
        self.log_file = log_file
        self.max_size = max_size

        # Verificar se precisa rotacionar log
        self._rotate_if_needed()

    def _rotate_if_needed(self) -> None:
        """Rotaciona o log se necessário"""
        try:
            if os.path.exists(self.log_file):
                if os.path.getsize(self.log_file) > self.max_size:
                    # Criar backup
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"{self.log_file}.{timestamp}"
                    os.rename(self.log_file, backup_name)
        except Exception as e:
            print(f"Erro ao rotacionar log: {e}")

    def _write_log(self, level: str, message: str) -> None:
        """
        Escreve mensagem no log

        Args:
            level: Nível do log (INFO, WARNING, ERROR)
            message: Mensagem a escrever
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"[{timestamp}] {level}: {message}\n"

            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception as e:
            print(f"Erro ao escrever log: {e}")

    def info(self, message: str) -> None:
        """Log de informação"""
        self._write_log("INFO", message)

    def warning(self, message: str) -> None:
        """Log de aviso"""
        self._write_log("WARNING", message)

    def error(self, message: str) -> None:
        """Log de erro"""
        self._write_log("ERROR", message)


def format_time(seconds: float) -> str:
    """
    Formata tempo em segundos para formato legível

    Args:
        seconds: Tempo em segundos

    Returns:
        String formatada (ex: "2h 30m 15s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    secs = int(seconds % 60)

    if minutes < 60:
        return f"{minutes}m {secs}s"

    hours = int(minutes // 60)
    mins = int(minutes % 60)

    return f"{hours}h {mins}m {secs}s"


def validate_coordinates(x: int, y: int, screen_width: int, screen_height: int) -> bool:
    """
    Valida se coordenadas estão dentro da tela

    Args:
        x, y: Coordenadas a validar
        screen_width, screen_height: Dimensões da tela

    Returns:
        True se coordenadas são válidas
    """
    return 0 <= x < screen_width and 0 <= y < screen_height


def create_backup_filename(original: str) -> str:
    """
    Cria nome de arquivo de backup com timestamp

    Args:
        original: Nome do arquivo original

    Returns:
        Nome do arquivo de backup
    """
    name, ext = os.path.splitext(original)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_backup_{timestamp}{ext}"


def ensure_directory(path: str) -> bool:
    """
    Garante que um diretório existe, criando se necessário

    Args:
        path: Caminho do diretório

    Returns:
        True se diretório existe ou foi criado com sucesso
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório {path}: {e}")
        return False


# Instância global do profiler para uso em toda a aplicação
profiler = PerformanceProfiler()

# Instância global do logger
logger = Logger()

# Instância global do gerenciador de configurações
config_manager = ConfigManager()
