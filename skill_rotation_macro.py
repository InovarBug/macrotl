
import time
import json

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.recording = False
        self.skills = []
        self.recorded_skills = []
        self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
                current_profile = config.get('current_profile', 'default')
                profile = config.get('profiles', {}).get(current_profile, {})
                self.skills = profile.get('skills', [])
                if not self.skills:
                    print(f"Nenhuma habilidade encontrada no perfil '{current_profile}'. Usando configurações padrão.")
                    self.skills = [{"key": "1", "cooldown": 1.0}, {"key": "2", "cooldown": 2.0}]
                else:
                    print(f"Perfil '{current_profile}' carregado com sucesso.")
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
        print("Simulando execução do macro por 5 segundos:")
        start_time = time.time()
        while time.time() - start_time < 5:
            if self.running:
                for skill in self.skills:
                    print(f"Usando habilidade: {skill['key']} (cooldown: {skill['cooldown']}s)")
                    time.sleep(skill['cooldown'])
            time.sleep(0.1)

    def start_recording(self):
        self.recording = True
        self.recorded_skills = []
        print("Gravação iniciada.")

    def stop_recording(self):
        self.recording = False
        print("Gravação finalizada.")
        self.save_recorded_skills()

    def record_skill(self, key, cooldown):
        self.recorded_skills.append({"key": key, "cooldown": float(cooldown)})
        print(f"Habilidade registrada: Tecla {key}, Cooldown {cooldown}s")

    def save_recorded_skills(self):
        if self.recorded_skills:
            self.skills = self.recorded_skills
            self.update_config()
            print("Novas habilidades salvas e ativadas.")
        else:
            print("Nenhuma habilidade foi gravada.")

    def update_config(self):
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
            
            current_profile = config.get('current_profile', 'default')
            if 'profiles' not in config:
                config['profiles'] = {}
            if current_profile not in config['profiles']:
                config['profiles'][current_profile] = {}
            
            config['profiles'][current_profile]['skills'] = self.skills

            with open('config.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            
            print("Configuração atualizada com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar a configuração: {str(e)}")

    def show_current_skills(self):
        print("Habilidades atuais:")
        for skill in self.skills:
            print(f"Tecla: {skill['key']}, Cooldown: {skill['cooldown']}s")

    def create_profile(self, profile_name):
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
            
            if 'profiles' not in config:
                config['profiles'] = {}
            
            if profile_name in config['profiles']:
                print(f"O perfil '{profile_name}' já existe.")
            else:
                config['profiles'][profile_name] = {'skills': []}
                config['current_profile'] = profile_name
                with open('config.json', 'w') as config_file:
                    json.dump(config, config_file, indent=4)
                print(f"Perfil '{profile_name}' criado e selecionado com sucesso.")
                self.load_config()
        except Exception as e:
            print(f"Erro ao criar o perfil: {str(e)}")

    def list_profiles(self):
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
            
            profiles = config.get('profiles', {})
            if profiles:
                print("Perfis disponíveis:")
                for profile in profiles:
                    print(f"- {profile}")
            else:
                print("Nenhum perfil encontrado.")
        except Exception as e:
            print(f"Erro ao listar os perfis: {str(e)}")

    def select_profile(self, profile_name):
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
            
            if 'profiles' in config and profile_name in config['profiles']:
                config['current_profile'] = profile_name
                with open('config.json', 'w') as config_file:
                    json.dump(config, config_file, indent=4)
                print(f"Perfil '{profile_name}' selecionado com sucesso.")
                self.load_config()
            else:
                print(f"Perfil '{profile_name}' não encontrado.")
        except Exception as e:
            print(f"Erro ao selecionar o perfil: {str(e)}")

    def delete_profile(self, profile_name):
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
            
            if 'profiles' in config and profile_name in config['profiles']:
                del config['profiles'][profile_name]
                if config.get('current_profile') == profile_name:
                    config['current_profile'] = next(iter(config['profiles']), 'default')
                with open('config.json', 'w') as config_file:
                    json.dump(config, config_file, indent=4)
                print(f"Perfil '{profile_name}' excluído com sucesso.")
                self.load_config()
            else:
                print(f"Perfil '{profile_name}' não encontrado.")
        except Exception as e:
            print(f"Erro ao excluir o perfil: {str(e)}")

    def simulate_interactions(self):
        print("Simulando interações com o macro:")
        while True:
            command = input("Digite um comando (iniciar, parar, gravar, finalizar, perfil, sair): ").lower()
            if command == "iniciar":
                self.toggle_macro()
                self.run_macro()
            elif command == "parar":
                self.toggle_macro()
            elif command == "gravar":
                self.start_recording()
                while True:
                    skill_input = input("Digite a tecla e o cooldown da habilidade (ou 'finalizar' para terminar): ")
                    if skill_input.lower() == "finalizar":
                        break
                    key, cooldown = skill_input.split()
                    self.record_skill(key, float(cooldown))
                self.stop_recording()
            elif command == "finalizar":
                self.stop_recording()
            elif command == "perfil":
                profile_command = input("Digite uma ação de perfil (criar, listar, selecionar, excluir): ").lower()
                if profile_command == "criar":
                    profile_name = input("Digite o nome do novo perfil: ")
                    self.create_profile(profile_name)
                elif profile_command == "listar":
                    self.list_profiles()
                elif profile_command == "selecionar":
                    profile_name = input("Digite o nome do perfil a ser selecionado: ")
                    self.select_profile(profile_name)
                elif profile_command == "excluir":
                    profile_name = input("Digite o nome do perfil a ser excluído: ")
                    self.delete_profile(profile_name)
                else:
                    print("Comando de perfil inválido.")
            elif command == "sair":
                print("Encerrando o programa.")
                break
            else:
                print("Comando inválido.")

    def record_skills_realtime(self):
        print("Gravação em tempo real iniciada. Pressione 'q' para finalizar.")
        while self.recording:
            key = input("Pressione uma tecla (ou 'q' para finalizar): ")
            if key.lower() == 'q':
                self.stop_recording()
                break
            cooldown = input(f"Digite o cooldown para a tecla {key} (em segundos): ")
            try:
                cooldown = float(cooldown)
                self.record_skill(key, cooldown)
            except ValueError:
                print("Cooldown inválido. Use um número decimal.")
        
        print("\n1. Mostrando habilidades atuais")
        self.show_current_skills()
        
        print("\n2. Iniciando o macro")
        self.toggle_macro()
        self.run_macro()
        
        print("\n3. Iniciando gravação")
        self.start_recording()
        self.record_skill("3", 1.5)
        self.record_skill("4", 2.0)
        self.stop_recording()
        
        print("\n4. Mostrando novas habilidades")
        self.show_current_skills()
        
        print("\n5. Executando macro com novas habilidades")
        if not self.running:
            self.toggle_macro()
        self.run_macro()
        
        print("\nSimulação concluída.")

if __name__ == "__main__":
    macro = SkillRotationMacro()
    
    def auto_test():
        print("Iniciando teste automático")
        
        print("1. Mostrando habilidades atuais")
        macro.show_current_skills()
        
        print("\n2. Iniciando gravação")
        macro.start_recording()
        macro.record_skill("3", 1.5)
        macro.record_skill("4", 2.0)
        macro.stop_recording()
        
        print("\n3. Mostrando novas habilidades")
        macro.show_current_skills()
        
        print("\n4. Executando macro com novas habilidades")
        macro.toggle_macro()
        macro.run_macro()
        
        print("\nTeste automático concluído")
    
    auto_test()
