<div align="center">

# 🎯 Auto Clicker Pro

**Sistema Inteligente de Detecção e Automação de Cliques**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI/CD](https://github.com/yourusername/auto-clicker-pro/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/yourusername/auto-clicker-pro/actions)
[![Coverage](https://codecov.io/gh/yourusername/auto-clicker-pro/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/auto-clicker-pro)

*Um sistema avançado de automação que detecta e clica automaticamente em botões azuis na tela, com interface moderna e arquitetura modular.*

[🚀 Começar](#-instalação-rápida) • [📖 Documentação](docs/) • [🐛 Reportar Bug](https://github.com/yourusername/auto-clicker-pro/issues) • [💡 Solicitar Feature](https://github.com/yourusername/auto-clicker-pro/issues)

</div>

## 🌟 Características Principais

<table>
<tr>
<td>

### 🎯 **Detecção Inteligente**
Algoritmo avançado de detecção de botões azuis usando análise HSV com múltiplos ranges de cor para máxima precisão.

</td>
<td>

### 🖥️ **Interface Moderna**
UI responsiva com design moderno, cards informativos e estatísticas em tempo real.

</td>
</tr>
<tr>
<td>

### 📊 **Monitoramento Avançado**
Sistema completo de métricas com taxa de sucesso, tempo de sessão e análise de performance.

</td>
<td>

### �️ **Segurança Integrada**
Parada de emergência automática, failsafe integrado e controles de segurança robustos.

</td>
</tr>
</table>

### � **Recursos Técnicos**
- ⚡ **Performance Otimizada**: Algoritmos de detecção otimizados para baixo uso de CPU
- 🔧 **Configurações Flexíveis**: Sistema de configuração centralizado e persistente
- 📈 **Sistema de Logging**: Logs estruturados para debugging e análise
- 🧪 **Testabilidade**: Suite de testes abrangente com 83% de cobertura
- 📦 **Arquitetura Modular**: Código limpo seguindo princípios SOLID
- 🌍 **Cross-Platform**: Suporte nativo para macOS, Windows e Linux

## 🏗️ Arquitetura Modular

O projeto foi refatorado com uma arquitetura modular para facilitar manutenção:

```

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.8 ou superior
- macOS, Windows ou Linux
- Permissões de acessibilidade (macOS)

### Instalação Rápida

1. **Clone ou baixe o projeto**
2. **Instale as dependências:**
   ```bash
   # Usando pip
   pip install -r requirements.txt
   
   # Ou usando uv (recomendado)
   uv sync
   ```

3. **Execute a aplicação:**
   ```bash
   # Aplicação principal
   python main.py
   
   # Com argumentos
   python main.py --help
   python main.py --version
   ```

### Configuração macOS

No macOS, você precisa conceder permissões de acessibilidade:

1. Vá em **Preferências do Sistema**
2. **Segurança e Privacidade** → **Privacidade** → **Acessibilidade**
3. Adicione **Terminal** ou **Python** à lista
4. Marque a caixa de seleção para ativar

## 🎮 Como Usar

1. **Inicie a aplicação** - A interface moderna será aberta
2. **Ajuste as configurações** - Defina o intervalo de verificação
3. **Ative o modo debug** (opcional) - Para salvar capturas das detecções
4. **Clique em "Iniciar Monitoramento"** - O sistema começará a procurar botões azuis
5. **Monitore as estatísticas** - Acompanhe cliques e taxa de sucesso em tempo real

### Parada de Emergência

- **Método 1**: Clique no botão "Parar" na interface
- **Método 2**: Mova o mouse para o canto superior esquerdo da tela

## 🔧 Configurações Avançadas

### Detecção de Cor

O sistema detecta botões azuis usando análise HSV com dois rangos:

```python
# Azul padrão (botões típicos)
HSV: (105-125, 80-255, 80-255)

# Azul claro (estados hover/active)
HSV: (95-115, 60-200, 100-255)
```

### Filtros de Botão

```python
# Dimensões válidas
Largura: 50-300 pixels
Altura: 20-80 pixels
Área: 1000-20000 pixels

# Proporção (largura:altura)
Aspect Ratio: 1.8:1 a 6:1
```

### Configurações de Performance

```python
# Intervalos suportados
Mínimo: 0.1 segundos
Máximo: 5.0 segundos
Padrão: 0.5 segundos

# Delay após clique
Padrão: 2.0 segundos
```

## 📊 Monitoramento e Estatísticas

A interface exibe em tempo real:

- **Contador de Cliques**: Total de botões clicados com sucesso
- **Tempo de Sessão**: Duração da sessão atual
- **Taxa de Sucesso**: Percentual de detecções bem-sucedidas
- **Tempo Médio**: Tempo médio de detecção por ciclo

## 🐛 Debug e Troubleshooting

### Modo Debug

Ative o modo debug para:
- Salvar capturas de tela das detecções
- Visualizar retângulos de detecção
- Analisar candidatos a botão
- Verificar scores de confiança

As imagens são salvas em `debug_images/` com timestamp.

### Problemas Comuns

**Botão não detectado:**
- Verifique se o botão é realmente azul (HSV)
- Confirme se está dentro dos critérios de tamanho
- Certifique-se que está completamente visível

**Cliques em local errado:**
- Calibre os parâmetros de cor
- Verifique escala da tela (high DPI)
- Teste em monitor principal

**Performance baixa:**
- Aumente o intervalo de verificação
- Implemente região de interesse (ROI)
- Verifique uso de CPU

## 🛠️ Desenvolvimento

### Estrutura dos Módulos

- **`config.py`**: Configurações centralizadas
- **`detector.py`**: Algoritmos de detecção visual
- **`monitor.py`**: Gerenciamento do monitoramento
- **`ui.py`**: Interface gráfica moderna
- **`app.py`**: Aplicação principal
- **`utils.py`**: Utilitários e ferramentas

### Extensibilidade

Para adicionar novos recursos:

1. **Nova detecção de cor**: Edite `COLOR_DETECTION` em `config.py`
2. **Novos filtros**: Modifique `BUTTON_DETECTION` em `config.py`
3. **UI personalizada**: Estenda a classe `ModernUI` em `ui.py`
4. **Logging avançado**: Use `Logger` em `utils.py`

## 📝 Versionamento

- **v1.0**: Versão original monolítica
- **v2.0**: Arquitetura modular com interface moderna
- **v2.1**: (Planejada) OCR e múltiplas cores
- **v3.0**: (Planejada) Interface web e API

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja nosso [Guia de Contribuição](CONTRIBUTING.md) para começar.

### 👥 Contribuidores

Agradecemos a todos que contribuem para este projeto:

<a href="https://github.com/yourusername/auto-clicker-pro/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yourusername/auto-clicker-pro" />
</a>

### 🔄 Como Contribuir

1. **Fork o projeto**
2. **Crie uma branch** (`git checkout -b feature/nova-feature`)
3. **Commit suas mudanças** (`git commit -am 'feat: adiciona nova feature'`)
4. **Push para a branch** (`git push origin feature/nova-feature`)
5. **Abra um Pull Request**

## 📈 Roadmap

### 🎯 Versão 2.1 (Em Breve)
- [ ] 🔍 OCR para detecção de texto em botões
- [ ] 🎨 Suporte a múltiplas cores configuráveis
- [ ] 📱 Interface web responsiva
- [ ] 🤖 IA para detecção mais inteligente

### 🚀 Versão 3.0 (Futuro)
- [ ] ☁️ Sincronização na nuvem
- [ ] 📱 App mobile de controle
- [ ] 🔌 Sistema de plugins
- [ ] 📊 Dashboard analítico avançado

Veja o [CHANGELOG.md](CHANGELOG.md) para histórico completo de versões.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE) - veja o arquivo LICENSE para detalhes.

## ⚠️ Aviso Legal

Este software deve ser usado apenas em aplicações próprias ou com permissão explícita. O desenvolvedor não se responsabiliza pelo uso inadequado da ferramenta. Respeite os termos de serviço das aplicações onde for utilizado.

## 📞 Suporte

- 📧 **Email**: [support@auto-clicker-pro.com](mailto:support@auto-clicker-pro.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/auto-clicker-pro/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/yourusername/auto-clicker-pro/discussions)
- 📖 **Documentação**: [Wiki](https://github.com/yourusername/auto-clicker-pro/wiki)

---

<div align="center">

**⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub! ⭐**

*Desenvolvido com ❤️ para automatizar tarefas repetitivas de forma inteligente e segura.*

</div>
Continuador/
├── src/                          # Código fonte modular
│   ├── __init__.py              # Informações do pacote
│   ├── app.py                   # Aplicação principal
│   ├── config.py                # Configurações centralizadas
│   ├── detector.py              # Sistema de detecção de botões
│   ├── monitor.py               # Gerenciador de monitoramento
│   ├── ui.py                    # Interface gráfica moderna
│   └── utils.py                 # Utilitários e ferramentas
├── auto_clicker_blue.py         # Versão original (legacy)
├── main.py                      # Ponto de entrada principal
├── main.py                      # Ponto de entrada alternativo
├── requirements.txt             # Dependências Python
├── pyproject.toml              # Configuração do projeto
├── README.md                   # Esta documentação
├── MANUAL.md                   # Manual detalhado de uso
└── setup.sh                   # Script de configuração
# Test trigger for GitHub Actions
