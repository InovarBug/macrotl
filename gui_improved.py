
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from skill_rotation_macro import SkillRotationMacro
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class MacroGUI:
    def __init__(self):
        self.macro = SkillRotationMacro()
        self.root = tk.Tk()
        self.root.title('Macro de Rotação de Skills com IA')
        self.create_widgets()
        self.root.after(60000, self.auto_save)  # Iniciar o salvamento automático

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(frame, text='Macro de Rotação de Skills com IA', font=('Helvetica', 16)).grid(column=0, row=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(frame, text='Iniciar Macro', command=self.start_macro)
        self.start_button.grid(column=0, row=1, pady=5, padx=5, sticky=tk.W)
        ToolTip(self.start_button, "Inicia a execução do macro")

        self.stop_button = ttk.Button(frame, text='Parar Macro', command=self.stop_macro, state=tk.DISABLED)
        self.stop_button.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)
        ToolTip(self.stop_button, "Para a execução do macro")

        ttk.Label(frame, text='Perfil:').grid(column=0, row=2, sticky=tk.W, pady=5)
        self.profile_combo = ttk.Combobox(frame, values=list(self.macro.config['profiles'].keys()), state='readonly')
        self.profile_combo.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)
        self.profile_combo.bind('<<ComboboxSelected>>', self.load_profile)
        ToolTip(self.profile_combo, "Seleciona o perfil ativo")

        edit_profile_button = ttk.Button(frame, text='Editar Perfil', command=self.edit_profile)
        edit_profile_button.grid(column=0, row=3, pady=5, padx=5, sticky=tk.W)
        ToolTip(edit_profile_button, "Edita o perfil selecionado")

        new_profile_button = ttk.Button(frame, text='Novo Perfil', command=self.new_profile)
        new_profile_button.grid(column=1, row=3, pady=5, padx=5, sticky=tk.W)
        ToolTip(new_profile_button, "Cria um novo perfil")

        self.record_button = ttk.Button(frame, text='Iniciar Gravação', command=self.start_recording)
        self.record_button.grid(column=0, row=4, pady=5, padx=5, sticky=tk.W)
        ToolTip(self.record_button, "Inicia a gravação de uma nova sequência de habilidades")

        self.stop_record_button = ttk.Button(frame, text='Parar Gravação', command=self.stop_recording, state=tk.DISABLED)
        self.stop_record_button.grid(column=1, row=4, pady=5, padx=5, sticky=tk.W)
        ToolTip(self.stop_record_button, "Para a gravação da sequência de habilidades")

        show_skills_button = ttk.Button(frame, text='Mostrar Habilidades', command=self.show_current_skills)
        show_skills_button.grid(column=0, row=5, pady=5, padx=5, sticky=tk.W)
        ToolTip(show_skills_button, "Mostra as habilidades do perfil atual")

        visualize_cooldowns_button = ttk.Button(frame, text='Visualizar Cooldowns', command=self.visualize_cooldowns)
        visualize_cooldowns_button.grid(column=1, row=5, pady=5, padx=5, sticky=tk.W)
        ToolTip(visualize_cooldowns_button, "Mostra uma visualização gráfica dos cooldowns")

        self.ai_button = ttk.Button(frame, text='Ativar IA', command=self.toggle_ai)
        self.ai_button.grid(column=0, row=6, pady=5, padx=5, sticky=tk.W)
        ToolTip(self.ai_button, "Ativa/Desativa a IA para otimização automática")

        analyze_usage_button = ttk.Button(frame, text='Analisar Uso', command=self.analyze_skill_usage)
        analyze_usage_button.grid(column=0, row=7, pady=5, padx=5, sticky=tk.W)
        ToolTip(analyze_usage_button, "Analisa o uso das habilidades")

        suggest_optimization_button = ttk.Button(frame, text='Sugerir Otimização', command=self.suggest_optimization)
        suggest_optimization_button.grid(column=1, row=7, pady=5, padx=5, sticky=tk.W)
        ToolTip(suggest_optimization_button, "Sugere otimizações para a rotação de habilidades")

        clear_usage_button = ttk.Button(frame, text='Limpar Uso', command=self.clear_skill_usage)
        clear_usage_button.grid(column=0, row=8, pady=5, padx=5, sticky=tk.W)
        ToolTip(clear_usage_button, "Limpa os dados de uso das habilidades")

        export_button = ttk.Button(frame, text='Exportar Perfis', command=self.export_profiles)
        export_button.grid(column=1, row=8, pady=5, padx=5, sticky=tk.W)
        ToolTip(export_button, "Exporta os perfis para um arquivo")

        import_button = ttk.Button(frame, text='Importar Perfis', command=self.import_profiles)
        import_button.grid(column=0, row=9, pady=5, padx=5, sticky=tk.W)
        ToolTip(import_button, "Importa perfis de um arquivo")

        self.output_text = tk.Text(frame, height=10, width=60, state=tk.DISABLED)
        self.output_text.grid(column=0, row=10, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        # Adicionar um canvas para visualização da rotação de habilidades
        self.skill_canvas = tk.Canvas(frame, width=300, height=100)
        self.skill_canvas.grid(column=0, row=11, columnspan=2, pady=10)

        # Adicionar uma área para o gráfico de uso de habilidades
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().grid(column=0, row=12, columnspan=2, pady=10)

        # Adicionar uma área de notificações
        self.notification_label = ttk.Label(frame, text="", font=('Helvetica', 10, 'italic'))
        self.notification_label.grid(column=0, row=13, columnspan=2, pady=5)

        exit_button = ttk.Button(frame, text='Sair', command=self.root.quit)
        exit_button.grid(column=0, row=14, columnspan=2, pady=5)
        ToolTip(exit_button, "Fecha o programa")

        for child in frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # Configurar salvamento automático
        self.root.after(60000, self.auto_save)  # Salva a cada 60 segundos

    def run(self):
        self.root.mainloop()

    def start_macro(self):
        self.macro.toggle_macro()
        self.start_button['state'] = tk.DISABLED
        self.stop_button['state'] = tk.NORMAL
        self.update_output('Macro iniciado.\n')
        self.visualize_skill_rotation()

    def stop_macro(self):
        self.macro.toggle_macro()
        self.start_button['state'] = tk.NORMAL
        self.stop_button['state'] = tk.DISABLED
        self.update_output('Macro parado.\n')

    def load_profile(self, event):
        profile_name = self.profile_combo.get()
        self.macro.load_profile(profile_name)
        self.update_output(f"Perfil '{profile_name}' carregado.\n")
        self.visualize_skill_rotation()

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

            ttk.Button(edit_window, text='Salvar', command=save_profile).grid(row=len(skills), column=0, columnspan=3, pady=10)

    def new_profile(self):
        profile_name = simpledialog.askstring("Novo Perfil", "Nome do novo perfil:")
        if profile_name:
            self.macro.create_profile(profile_name)
            self.profile_combo['values'] = list(self.macro.config['profiles'].keys())
            self.profile_combo.set(profile_name)
            self.update_output(f"Novo perfil '{profile_name}' criado.\n")

    def start_recording(self):
        self.macro.start_recording()
        self.record_button['state'] = tk.DISABLED
        self.stop_record_button['state'] = tk.NORMAL
        self.update_output('Gravação iniciada. Pressione as teclas para registrar as habilidades.\n')

    def stop_recording(self):
        self.macro.stop_recording()
        self.record_button['state'] = tk.NORMAL
        self.stop_record_button['state'] = tk.DISABLED
        profile_name = simpledialog.askstring("Salvar Gravação", "Nome do perfil para salvar a gravação:")
        if profile_name:
            self.macro.save_recorded_profile(profile_name)
            self.profile_combo['values'] = list(self.macro.config['profiles'].keys())
            self.profile_combo.set(profile_name)
            self.update_output(f"Gravação salva como perfil '{profile_name}'.\n")
        self.visualize_skill_rotation()

    def show_current_skills(self):
        skills = self.macro.skills
        skill_text = "Habilidades atuais:\n"
        for i, skill in enumerate(skills):
            skill_text += f"{i+1}. Tecla: {skill['key']}, Cooldown: {skill['cooldown']}s\n"
        self.update_output(skill_text)

    def toggle_ai(self):
        self.macro.toggle_ai()
        if self.macro.ai_active:
            self.ai_button['text'] = 'Desativar IA'
            self.update_output('IA ativada.\n')
        else:
            self.ai_button['text'] = 'Ativar IA'
            self.update_output('IA desativada.\n')

    def analyze_skill_usage(self):
        analysis = self.macro.analyze_skill_usage()
        self.update_output(analysis)
        self.update_skill_usage_graph()
        self.show_notification("Análise de uso de habilidades atualizada!")

    def suggest_optimization(self):
        suggestion = self.macro.suggest_optimization()
        self.update_output(suggestion)
        self.show_notification("Sugestão de otimização gerada!")

    def update_output(self, text):
        self.output_text['state'] = tk.NORMAL
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text['state'] = tk.DISABLED

    def visualize_skill_rotation(self):
        self.skill_canvas.delete("all")
        skills = self.macro.get_current_skills()
        for i, skill in enumerate(skills):
            x = i * 50 + 25
            y = 50
            self.skill_canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
            self.skill_canvas.create_text(x, y, text=skill['key'])

    def update_skill_usage_graph(self):
        self.ax.clear()
        skills = list(self.macro.skill_usage.keys())
        usage = list(self.macro.skill_usage.values())
        self.ax.bar(skills, usage)
        self.ax.set_title("Uso de Habilidades")
        self.ax.set_xlabel("Habilidades")
        self.ax.set_ylabel("Número de Usos")
        self.canvas.draw()

    def show_notification(self, message):
        self.notification_label.config(text=message)
        self.root.after(5000, lambda: self.notification_label.config(text=""))

    def clear_skill_usage(self):
        self.macro.clear_skill_usage()
        self.update_skill_usage_graph()
        self.show_notification("Uso de habilidades limpo.")

    def visualize_cooldowns(self):
        skills = self.macro.get_current_skills()
        if not skills:
            self.show_notification("Nenhuma habilidade para visualizar.")
            return

        cooldown_window = tk.Toplevel(self.root)
        cooldown_window.title("Visualização de Cooldowns")
        cooldown_window.geometry("400x300")

        canvas = tk.Canvas(cooldown_window, width=380, height=280)
        canvas.pack(pady=10)

        max_cooldown = max(skill['cooldown'] for skill in skills)
        bar_width = 30
        spacing = 20
        x_start = 40

        for i, skill in enumerate(skills):
            x = x_start + i * (bar_width + spacing)
            bar_height = (skill['cooldown'] / max_cooldown) * 200
            y = 250 - bar_height

            canvas.create_rectangle(x, y, x + bar_width, 250, fill="lightblue")
            canvas.create_text(x + bar_width/2, 260, text=skill['key'])
            canvas.create_text(x + bar_width/2, y - 10, text=f"{skill['cooldown']}s")

        canvas.create_line(20, 250, 380, 250, width=2)  # x-axis
        canvas.create_line(20, 250, 20, 30, width=2)  # y-axis
        canvas.create_text(10, 20, text=f"{max_cooldown}s", anchor="e")

        self.show_notification("Visualização de cooldowns aberta.")

    def export_profiles(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(self.macro.config['profiles'], f, indent=4)
            self.show_notification("Perfis exportados com sucesso!")

    def import_profiles(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                imported_profiles = json.load(f)
            self.macro.config['profiles'].update(imported_profiles)
            self.macro.save_config()
            self.profile_combo['values'] = list(self.macro.config['profiles'].keys())
            self.show_notification("Perfis importados com sucesso!")

    def auto_save(self):
        self.macro.save_config()
        self.show_notification("Configurações salvas automaticamente.")
        self.root.after(60000, self.auto_save)  # Agendar próximo salvamento automático

if __name__ == "__main__":
    gui = MacroGUI()
    gui.run()
