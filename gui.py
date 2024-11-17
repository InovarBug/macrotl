import PySimpleGUI as sg
from skill_rotation_macro import SkillRotationMacro

class MacroGUI:
    def __init__(self):
        self.macro = SkillRotationMacro()
        self.layout = [
            [sg.Text('Macro de Rotação de Skills', font=('Helvetica', 16))],
            [sg.Button('Iniciar Macro', key='-START-'), sg.Button('Parar Macro', key='-STOP-', disabled=True)],
            [sg.Text('Perfil:'), sg.Combo(self.macro.config['profiles'], key='-PROFILE-', enable_events=True, readonly=True)],
            [sg.Button('Editar Perfil', key='-EDIT-'), sg.Button('Novo Perfil', key='-NEW-')],
            [sg.Button('Iniciar Gravação', key='-RECORD-'), sg.Button('Parar Gravação', key='-STOP-RECORD-', disabled=True)],
            [sg.Button('Mostrar Habilidades', key='-SHOW-')],
            [sg.Multiline(size=(60, 10), key='-OUTPUT-', disabled=True)],
            [sg.Button('Sair')]
        ]
        self.window = sg.Window('Macro de Rotação de Skills', self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'Sair':
                break
            elif event == '-START-':
                self.macro.toggle_macro()
                self.window['-START-'].update(disabled=True)
                self.window['-STOP-'].update(disabled=False)
                self.window['-OUTPUT-'].update('Macro iniciado.\n', append=True)
            elif event == '-STOP-':
                self.macro.toggle_macro()
                self.window['-START-'].update(disabled=False)
                self.window['-STOP-'].update(disabled=True)
                self.window['-OUTPUT-'].update('Macro parado.\n', append=True)
            elif event == '-PROFILE-':
                self.macro.load_profile(values['-PROFILE-'])
                self.window['-OUTPUT-'].update(f"Perfil '{values['-PROFILE-']}' carregado.\n", append=True)
            elif event == '-EDIT-':
                self.edit_profile(values['-PROFILE-'])
            elif event == '-NEW-':
                self.new_profile()
            elif event == '-RECORD-':
                self.macro.start_recording()
                self.window['-RECORD-'].update(disabled=True)
                self.window['-STOP-RECORD-'].update(disabled=False)
                self.window['-OUTPUT-'].update('Gravação iniciada. Pressione as teclas das habilidades.\n', append=True)
            elif event == '-STOP-RECORD-':
                self.macro.stop_recording()
                self.window['-RECORD-'].update(disabled=False)
                self.window['-STOP-RECORD-'].update(disabled=True)
                self.window['-OUTPUT-'].update('Gravação finalizada.\n', append=True)
                self.save_recorded_profile()
            elif event == '-SHOW-':
                self.show_current_skills()

        self.window.close()

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
