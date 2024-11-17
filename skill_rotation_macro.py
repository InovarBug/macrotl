import json
import time
import keyboard
import threading
import random
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
        self.buff_active = False
        self.buff_duration = 0
        self.buff_start_time = 0
        self.buff_reduction = 0

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
                        cooldown = self.apply_buff_reduction(skill['cooldown'])
                        time.sleep(cooldown)
                else:
                    break
            self.check_buff_duration()

    def activate_buff(self, duration, reduction):
        """Ativa o buff com a duração e redução especificadas."""
        self.buff_active = True
        self.buff_duration = duration
        self.buff_start_time = time.time()
        self.buff_reduction = reduction

    def check_buff_duration(self):
        """Verifica se o buff ainda está ativo e o desativa se o tempo expirou."""
        if self.buff_active and time.time() - self.buff_start_time > self.buff_duration:
            self.buff_active = False

    def apply_buff_reduction(self, cooldown):
        """Aplica a redução do buff ao cooldown da habilidade."""
        if self.buff_active:
            return cooldown * (1 - self.buff_reduction)
        return cooldown

    def get_buff_remaining_time(self):
        """Retorna o tempo restante do buff em segundos."""
        if self.buff_active:
            remaining = self.buff_duration - (time.time() - self.buff_start_time)
            return max(0, remaining)
        return 0

    def use_pve_skill(self, skill):
        keyboard.press_and_release(skill['key'])
        self.skill_usage[skill['key']] += 1
        cooldown = self.apply_buff_reduction(skill['cooldown'] * 1.2)  # Cooldown aumentado para PVE
        time.sleep(cooldown)

    def use_pvp_skill(self, skill):
        # Lógica mais complexa para PVP
        if skill.get('type') == 'defensive' and self.player_health() < 50:
            # Prioriza habilidades defensivas quando a saúde está baixa
            keyboard.press_and_release(skill['key'])
            self.skill_usage[skill['key']] += 2  # Conta como uso duplo para enfatizar a importância
        elif skill.get('type') == 'offensive' and self.player_health() > 70:
            # Usa habilidades ofensivas quando a saúde está alta
            keyboard.press_and_release(skill['key'])
            self.skill_usage[skill['key']] += 1
        else:
            # Usa habilidades normalmente em outras situações
            keyboard.press_and_release(skill['key'])
            self.skill_usage[skill['key']] += 1
        
        cooldown = self.apply_buff_reduction(skill['cooldown'] * 0.8)  # Cooldown reduzido para PVP
        time.sleep(cooldown)

    def player_health(self):
        # Simula a verificação da saúde do jogador
        # Em uma implementação real, isso seria substituído por uma leitura real da saúde do jogador
        return random.randint(1, 100)

    def load_profile(self, profile_name):
        if profile_name in self.config['profiles']:
            self.current_profile = profile_name
            self.skills = self.config['profiles'][self.current_profile]['skills']

    def start_recording(self):
        self.recording = True
        self.recorded_skills = []
        self.last_key_time = time.time()
        keyboard.on_press(self.on_key_press)
        print("Gravação iniciada. Pressione as teclas para gravar.")

    def stop_recording(self):
        self.recording = False
        keyboard.unhook_all()
        print(f"Gravação finalizada. {len(self.recorded_skills)} teclas gravadas.")

    def on_key_press(self, event):
        if self.recording:
            current_time = time.time()
            cooldown = round(current_time - self.last_key_time, 2)
            self.recorded_skills.append({'key': event.name, 'cooldown': cooldown})
            self.last_key_time = current_time
            print(f"Tecla gravada: {event.name}, Cooldown: {cooldown}s")

    def save_recorded_profile(self, profile_name):
        if self.recorded_skills:
            self.config['profiles'][profile_name] = {'skills': self.recorded_skills}
            self.save_config()
            self.load_profile(profile_name)
            print(f"Perfil '{profile_name}' salvo com sucesso.")
        else:
            print("Nenhuma skill foi gravada para salvar.")

    def update_skill(self, profile_name, skill_index, key, cooldown):
        if profile_name in self.config['profiles'] and 'skills' in self.config['profiles'][profile_name]:
            if 0 <= skill_index < len(self.config['profiles'][profile_name]['skills']):
                self.config['profiles'][profile_name]['skills'][skill_index] = {'key': key, 'cooldown': cooldown}
                self.save_config()
            else:
                print(f"Invalid skill index for profile '{profile_name}'")
        else:
            print(f"Profile '{profile_name}' not found or has no skills")
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
