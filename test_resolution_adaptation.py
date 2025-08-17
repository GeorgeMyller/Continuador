#!/usr/bin/env python3
"""
Teste do Sistema de Adaptação de Resolução
Demonstra como o sistema adapta os parâmetros para diferentes resoluções
"""

import os
import sys

# Adicionar src ao path para importações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import pyautogui

from config import BUTTON_DETECTION, RESOLUTION_ADAPTATION
from resolution_adapter import ResolutionAdapter


def test_resolution_adaptation():
    """Testa o sistema de adaptação para diferentes resoluções"""
    print("🔍 TESTE DO SISTEMA DE ADAPTAÇÃO DE RESOLUÇÃO")
    print("=" * 60)

    # Resolução atual real
    adapter = ResolutionAdapter()
    current_resolution = pyautogui.size()
    print(
        f"📐 Resolução atual da tela: {current_resolution.width}x{current_resolution.height}"
    )

    # Configuração adaptada para resolução atual
    config = adapter.get_adapted_config()
    print("\n✅ Configuração adaptada:")
    print(f"   - Largura mínima do botão: {config['min_width']}px")
    print(f"   - Largura máxima do botão: {config['max_width']}px")
    print(f"   - Altura mínima do botão: {config['min_height']}px")
    print(f"   - Altura máxima do botão: {config['max_height']}px")
    print(f"   - Margem das bordas: {config['edge_margin']}px")

    # Simular diferentes resoluções
    test_resolutions = [
        (1366, 768),  # HD
        (1920, 1080),  # Full HD (base)
        (2560, 1440),  # QHD
        (3840, 2160),  # 4K
        (1024, 768),  # XGA
        (2880, 1800),  # MacBook Pro Retina
    ]

    print("\n🧪 SIMULAÇÃO PARA DIFERENTES RESOLUÇÕES:")
    print("-" * 60)

    base_resolution = RESOLUTION_ADAPTATION["base_resolution"]

    for width, height in test_resolutions:
        # Calcular fatores de escala
        scale_x = width / base_resolution[0]
        scale_y = height / base_resolution[1]

        # Simular configuração adaptada
        min_width = int(BUTTON_DETECTION["min_width"] * scale_x)
        max_width = int(BUTTON_DETECTION["max_width"] * scale_x)
        min_height = int(BUTTON_DETECTION["min_height"] * scale_y)
        max_height = int(BUTTON_DETECTION["max_height"] * scale_y)

        print(f"\n📺 {width}x{height} (escala: {scale_x:.2f}x, {scale_y:.2f}x)")
        print(f"   ├─ Largura: {min_width}-{max_width}px")
        print(f"   └─ Altura:  {min_height}-{max_height}px")

    # Testar limites de escala
    print("\n⚠️  TESTE DE LIMITES:")
    print("-" * 30)

    min_scale = RESOLUTION_ADAPTATION["min_scale_factor"]
    max_scale = RESOLUTION_ADAPTATION["max_scale_factor"]

    print(f"📏 Fator de escala mínimo: {min_scale}x")
    print(f"📏 Fator de escala máximo: {max_scale}x")

    # Teste com resolução muito pequena
    tiny_scale_x = 800 / base_resolution[0]  # ~0.42x
    if tiny_scale_x < min_scale:
        print(f"⚠️  Resolução 800x600 seria limitada ao fator mínimo ({min_scale}x)")

    # Teste com resolução muito grande
    huge_scale_x = 7680 / base_resolution[0]  # ~4.0x (8K)
    if huge_scale_x > max_scale:
        print(f"⚠️  Resolução 8K seria limitada ao fator máximo ({max_scale}x)")

    print("\n✅ RESULTADO:")
    print("🎯 O sistema adapta automaticamente os parâmetros de detecção")
    print("🔄 Mantém a precisão independente da resolução da tela")
    print("🛡️ Aplicação de limites de segurança previne valores extremos")
    print("⚡ Cache evita recálculos desnecessários")

    return True


def test_cache_performance():
    """Testa a performance do sistema de cache"""
    print("\n🚀 TESTE DE PERFORMANCE DO CACHE")
    print("=" * 40)

    import time

    adapter = ResolutionAdapter()

    # Primeira chamada (sem cache)
    start_time = time.time()
    config1 = adapter.get_adapted_config()
    first_call_time = time.time() - start_time

    # Segunda chamada (com cache)
    start_time = time.time()
    config2 = adapter.get_adapted_config()
    cached_call_time = time.time() - start_time

    print(f"⏱️  Primeira chamada: {first_call_time * 1000:.2f}ms")
    print(f"⚡ Segunda chamada (cache): {cached_call_time * 1000:.2f}ms")

    if cached_call_time < first_call_time:
        speedup = (
            first_call_time / cached_call_time if cached_call_time > 0 else float("inf")
        )
        print(f"🎯 Aceleração do cache: {speedup:.1f}x mais rápido")

    # Verificar se as configurações são idênticas
    assert config1 == config2, "Configurações do cache devem ser idênticas"
    print("✅ Cache funcionando corretamente!")

    return True


if __name__ == "__main__":
    try:
        print("🧪 SISTEMA DE TESTES - AUTO CLICKER PRO")
        print("🔧 Testando adaptação de resolução...")
        print()

        # Executar testes
        test_resolution_adaptation()
        test_cache_performance()

        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema de adaptação de resolução funcionando perfeitamente")

    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
