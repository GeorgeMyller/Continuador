#!/usr/bin/env python3
"""
Auto Clicker Pro - Ponto de Entrada Principal
Sistema moderno de detecção e clique automático em botões azuis

Este arquivo mantém compatibilidade com a versão anterior enquanto
utiliza a nova arquitetura modular.
"""

import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.app import main, AutoClickerPro
    from src import __version__, __description__
    
    # Manter compatibilidade com imports antigos
    ModernAutoClickerBlue = AutoClickerPro
    
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


if __name__ == "__main__":
    try:
        # Verificar argumentos de linha de comando
        if len(sys.argv) > 1:
            if sys.argv[1] in ['--version', '-v']:
                show_version_info()
                sys.exit(0)
            elif sys.argv[1] in ['--help', '-h']:
                show_version_info()
                print("Uso: python auto_clicker_blue.py [opções]")
                print()
                print("Opções:")
                print("  -v, --version    Mostra a versão do programa")
                print("  -h, --help       Mostra esta mensagem de ajuda")
                print()
                print("Para usar o programa, execute sem argumentos para abrir a interface gráfica.")
                sys.exit(0)
        
        # Executar aplicação principal
        main()
        
    except KeyboardInterrupt:
        print("\n👋 Programa interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)
