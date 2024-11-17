
# Skill Rotation Macro for Throne and Liberty (macrotl)

Este script fornece um macro de rotação de habilidades personalizável para o jogo Throne and Liberty, com uma interface gráfica amigável, suporte para múltiplos perfis, recurso de gravação, logging, hotkeys para troca de perfis e um sistema de aprendizado de IA avançado com perfis específicos para PVP e PVE.

## Características Principais

- Interface gráfica intuitiva com abas para diferentes funcionalidades
- Rotação de habilidades personalizável
- Suporte a múltiplos perfis
- Modo de gravação para fácil criação de sequências de habilidades
- Sistema de aprendizado de IA avançado para PVP e PVE
- Visualização em tempo real da rotação de habilidades
- Detecção automática de modo PVP/PVE (experimental)
- Logging detalhado para depuração e monitoramento

## Instalação

1. Certifique-se de ter Python 3.7+ instalado em seu sistema.
2. Clone este repositório ou baixe os arquivos.
3. Instale as dependências:
   ```
   pip install pynput pyautogui opencv-python pillow numpy
   ```

## Uso

1. Execute o script:
   ```
   python skill_rotation_macro.py
   ```
2. Use a interface gráfica para:
   - Gerenciar perfis na aba "Profiles"
   - Configurar as opções de IA na aba "AI Settings"
   - Gravar sequências de habilidades na aba "Recording"
   - Visualizar a rotação de habilidades na aba "Visualization"

## Interface Gráfica

A nova interface gráfica inclui as seguintes abas:

1. **Profiles**: Gerencie seus perfis de rotação de habilidades e configure teclas de ativação.
2. **AI Settings**: Ajuste as configurações de IA para PVP e PVE, incluindo agressividade e defesa.
3. **Recording**: Grave novas sequências de habilidades para seus perfis.
4. **Visualization**: Visualize em tempo real a rotação de habilidades executada pela IA.

## Sistema de IA Avançado

O sistema de IA utiliza um algoritmo refinado para a rotação de habilidades, considerando:
- Frequência de uso de cada habilidade
- Tempo desde o último uso de cada habilidade
- Prioridade definida para cada habilidade
- Configurações de agressividade e defesa do perfil atual

## Detecção Automática de PVP/PVE

A funcionalidade de detecção automática usa processamento de imagem para tentar identificar se você está em modo PVP ou PVE. Esta é uma funcionalidade experimental e pode não ser 100% precisa.

## Logging

O script cria um arquivo `macro_log.txt` no mesmo diretório, que registra vários eventos, ações e erros para fins de depuração e monitoramento.

## Desenvolvimento

Para informações sobre como configurar o ambiente de desenvolvimento usando PyCharm, consulte o arquivo `pycharm_instructions.md`.

## Testes

O projeto inclui um conjunto de testes unitários. Para executar os testes:

```
python comprehensive_test.py
```

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests ou abrir issues para reportar bugs ou sugerir novas funcionalidades.

## Aviso Legal

Use macros de forma responsável e de acordo com os termos de serviço do jogo. O recurso de IA é experimental e pode não replicar perfeitamente a jogabilidade humana.
