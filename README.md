
# Macro de Rotação de Skills para Throne and Liberty

Este projeto implementa um macro de rotação de skills para o jogo Throne and Liberty, permitindo aos jogadores automatizar sequências de habilidades e personalizar suas rotações.

## Funcionalidades

- Execução automática de sequência de habilidades
- Modo de gravação para criar sequências personalizadas
- Configuração via arquivo JSON
- Simulação de uso para teste

## Requisitos

- Python 3.6+
- Bibliotecas: json, time

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/InovarBug/macrotl.git
   ```

2. Navegue até o diretório do projeto:
   ```
   cd macrotl
   ```

## Uso

1. Execute o script principal:
   ```
   python3 skill_rotation_macro.py
   ```

2. O script iniciará uma interface de linha de comando com as seguintes opções:
   - `iniciar`: Inicia a execução do macro com as habilidades atuais
   - `parar`: Interrompe a execução do macro
   - `gravar`: Inicia o modo de gravação para criar uma nova sequência de habilidades
   - `finalizar`: Finaliza o modo de gravação e salva a nova sequência
   - `sair`: Encerra o programa

3. Para gravar uma nova sequência de habilidades:
   a. Digite `gravar` para iniciar o modo de gravação
   b. Insira a tecla da habilidade (por exemplo, "3")
   c. Insira o tempo de recarga (cooldown) da habilidade em segundos (por exemplo, "1.5")
   d. Repita os passos b e c para cada habilidade que deseja adicionar à sequência
   e. Digite 'q' quando terminar de adicionar habilidades
   f. A nova sequência será salva automaticamente e estará pronta para uso

4. Para executar o macro com a nova sequência, digite `iniciar`

5. Para interromper a execução do macro, digite `parar`

6. Para encerrar o programa, digite `sair`

## Configuração

As configurações do macro são armazenadas no arquivo `config.json`. Você pode editar este arquivo para ajustar as habilidades e seus tempos de recarga.

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests ou abrir issues para sugerir melhorias ou reportar bugs.

## Licença

Este projeto está licenciado sob a MIT License.
