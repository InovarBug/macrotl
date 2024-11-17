
import time
import json

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.skills = []  # Lista de habilidades será carregada do arquivo de configuração
        self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
                current_profile = config.get('current_profile', 'default')
                profile = config.get('profiles', {}).get(current_profile, {})
                self.skills = profile.get('skills', [])
                if not self.skills:
                    print("Nenhuma habilidade encontrada no perfil atual. Usando configurações padrão.")
                    self.skills = [{"key": "1", "cooldown": 1.0}, {"key": "2", "cooldown": 2.0}]
        except FileNotFoundError:
            print("Arquivo de configuração não encontrado. Usando configurações padrão.")
            self.skills = [{"key": "1", "cooldown": 1.0}, {"key": "2", "cooldown": 2.0}]
        except json.JSONDecodeError:
            print("Erro ao ler o arquivo de configuração. Usando configurações padrão.")
            self.skills = [{"key": "1", "cooldown": 1.0}, {"key": "2", "cooldown": 2.0}]

    def toggle_macro(self):
        self.running = not self.running
        print(f"Macro {'ativado' if self.running else 'desativado'}")

    def run_macro(self):
        while True:
            if self.running:
                for skill in self.skills:
                    print(f"Simulando uso da habilidade: {skill['key']}")
                    time.sleep(skill['cooldown'])
            time.sleep(0.1)

    def start(self):
        print("Macro iniciado. Digite 'toggle' para ativar/desativar o macro, ou 'exit' para sair.")
        import threading
        macro_thread = threading.Thread(target=self.run_macro)
        macro_thread.start()

        while True:
            command = input().strip().lower()
            if command == 'toggle':
                self.toggle_macro()
            elif command == 'exit':
                print("Encerrando o macro.")
                self.running = False
                break
            else:
                print("Comando não reconhecido. Use 'toggle' ou 'exit'.")

        macro_thread.join()

if __name__ == "__main__":
    macro = SkillRotationMacro()
    macro.start()
