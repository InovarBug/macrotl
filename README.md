
# Skill Rotation Macro for Throne and Liberty (macrotl)

Este script fornece um macro de rotação de habilidades personalizável para o jogo Throne and Liberty, com suporte para múltiplos perfis, recurso de gravação, logging, hotkeys para troca de perfis, interface gráfica do usuário e um sistema de aprendizado de IA avançado com perfis específicos para PVP e PVE.

## Instalação

1. Certifique-se de ter Python 3.7+ instalado em seu sistema.
2. Instale as bibliotecas necessárias:
   ```
   pip install pynput pyautogui opencv-python pillow numpy
   ```
3. Clone este repositório ou baixe os arquivos `skill_rotation_macro.py` e `config.json`.

## Uso

1. Execute o script:
   ```
   python skill_rotation_macro.py
   ```
2. Use a interface gráfica para:
   - Alternar entre perfis
   - Definir teclas de ativação
   - Gravar sequências de habilidades
   - Iniciar e parar o macro
   - Ajustar cooldowns dinamicamente
   - Iniciar e parar o aprendizado da IA
   - Iniciar o macro controlado pela IA
   - Selecionar manualmente o modo PVP ou PVE
   - Ativar/desativar a detecção automática de PVP/PVE
   - Configurar as opções avançadas de IA
   - Exportar e importar perfis de IA

## Recursos

- Rotação de habilidades personalizável
- Suporte a múltiplos perfis
- Modo de gravação para fácil criação de sequências de habilidades
- Tecla de ativação e cooldowns de habilidades configuráveis
- Ajuste dinâmico de cooldown
- Sistema de logging para depuração e rastreamento de uso
- Interface gráfica do usuário para fácil configuração e controle
- Sistema de aprendizado de IA avançado:
  - Aprende padrões de rotação de habilidades a partir da jogabilidade do usuário
  - Pode executar padrões aprendidos automaticamente
  - Perfis separados para PVP e PVE
  - Algoritmo de rotação baseado em frequência, tempo desde o último uso e prioridade da habilidade
  - Configurações ajustáveis de agressividade e defesa
- Seleção manual de modo PVP/PVE
- Detecção automática de modo PVP/PVE (experimental)
- Tratamento de erros robusto
- Exportação e importação de perfis de IA treinados

## Sistema de IA Avançado

O sistema de IA utiliza um algoritmo refinado para a rotação de habilidades, considerando:
- Frequência de uso de cada habilidade
- Tempo desde o último uso de cada habilidade
- Prioridade definida para cada habilidade
- Configurações de agressividade e defesa do perfil atual

## Testes

O projeto inclui um conjunto de testes unitários para garantir o funcionamento correto das principais funcionalidades. Para executar os testes:

```
python comprehensive_test.py
```

Note que alguns testes podem requerer um ambiente gráfico simulado (como Xvfb) para funcionar corretamente em ambientes sem interface gráfica.

## Logging

O script cria um arquivo `macro_log.txt` no mesmo diretório, que registra vários eventos, ações e erros para fins de depuração e monitoramento.

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests ou abrir issues para reportar bugs ou sugerir novas funcionalidades.

## Aviso Legal

Use macros de forma responsável e de acordo com os termos de serviço do jogo. O recurso de IA é experimental e pode não replicar perfeitamente a jogabilidade humana.
