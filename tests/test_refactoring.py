"""
Testes básicos para o Auto Clicker Pro
Testes unitários para validar a refatoração
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch

# Adicionar src ao path para importações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestConfig(unittest.TestCase):
    """Testes para o módulo de configuração"""

    def test_config_imports(self):
        """Testa se as configurações podem ser importadas"""
        try:
            from config import BUTTON_DETECTION, COLOR_DETECTION, UI_CONFIG

            self.assertIsInstance(UI_CONFIG, dict)
            self.assertIsInstance(COLOR_DETECTION, dict)
            self.assertIsInstance(BUTTON_DETECTION, dict)
        except ImportError as e:
            self.fail(f"Erro ao importar configurações: {e}")

    def test_color_ranges(self):
        """Testa se os ranges de cor estão bem definidos"""
        from config import COLOR_DETECTION

        self.assertIn("blue_ranges", COLOR_DETECTION)
        blue_ranges = COLOR_DETECTION["blue_ranges"]
        self.assertIsInstance(blue_ranges, list)
        self.assertGreater(len(blue_ranges), 0)

        for range_config in blue_ranges:
            self.assertIn("name", range_config)
            self.assertIn("lower", range_config)
            self.assertIn("upper", range_config)


class TestDetector(unittest.TestCase):
    """Testes para o detector de botões"""

    @patch("detector.pyautogui")
    @patch("detector.cv2")
    def test_detector_initialization(self, mock_cv2, mock_pyautogui):
        """Testa inicialização do detector"""
        try:
            from detector import BlueButtonDetector

            detector = BlueButtonDetector(debug_mode=False)
            self.assertIsInstance(detector, BlueButtonDetector)
            self.assertEqual(detector.debug_mode, False)
            self.assertEqual(detector.detection_count, 0)
        except ImportError as e:
            self.fail(f"Erro ao importar detector: {e}")

    def test_detector_statistics(self):
        """Testa sistema de estatísticas do detector"""
        try:
            from detector import BlueButtonDetector

            detector = BlueButtonDetector()

            stats = detector.get_statistics()
            self.assertIsInstance(stats, dict)
            self.assertIn("total_detections", stats)
            self.assertIn("successful_detections", stats)
            self.assertIn("success_rate", stats)

            # Testar reset
            detector.reset_statistics()
            self.assertEqual(detector.detection_count, 0)
            self.assertEqual(detector.successful_detections, 0)
        except ImportError as e:
            self.fail(f"Erro ao importar detector: {e}")


class TestMonitor(unittest.TestCase):
    """Testes para o gerenciador de monitoramento"""

    def test_monitor_initialization(self):
        """Testa inicialização do monitor"""
        try:
            from monitor import MonitoringManager

            monitor = MonitoringManager()
            self.assertIsInstance(monitor, MonitoringManager)
            self.assertEqual(monitor.is_monitoring, False)
            self.assertEqual(monitor.click_count, 0)
        except ImportError as e:
            self.fail(f"Erro ao importar monitor: {e}")

    def test_monitor_configuration(self):
        """Testa configuração do monitor"""
        try:
            from monitor import MonitoringManager

            monitor = MonitoringManager()

            # Testar atualização de intervalo
            monitor.update_interval(1.5)
            self.assertEqual(monitor.monitor_interval, 1.5)

            # Testar limites
            monitor.update_interval(0.05)  # Muito baixo
            self.assertGreaterEqual(monitor.monitor_interval, 0.1)

            monitor.update_interval(10.0)  # Muito alto
            self.assertLessEqual(monitor.monitor_interval, 5.0)
        except ImportError as e:
            self.fail(f"Erro ao importar monitor: {e}")


class TestUI(unittest.TestCase):
    """Testes para a interface gráfica"""

    @patch("tkinter.Tk")
    def test_ui_initialization(self, mock_tk):
        """Testa inicialização da UI"""
        try:
            import tkinter as tk

            from ui import ModernUI

            # Mock do root
            mock_root = Mock()
            mock_tk.return_value = mock_root

            ui = ModernUI(mock_root)
            self.assertIsInstance(ui, ModernUI)
            self.assertEqual(ui.root, mock_root)
        except ImportError as e:
            self.fail(f"Erro ao importar UI: {e}")


class TestUtils(unittest.TestCase):
    """Testes para utilitários"""

    def test_performance_profiler(self):
        """Testa o profiler de performance"""
        try:
            import time

            from utils import PerformanceProfiler

            profiler = PerformanceProfiler()

            # Testar timer
            profiler.start_timer("test_operation")
            time.sleep(0.01)  # 10ms
            elapsed = profiler.end_timer("test_operation")

            self.assertIsNotNone(elapsed)
            self.assertGreater(elapsed, 0.008)  # Pelo menos 8ms

            # Testar estatísticas
            stats = profiler.get_statistics("test_operation")
            self.assertIn("min", stats)
            self.assertIn("max", stats)
            self.assertIn("avg", stats)
            self.assertIn("count", stats)
            self.assertEqual(stats["count"], 1)
        except ImportError as e:
            self.fail(f"Erro ao importar utils: {e}")

    def test_config_manager(self):
        """Testa o gerenciador de configurações"""
        try:
            import os
            import tempfile

            from utils import ConfigManager

            # Usar arquivo temporário
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                temp_file = f.name

            try:
                config = ConfigManager(temp_file)

                # Testar set/get
                config.set("test_key", "test_value")
                self.assertEqual(config.get("test_key"), "test_value")

                # Testar valor padrão
                self.assertEqual(config.get("nonexistent", "default"), "default")

                # Testar save/load
                self.assertTrue(config.save_config())

                # Criar nova instância e verificar persistência
                config2 = ConfigManager(temp_file)
                self.assertEqual(config2.get("test_key"), "test_value")

            finally:
                # Limpar arquivo temporário
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

        except ImportError as e:
            self.fail(f"Erro ao importar utils: {e}")

    def test_format_time(self):
        """Testa formatação de tempo"""
        try:
            from utils import format_time

            # Testar diferentes intervalos
            self.assertEqual(format_time(30), "30.0s")
            self.assertEqual(format_time(90), "1m 30s")
            self.assertEqual(format_time(3661), "1h 1m 1s")
        except ImportError as e:
            self.fail(f"Erro ao importar utils: {e}")


class TestIntegration(unittest.TestCase):
    """Testes de integração"""

    def test_full_import_chain(self):
        """Testa se toda a cadeia de importações funciona"""
        try:
            # Importar módulo principal
            from app import AutoClickerPro

            # Verificar se consegue importar todos os componentes necessários
            self.assertTrue(hasattr(AutoClickerPro, "__init__"))

        except ImportError as e:
            self.fail(f"Erro na cadeia de importações: {e}")

    @patch("tkinter.Tk")
    def test_app_initialization(self, mock_tk):
        """Testa inicialização completa da aplicação"""
        try:
            from app import AutoClickerPro

            # Mock do Tkinter
            mock_root = Mock()
            mock_tk.return_value = mock_root

            # Tentar criar aplicação
            app = AutoClickerPro()
            self.assertIsInstance(app, AutoClickerPro)

        except Exception as e:
            self.fail(f"Erro ao inicializar aplicação: {e}")


if __name__ == "__main__":
    # Configurar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adicionar todos os testes
    suite.addTest(loader.loadTestsFromTestCase(TestConfig))
    suite.addTest(loader.loadTestsFromTestCase(TestDetector))
    suite.addTest(loader.loadTestsFromTestCase(TestMonitor))
    suite.addTest(loader.loadTestsFromTestCase(TestUI))
    suite.addTest(loader.loadTestsFromTestCase(TestUtils))
    suite.addTest(loader.loadTestsFromTestCase(TestIntegration))

    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Relatório final
    print(f"\n{'='*50}")
    print(f"Testes executados: {result.testsRun}")
    print(f"Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Falhas: {len(result.failures)}")
    print(f"Erros: {len(result.errors)}")
    print(f"{'='*50}")

    # Exit code baseado no resultado
    exit_code = 0 if result.wasSuccessful() else 1
    sys.exit(exit_code)
