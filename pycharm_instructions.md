
# Instruções para Gerar o Programa usando PyCharm

Este guia fornecerá instruções passo a passo sobre como configurar e executar o projeto Skill Rotation Macro for Throne and Liberty usando o PyCharm.

## Pré-requisitos

1. Instale o PyCharm Community Edition ou Professional (https://www.jetbrains.com/pycharm/download/)
2. Instale o Python 3.7 ou superior (https://www.python.org/downloads/)
3. Certifique-se de ter o Git instalado (https://git-scm.com/downloads)

## Passos

1. Abra o PyCharm

2. Clone o repositório:
   - Vá para "File" > "New" > "Project from Version Control"
   - URL: https://github.com/InovarBug/macrotl.git
   - Escolha um diretório para o projeto e clique em "Clone"

3. Configure o ambiente virtual:
   - Vá para "File" > "Settings" (Windows/Linux) ou "PyCharm" > "Preferences" (macOS)
   - Navegue até "Project: macrotl" > "Python Interpreter"
   - Clique na engrenagem > "Add"
   - Selecione "Virtual Environment" > "New environment"
   - Certifique-se de que o Python 3.7+ esteja selecionado
   - Clique em "OK" para criar o ambiente virtual

4. Instale as dependências:
   - Abra um terminal no PyCharm (View > Tool Windows > Terminal)
   - Execute o comando: `pip install pynput pyautogui opencv-python pillow numpy`

5. Configure a execução do script:
   - Clique com o botão direito em "skill_rotation_macro.py" no navegador de projetos
   - Selecione "Run 'skill_rotation_macro'"

6. Execute o programa:
   - Clique no botão de play verde no canto superior direito ou use o atalho Shift+F10

7. Para executar os testes:
   - Clique com o botão direito em "comprehensive_test.py" no navegador de projetos
   - Selecione "Run 'Unittests in comprehensive_test'"

## Notas Adicionais

- Certifique-se de que todas as dependências estejam instaladas corretamente.
- Se encontrar problemas com bibliotecas gráficas em um ambiente sem interface gráfica, considere usar Xvfb para simular um display.
- Para desenvolvimento contínuo, use o controle de versão integrado do PyCharm para fazer commits e push das suas alterações.

## Solução de Problemas

- Se encontrar erros relacionados a módulos não encontrados, verifique se todas as dependências foram instaladas corretamente no ambiente virtual.
- Para problemas específicos do PyCharm, consulte a [documentação oficial do PyCharm](https://www.jetbrains.com/help/pycharm/quick-start-guide.html).

Lembre-se de sempre testar o programa em um ambiente seguro antes de usá-lo no jogo real.
