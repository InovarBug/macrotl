# Instruções para Configurar o Projeto no PyCharm

Este guia irá ajudá-lo a configurar o projeto Macro de Rotação de Habilidades no PyCharm.

## Passo 1: Clonar o Repositório

1. Abra o PyCharm
2. Vá para `VCS > Get from Version Control`
3. Cole a URL do repositório: `https://github.com/InovarBug/macrotl.git`
4. Escolha um diretório local para o projeto
5. Clique em "Clone"

## Passo 2: Configurar o Ambiente Virtual

1. Vá para `File > Settings` (no Windows/Linux) ou `PyCharm > Preferences` (no macOS)
2. Navegue até `Project: macrotl > Python Interpreter`
3. Clique na engrenagem ao lado do campo do interpretador e selecione "Add"
4. Escolha "Virtual Environment" e selecione "New environment"
5. Escolha a localização para o ambiente virtual (geralmente dentro da pasta do projeto)
6. Selecione a versão do Python (recomendamos Python 3.8 ou superior)
7. Clique em "OK" para criar o ambiente virtual

## Passo 3: Instalar Dependências

1. Abra o terminal integrado do PyCharm (View > Tool Windows > Terminal)
2. Certifique-se de que o ambiente virtual está ativado (você deve ver (venv) no início da linha de comando)
3. Execute o seguinte comando:
   ```
   pip install -r requirements.txt
   ```

## Passo 4: Instalar Tkinter (se necessário)

Se você estiver usando Windows ou macOS, o Tkinter geralmente já vem instalado com o Python. Para Linux, siga estas etapas:

1. No terminal integrado do PyCharm, execute:
   ```
   sudo apt-get update
   sudo apt-get install python3-tk
   ```
2. Reinicie o PyCharm após a instalação

## Passo 5: Configurar o Script de Execução

1. Vá para `Run > Edit Configurations`
2. Clique no "+" e selecione "Python"
3. Dê um nome à configuração (por exemplo, "Run GUI")
4. No campo "Script path", selecione o arquivo `gui.py`
5. Certifique-se de que o interpretador Python selecionado é o do seu ambiente virtual
6. Clique em "Apply" e depois em "OK"

## Passo 6: Executar o Projeto

1. Selecione a configuração de execução que você criou no passo anterior
2. Clique no botão de play verde ou pressione Shift+F10 para executar o projeto

Agora você deve ver a interface gráfica do Macro de Rotação de Habilidades em execução!

## Solução de Problemas

Se você encontrar algum erro relacionado a módulos faltantes, certifique-se de que todas as dependências foram instaladas corretamente executando novamente o comando pip install -r requirements.txt no terminal do PyCharm.

Se persistirem problemas com o Tkinter no Linux, você pode precisar reinstalar o Python com suporte ao Tkinter. Consulte a documentação da sua distribuição Linux para obter instruções específicas.
