
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

    def simulate_interactions(self):
        print("Simulando interações com o macro:")
        
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
    macro.simulate_interactions()
