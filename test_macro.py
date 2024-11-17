
import json
from skill_rotation_macro import SkillRotationMacro

def test_macro():
    # Criar instância do macro
    macro = SkillRotationMacro()

    # Teste 1: Criar perfis
    print("Teste 1: Criando perfis")
    macro.create_profile("perfil1")
    macro.create_profile("perfil2")

    # Teste 2: Listar perfis
    print("\nTeste 2: Listando perfis")
    macro.list_profiles()

    # Teste 3: Gravar habilidades para perfil1
    print("\nTeste 3: Gravando habilidades para perfil1")
    macro.select_profile("perfil1")
    macro.start_recording()
    macro.record_skill("Q", 1.5)
    macro.record_skill("W", 2.0)
    macro.record_skill("E", 3.0)
    macro.stop_recording()

    # Teste 4: Gravar habilidades para perfil2
    print("\nTeste 4: Gravando habilidades para perfil2")
    macro.select_profile("perfil2")
    macro.start_recording()
    macro.record_skill("R", 5.0)
    macro.record_skill("T", 4.0)
    macro.stop_recording()

    # Teste 5: Executar macro com perfil1
    print("\nTeste 5: Executando macro com perfil1")
    macro.select_profile("perfil1")
    macro.toggle_macro()
    macro.run_macro()
    macro.toggle_macro()

    # Teste 6: Executar macro com perfil2
    print("\nTeste 6: Executando macro com perfil2")
    macro.select_profile("perfil2")
    macro.toggle_macro()
    macro.run_macro()
    macro.toggle_macro()

    # Teste 7: Excluir perfil
    print("\nTeste 7: Excluindo perfil")
    macro.delete_profile("perfil2")
    macro.list_profiles()

    print("\nTestes concluídos.")

if __name__ == "__main__":
    test_macro()
