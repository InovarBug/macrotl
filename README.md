
# Skill Rotation Macro for Throne and Liberty (macrotl)

Este script fornece um macro de rotação de habilidades personalizável para o jogo Throne and Liberty, com suporte para múltiplos perfis, recurso de gravação, logging, hotkeys para troca de perfis, interface gráfica do usuário e um sistema de aprendizado de IA avançado com perfis específicos para PVP e PVE.

## Instalação

1. Certifique-se de ter Python 3.7+ instalado em seu sistema.
2. Instale as bibliotecas necessárias:
   ```
   pip install pynput pyautogui opencv-python pillow numpy
   ```
3. Baixe `skill_rotation_macro.py` e `config.json` para o mesmo diretório.

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

## Sistema de IA Avançado

O sistema de IA utiliza um algoritmo refinado para a rotação de habilidades:

1. Durante o aprendizado, a IA registra:
   - A frequência de uso de cada habilidade
   - O tempo desde o último uso de cada habilidade
   - O cooldown mínimo observado para cada habilidade

2. Durante a execução, a IA seleciona a próxima habilidade baseada em:
   - A disponibilidade da habilidade (respeitando o cooldown)
   - Um peso calculado considerando a frequência de uso, o tempo desde o último uso e a prioridade da habilidade
   - As configurações de agressividade e defesa do perfil atual

3. Configurações personalizáveis:
   - Agressividade: Aumenta a probabilidade de usar habilidades ofensivas
   - Defesa: Aumenta a probabilidade de usar habilidades defensivas
   - Prioridade de habilidades: Permite definir a importância relativa de cada habilidade

Este sistema resulta em uma rotação de habilidades mais dinâmica e adaptável, que tenta imitar mais de perto o estilo de jogo do usuário, enquanto permite ajustes finos para diferentes situações de jogo.

## Aprendizado de IA

1. Selecione o perfil de IA desejado (PVP ou PVE) na interface ou use os botões de seleção manual.
2. Clique em "Start AI Learning" e jogue normalmente.
3. A IA aprenderá seus padrões de rotação de habilidades para o perfil selecionado.
4. Clique em "Stop AI Learning" quando terminar.
5. Use o botão "AI Settings" para ajustar as configurações de agressividade, defesa e prioridades de habilidades.
6. Clique em "Start AI Macro" para deixar a IA executar os padrões aprendidos para o perfil atual.

## Detecção Automática de PVP/PVE

A funcionalidade de detecção automática usa processamento de imagem para tentar identificar se você está em modo PVP ou PVE. Esta é uma funcionalidade experimental e pode não ser 100% precisa. Use a seleção manual se preferir um controle mais preciso.

## Tratamento de Erros

O script inclui um sistema de tratamento de erros robusto:

- Erros são registrados em detalhes no arquivo de log (macro_log.txt).
- Mensagens de erro são exibidas na interface gráfica para informar o usuário sobre problemas.
- O script tenta lidar graciosamente com erros comuns, como arquivos de configuração ausentes ou mal formatados.
- Em caso de erro fatal, o script tenta salvar as configurações e fechar de forma segura.

## Logging

O script cria um arquivo `macro_log.txt` no mesmo diretório, que registra vários eventos, ações e erros para fins de depuração e monitoramento.

## Cuidado

Use macros de forma responsável e de acordo com os termos de serviço do jogo. O recurso de IA é experimental e pode não replicar perfeitamente a jogabilidade humana.
