
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

2. O script iniciará uma simulação demonstrando as funcionalidades:
   - Exibição das habilidades atuais
   - Ativação do macro
   - Gravação de novas habilidades
   - Execução do macro com as novas habilidades

3. Para uso real, modifique o método `simulate_interactions()` na classe `SkillRotationMacro` para atender às suas necessidades específicas.

## Configuração

As configurações do macro são armazenadas no arquivo `config.json`. Você pode editar este arquivo para ajustar as habilidades e seus tempos de recarga.

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests ou abrir issues para sugerir melhorias ou reportar bugs.

## Licença

Este projeto está licenciado sob a MIT License.
