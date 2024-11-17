import tkinter as tk
from tkinter import ttk, messagebox
from skill_rotation_macro import SkillRotationMacro

class MacroGUI:
    def __init__(self):
        self.macro = SkillRotationMacro()
        self.root = tk.Tk()
        self.root.title('Macro de Rotação de Skills com IA')
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(frame, text='Macro de Rotação de Skills com IA', font=('Helvetica', 16)).grid(column=0, row=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(frame, text='Iniciar Macro', command=self.start_macro)
        self.start_button.grid(column=0, row=1, pady=5, padx=5, sticky=tk.W)

        self.stop_button = ttk.Button(frame, text='Parar Macro', command=self.stop_macro, state=tk.DISABLED)
        self.stop_button.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)

        ttk.Label(frame, text='Perfil:').grid(column=0, row=2, sticky=tk.W, pady=5)
        self.profile_combo = ttk.Combobox(frame, values=list(self.macro.config['profiles'].keys()), state='readonly')
        self.profile_combo.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)
        self.profile_combo.bind('<<ComboboxSelected>>', self.load_profile)

        ttk.Button(frame, text='Editar Perfil', command=self.edit_profile).grid(column=0, row=3, pady=5, padx=5, sticky=tk.W)
        ttk.Button(frame, text='Novo Perfil', command=self.new_profile).grid(column=1, row=3, pady=5, padx=5, sticky=tk.W)

        self.record_button = ttk.Button(frame, text='Iniciar Gravação', command=self.start_recording)
        self.record_button.grid(column=0, row=4, pady=5, padx=5, sticky=tk.W)

        self.stop_record_button = ttk.Button(frame, text='Parar Gravação', command=self.stop_recording, state=tk.DISABLED)
        self.stop_record_button.grid(column=1, row=4, pady=5, padx=5, sticky=tk.W)

        ttk.Button(frame, text='Mostrar Habilidades', command=self.show_current_skills).grid(column=0, row=5, columnspan=2, pady=5)

        self.ai_button = ttk.Button(frame, text='Ativar IA', command=self.toggle_ai)
        self.ai_button.grid(column=0, row=6, pady=5, padx=5, sticky=tk.W)

        ttk.Button(frame, text='Analisar Uso', command=self.analyze_skill_usage).grid(column=0, row=7, pady=5, padx=5, sticky=tk.W)
        ttk.Button(frame, text='Sugerir Otimização', command=self.suggest_optimization).grid(column=1, row=7, pady=5, padx=5, sticky=tk.W)

        self.output_text = tk.Text(frame, height=10, width=60, state=tk.DISABLED)
        self.output_text.grid(column=0, row=8, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        ttk.Button(frame, text='Sair', command=self.root.quit).grid(column=0, row=9, columnspan=2, pady=5)

        for child in frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def run(self):
        self.root.mainloop()

    def start_macro(self):
        self.macro.toggle_macro()
        self.start_button['state'] = tk.DISABLED
        self.stop_button['state'] = tk.NORMAL
        self.update_output('Macro iniciado.\n')

    def stop_macro(self):
        self.macro.toggle_macro()
        self.start_button['state'] = tk.NORMAL
        self.stop_button['state'] = tk.DISABLED
        self.update_output('Macro parado.\n')

    def load_profile(self, event):
        profile_name = self.profile_combo.get()
        self.macro.load_profile(profile_name)
        self.update_output(f"Perfil '{profile_name}' carregado.\n")

    def edit_profile(self):
        profile_name = self.profile_combo.get()
        if profile_name:
            skills = self.macro.config['profiles'][profile_name]['skills']
            edit_window = tk.Toplevel(self.root)
            edit_window.title(f'Editando perfil: {profile_name}')
            edit_window.grab_set()

            for i, skill in enumerate(skills):
                ttk.Label(edit_window, text=f'Skill {i+1}').grid(row=i, column=0, padx=5, pady=5)
                key_entry = ttk.Entry(edit_window, width=5)
                key_entry.insert(0, skill['key'])
                key_entry.grid(row=i, column=1, padx=5, pady=5)
                cooldown_entry = ttk.Entry(edit_window, width=5)
                cooldown_entry.insert(0, str(skill['cooldown']))
                cooldown_entry.grid(row=i, column=2, padx=5, pady=5)

            def save_profile():
                for i, skill in enumerate(skills):
                    key = edit_window.grid_slaves(row=i, column=1)[0].get()
                    cooldown = float(edit_window.grid_slaves(row=i, column=2)[0].get())
                    self.macro.update_skill(profile_name, i, key, cooldown)
                self.update_output(f"Perfil '{profile_name}' atualizado.\n")
                edit_window.destroy()

            ttk.Button(edit_window, text='Salvar', command=save_profile).grid(row=len(skills), column=1, pady=10)

    def new_profile(self):
        new_window = tk.Toplevel(self.root)
        new_window.title('Novo Perfil')
        new_window.grab_set()

        ttk.Label(new_window, text='Nome do novo perfil:').pack(pady=5)
        name_entry = ttk.Entry(new_window)
        name_entry.pack(pady=5)

        def create_profile():
            new_profile_name = name_entry.get()
            if new_profile_name and new_profile_name not in self.macro.config['profiles']:
                self.macro.create_profile(new_profile_name)
                self.profile_combo['values'] = list(self.macro.config['profiles'].keys())
                self.profile_combo.set(new_profile_name)
                self.update_output(f"Novo perfil '{new_profile_name}' criado.\n")
                new_window.destroy()
            else:
                messagebox.showerror('Erro', 'Nome de perfil inválido ou já existente.')

        ttk.Button(new_window, text='Criar', command=create_profile).pack(pady=10)

    def start_recording(self):
        self.macro.start_recording()
        self.record_button['state'] = tk.DISABLED
        self.stop_record_button['state'] = tk.NORMAL
        self.update_output('Gravação iniciada. Pressione as teclas das habilidades.\n')

    def stop_recording(self):
        self.macro.stop_recording()
        self.record_button['state'] = tk.NORMAL
        self.stop_record_button['state'] = tk.DISABLED
        self.update_output('Gravação finalizada.\n')
        self.save_recorded_profile()
        self.update_output('Gravação finalizada.\n')
        self.save_recorded_profile()

    def show_current_skills(self):
        skills = self.macro.skills
        if skills:
            skill_info = "Habilidades atuais:\n"
            for i, skill in enumerate(skills):
                skill_info += f"Skill {i+1}: Tecla = {skill['key']}, Cooldown = {skill['cooldown']}s\n"
            self.update_output(skill_info)
        else:
            self.update_output("Nenhuma habilidade configurada.\n")

    def save_recorded_profile(self):
        new_window = tk.Toplevel(self.root)
        new_window.title('Salvar Perfil Gravado')

        ttk.Label(new_window, text='Nome do perfil:').pack(pady=5)
        name_entry = ttk.Entry(new_window)
        name_entry.pack(pady=5)

        def save_profile():
            profile_name = name_entry.get()
            if profile_name:
                self.macro.save_recorded_profile(profile_name)
                self.profile_combo['values'] = list(self.macro.config['profiles'].keys())
                self.profile_combo.set(profile_name)
                self.update_output(f"Perfil gravado '{profile_name}' salvo.\n")
                new_window.destroy()
            else:
                messagebox.showerror('Erro', 'Nome de perfil inválido.')

        ttk.Button(new_window, text='Salvar', command=save_profile).pack(pady=10)

    def toggle_ai(self):
        self.macro.toggle_ai()
        if self.ai_button['text'] == 'Ativar IA':
            self.ai_button['text'] = 'Desativar IA'
            self.update_output("IA ativada\n")
        else:
            self.ai_button['text'] = 'Ativar IA'
            self.update_output("IA desativada\n")

    def analyze_skill_usage(self):
        analysis = self.macro.analyze_skill_usage()
        self.update_output(analysis)

    def suggest_optimization(self):
        suggestion = self.macro.suggest_optimization()
        self.update_output(suggestion)

    def update_output(self, message):
        self.output_text['state'] = tk.NORMAL
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.output_text['state'] = tk.DISABLED

if __name__ == '__main__':
    gui = MacroGUI()
    gui.run()

    def toggle_ai(self):
        self.macro.toggle_ai()
        if self.window['-AI-TOGGLE-'].get_text() == 'Ativar IA':
            self.window['-AI-TOGGLE-'].update('Desativar IA')
            self.window['-OUTPUT-'].update("IA ativada\n", append=True)
        else:
            self.window['-AI-TOGGLE-'].update('Ativar IA')
            self.window['-OUTPUT-'].update("IA desativada\n", append=True)

    def analyze_skill_usage(self):
        analysis = self.macro.analyze_skill_usage()
        self.window['-OUTPUT-'].update(analysis, append=True)

    def suggest_optimization(self):
        suggestion = self.macro.suggest_optimization()
        self.window['-OUTPUT-'].update(suggestion, append=True)

    def edit_profile(self, profile_name):
        if profile_name:
            skills = self.macro.config['profiles'][profile_name]['skills']
            layout = [
                [sg.Text(f'Editando perfil: {profile_name}')],
                [sg.Text('Habilidade'), sg.Text('Tecla'), sg.Text('Cooldown (s)')],
            ]
            for i, skill in enumerate(skills):
                layout.append([
                    sg.Text(f'Skill {i+1}'),
                    sg.Input(skill['key'], key=f'-KEY-{i}-', size=(5,1)),
                    sg.Input(skill['cooldown'], key=f'-COOLDOWN-{i}-', size=(5,1))
                ])
            layout.append([sg.Button('Salvar'), sg.Button('Cancelar')])

            window = sg.Window('Editar Perfil', layout)

            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                    break
                elif event == 'Salvar':
                    for i, skill in enumerate(skills):
                        key = values[f'-KEY-{i}-']
                        cooldown = float(values[f'-COOLDOWN-{i}-'])
                        self.macro.update_skill(profile_name, i, key, cooldown)
                    self.window['-OUTPUT-'].update(f"Perfil '{profile_name}' atualizado.\n", append=True)
                    break

            window.close()

    def new_profile(self):
        layout = [
            [sg.Text('Nome do novo perfil:')],
            [sg.Input(key='-NEW-PROFILE-NAME-')],
            [sg.Button('Criar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Novo Perfil', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            elif event == 'Criar':
                new_profile_name = values['-NEW-PROFILE-NAME-']
                if new_profile_name and new_profile_name not in self.macro.config['profiles']:
                    self.macro.create_profile(new_profile_name)
                    self.window['-PROFILE-'].update(values=list(self.macro.config['profiles'].keys()), value=new_profile_name)
                    self.window['-OUTPUT-'].update(f"Novo perfil '{new_profile_name}' criado.\n", append=True)
                    break
                else:
                    sg.popup('Nome de perfil inválido ou já existente.')

        window.close()

    def save_recorded_profile(self):
        layout = [
            [sg.Text('Nome do perfil gravado:')],
            [sg.Input(key='-RECORDED-PROFILE-NAME-')],
            [sg.Button('Salvar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Salvar Perfil Gravado', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            elif event == 'Salvar':
                profile_name = values['-RECORDED-PROFILE-NAME-']
                if profile_name:
                    self.macro.save_recorded_profile(profile_name)
                    self.window['-PROFILE-'].update(values=list(self.macro.config['profiles'].keys()), value=profile_name)
                    self.window['-OUTPUT-'].update(f"Perfil gravado '{profile_name}' salvo.\n", append=True)
                    break
                else:
                    sg.popup('Nome de perfil inválido.')

        window.close()

    def show_current_skills(self):
        skills = self.macro.skills
        output = "Habilidades atuais:\n"
        for i, skill in enumerate(skills):
            output += f"Skill {i+1}: Tecla = {skill['key']}, Cooldown = {skill['cooldown']}s\n"
        self.window['-OUTPUT-'].update(output, append=True)

if __name__ == '__main__':
    sg.theme('DefaultNoMoreNagging')
    gui = MacroGUI()
    gui.run()
