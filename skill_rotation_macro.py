import json
import time
import keyboard
import threading
from collections import Counter

class SkillRotationMacro:
    def __init__(self):
        self.running = False
        self.recording = False
        self.config = self.load_config()
        self.current_profile = list(self.config['profiles'].keys())[0] if self.config['profiles'] else 'default'
        self.skills = self.config['profiles'].get(self.current_profile, {}).get('skills', [])
        self.recorded_skills = []
        self.last_key_time = 0
        self.skill_usage = Counter()
        self.ai_active = False
        self.ai_mode = 'PVE'  # Padrão para PVE

    def toggle_ai_mode(self):
        self.ai_mode = 'PVP' if self.ai_mode == 'PVE' else 'PVE'
        return f"Modo IA alterado para {self.ai_mode}"

    def get_ai_mode(self):
        return self.ai_mode

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'profiles': {'default': {'skills': []}}}

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def toggle_macro(self):
        self.running = not self.running
        if self.running:
            threading.Thread(target=self.run_macro, daemon=True).start()

    def run_macro(self):
        while self.running:
            for skill in self.skills:
                if self.running:
                    if self.ai_active:
                        if self.ai_mode == 'PVE':
                            self.use_pve_skill(skill)
                        else:
                            self.use_pvp_skill(skill)
                    else:
                        keyboard.press_and_release(skill['key'])
                        time.sleep(skill['cooldown'])
                else:
                    break

    def use_pve_skill(self, skill):
        keyboard.press_and_release(skill['key'])
        self.skill_usage[skill['key']] += 1
        time.sleep(skill['cooldown'])

    def use_pvp_skill(self, skill):
        # Lógica mais complexa para PVP pode ser implementada aqui
        # Por exemplo, verificar a saúde do jogador antes de usar uma habilidade defensiva
        keyboard.press_and_release(skill['key'])
        self.skill_usage[skill['key']] += 1
        time.sleep(skill['cooldown'] * 0.8)  # Cooldown reduzido para PVP

    def load_profile(self, profile_name):
        if profile_name in self.config['profiles']:
            self.current_profile = profile_name
            self.skills = self.config['profiles'][self.current_profile]['skills']

    def start_recording(self):
        self.recording = True
        self.recorded_skills = []
        self.last_key_time = time.time()
        keyboard.on_press(self.on_key_press)

    def stop_recording(self):
        self.recording = False
        keyboard.unhook_all()

    def on_key_press(self, event):
        if self.recording:
            current_time = time.time()
            cooldown = round(current_time - self.last_key_time, 2)
            self.recorded_skills.append({'key': event.name, 'cooldown': cooldown})
            self.last_key_time = current_time

    def save_recorded_profile(self, profile_name):
        self.config['profiles'][profile_name] = {'skills': self.recorded_skills}
        self.save_config()
        self.load_profile(profile_name)

    def update_skill(self, profile_name, skill_index, key, cooldown):
        self.config['profiles'][profile_name]['skills'][skill_index] = {'key': key, 'cooldown': cooldown}
        self.save_config()
        if profile_name == self.current_profile:
            self.skills = self.config['profiles'][self.current_profile]['skills']

    def create_profile(self, profile_name):
        self.config['profiles'][profile_name] = {'skills': []}
        self.save_config()

    def toggle_ai(self):
        self.ai_active = not self.ai_active
        if self.ai_active:
            self.skill_usage.clear()

    def analyze_skill_usage(self):
        if not self.ai_active:
            return "IA não está ativa."
        
        total_uses = sum(self.skill_usage.values())
        if total_uses == 0:
            return "Nenhuma habilidade foi usada ainda."
        
        analysis = "Análise de uso de habilidades:\n"
        for skill, count in self.skill_usage.most_common():
            percentage = (count / total_uses) * 100
            analysis += f"Habilidade {skill}: {percentage:.2f}% de uso\n"
        
        return analysis

    def get_current_skills(self):
        return self.skills

    def clear_skill_usage(self):
        self.skill_usage.clear()

    def suggest_optimization(self):
        if not self.ai_active:
            return "IA não está ativa. Ative a IA para obter sugestões de otimização."
        
        total_uses = sum(self.skill_usage.values())
        if total_uses == 0:
            return "Nenhuma habilidade foi usada ainda. Use o macro por um tempo para coletar dados."
        
        avg_usage = total_uses / len(self.skill_usage)
        suggestion = "Sugestões de otimização:\n"
        
        for skill, count in self.skill_usage.items():
            if count < avg_usage * 0.5:
                suggestion += f"Considere usar a habilidade {skill} com mais frequência.\n"
            elif count > avg_usage * 1.5:
                suggestion += f"A habilidade {skill} está sendo usada muito frequentemente. Considere reduzir seu uso.\n"
        
        if not suggestion.endswith(":\n"):
            suggestion += "A rotação atual parece bem balanceada.\n"
        
        return suggestion

if __name__ == "__main__":
    print("Este arquivo não deve ser executado diretamente. Por favor, execute gui.py para usar a interface gráfica.")
