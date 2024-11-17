# Instruções para Executar o Programa usando PyCharm

Este guia fornecerá instruções passo a passo sobre como configurar e executar o projeto Skill Rotation Macro for Throne and Liberty usando o PyCharm, focando na interface gráfica.

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
   - Execute o comando: `pip install PySimpleGUI keyboard`

5. Configure a execução da interface gráfica:
   - Clique com o botão direito em "gui.py" no navegador de projetos
   - Selecione "Run 'gui'"

6. Execute o programa:
   - Clique no botão de play verde no canto superior direito ou use o atalho Shift+F10
   - A interface gráfica do macro será iniciada

7. Usar o programa via interface gráfica:
   - Use os botões e campos da interface para controlar o macro, criar perfis e gravar sequências de habilidades

## Notas Adicionais

- Certifique-se de que todas as dependências estejam instaladas corretamente.
- Se encontrar problemas com bibliotecas gráficas em um ambiente sem interface gráfica, considere usar Xvfb para simular um display.
- Para desenvolvimento contínuo, use o controle de versão integrado do PyCharm para fazer commits e push das suas alterações.
- Ao usar o modo de gravação, pressione as teclas das habilidades na ordem desejada.
- Em alguns sistemas operacionais, pode ser necessário executar o programa com privilégios de administrador devido ao uso da biblioteca keyboard.

## Solução de Problemas

- Se encontrar erros relacionados a módulos não encontrados, verifique se todas as dependências foram instaladas corretamente no ambiente virtual.
- Para problemas específicos do PyCharm, consulte a [documentação oficial do PyCharm](https://www.jetbrains.com/help/pycharm/quick-start-guide.html).
- Se o macro não funcionar corretamente no jogo, verifique se as teclas configuradas correspondem às teclas de habilidade no jogo.

Lembre-se de sempre testar o programa em um ambiente seguro antes de usá-lo no jogo real.
