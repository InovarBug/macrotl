import json
import time
import threading
import random
from collections import Counter
import logging

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
        self.skill_cooldowns = {}  # Novo dicionário para rastrear cooldowns
        
        # Configuração do logging
        logging.basicConfig(filename='macro_log.txt', level=logging.INFO, 
                            format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'profiles': {}}

    def load_profile(self, profile_name):
        if profile_name in self.config['profiles']:
            self.current_profile = profile_name
            self.skills = self.config['profiles'][self.current_profile]['skills']
            logging.info(f"Profile '{profile_name}' loaded")
        else:
            logging.error(f"Profile '{profile_name}' not found")

    def create_profile(self, profile_name):
        if profile_name not in self.config['profiles']:
            self.config['profiles'][profile_name] = {'skills': []}
            self.save_config()
            logging.info(f"Profile '{profile_name}' created")
        else:
            logging.warning(f"Profile '{profile_name}' already exists")

    def start_recording(self):
        self.recording = True
        self.recorded_skills = []
        logging.info("Started recording skills")

    def stop_recording(self):
        self.recording = False
        if self.recorded_skills:
            self.config['profiles'][self.current_profile]['skills'] = self.recorded_skills
            self.save_config()
        logging.info("Stopped recording skills")

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def simulate_cooldown(self, skill):
        current_time = time.time()
        if skill['key'] not in self.skill_cooldowns:
            self.skill_cooldowns[skill['key']] = 0
        
        if current_time - self.skill_cooldowns[skill['key']] >= skill['cooldown']:
            self.skill_cooldowns[skill['key']] = current_time
            return False  # Skill is not on cooldown
        return True  # Skill is on cooldown

    def run_macro(self):
        logging.info("Macro started")
        while self.running:
            for skill in self.skills:
                if self.running:
                    if not self.simulate_cooldown(skill):
                        logging.info(f"Using skill {skill['key']}")
                        cooldown = self.apply_buff_reduction(skill['cooldown'])
                        self.skill_cooldowns[skill['key']] = time.time()
                        time.sleep(0.1)  # Small delay to prevent key spamming
                else:
                    break
            time.sleep(0.5)  # Reduce logging frequency
            self.check_buff_duration()
        logging.info("Macro stopped")

    def toggle_macro(self):
        self.running = not self.running
        if self.running:
            logging.info("Macro activated")
            threading.Thread(target=self.run_macro, daemon=True).start()
        else:
            logging.info("Macro deactivated")

    def apply_buff_reduction(self, cooldown):
        if self.buff_active:
            return cooldown * (1 - self.buff_reduction)
        return cooldown

    def check_buff_duration(self):
        if self.buff_active and time.time() - self.buff_start_time > self.buff_duration:
            self.buff_active = False
            logging.info("Buff expired")

