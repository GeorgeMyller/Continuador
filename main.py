#!/usr/bin/env python3
"""
Auto Clicker Pro - Sistema de Detecção e Clique Automático
Sistema moderno de detecção e clique automático em botões azuis

Versão refatorada com arquitetura modular para facilitar manutenção.
"""

import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.app import main as app_main, AutoClickerPro
    from src import __version__, __description__
    
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("💡 Certifique-se de que todas as dependências estão instaladas:")
    print("   pip install -r requirements.txt")
    sys.exit(1)


def show_version_info():
    """Mostra informações de versão"""
    print(f"Auto Clicker Pro v{__version__}")
    print(__description__)
    print()


def main():
    """Função principal do programa"""
    try:
        # Verificar argumentos de linha de comando
        if len(sys.argv) > 1:
            if sys.argv[1] in ['--version', '-v']:
                show_version_info()
                return
            elif sys.argv[1] in ['--help', '-h']:
                show_version_info()
                print("Uso: python main.py [opções]")
                print()
                print("Opções:")
                print("  -v, --version    Mostra a versão do programa")
                print("  -h, --help       Mostra esta mensagem de ajuda")
                print()
                print("Para usar o programa, execute sem argumentos para abrir a interface gráfica.")
                return
        
        # Executar aplicação principal
        app_main()
        
    except KeyboardInterrupt:
        print("\n👋 Programa interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
