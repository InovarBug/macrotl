# Macro de Rotação de Habilidades

Este projeto implementa um macro para rotação de habilidades em jogos, com suporte para cooldowns e logging.

## Funcionalidades

- Simulação de uso de habilidades com cooldowns
- Logging detalhado das ações do macro
- Suporte para múltiplos perfis de habilidades
- Modo AI para PVE e PVP (em desenvolvimento)
- Interface gráfica usando Tkinter

## Como usar

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o script de teste: `python test_macro.py`
4. Para a interface gráfica, execute: `python gui.py`

## Configuração do PyCharm

Para configurar este projeto no PyCharm:

1. Abra o PyCharm e selecione "Open"
2. Navegue até o diretório do projeto e selecione-o
3. Vá para File > Settings > Project: [Nome do Projeto] > Python Interpreter
4. Clique na engrenagem e selecione "Add"
5. Escolha "Virtual Environment" e crie um novo ambiente virtual
6. Instale as dependências usando o terminal do PyCharm: `pip install -r requirements.txt`

### Instalando Tkinter

Se você estiver usando Windows ou macOS, o Tkinter geralmente já vem instalado com o Python. Para Linux, siga estas etapas:

1. Abra o terminal no PyCharm (View > Tool Windows > Terminal)
2. Execute o seguinte comando:
   ```
   sudo apt-get update
   sudo apt-get install python3-tk
   ```
3. Reinicie o PyCharm após a instalação

## Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue para discutir mudanças maiores antes de submeter um pull request.

## Licença

Este projeto está licenciado sob a licença MIT.
