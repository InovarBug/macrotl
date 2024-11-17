import time
from skill_rotation_macro import SkillRotationMacro

def test_macro():
    # Criar instância do macro
    macro = SkillRotationMacro()

    # Configurar algumas habilidades de teste
    macro.skills = [
        {'key': 'Q', 'cooldown': 5},
        {'key': 'W', 'cooldown': 8},
        {'key': 'E', 'cooldown': 12}
    ]

    print("Teste 1: Iniciando o macro")
    macro.toggle_macro()  # Ativar o macro

    print("Executando o macro por 30 segundos...")
    time.sleep(30)

    print("Teste 2: Parando o macro")
    macro.toggle_macro()  # Desativar o macro

    print("Teste concluído.")
    print("Verifique o arquivo 'macro_log.txt' para ver os logs de execução.")

if __name__ == "__main__":
    test_macro()
