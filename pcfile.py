import os
import psutil
import customtkinter as ctk
from tkinter import messagebox, simpledialog

# Configurações visuais do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ExecutorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # CONFIGURAÇÃO DA JANELA PRINCIPAL
        self.title("CoToAs.net - PC Executor Hub v1.7")
        self.geometry("850x480")
        self.resizable(False, False)

        # Pasta de Scripts integrada
        self.pasta_scripts = "scripts"
        if not os.path.exists(self.pasta_scripts):
            os.makedirs(self.pasta_scripts)

        self.tema_escuro = True

        # ---------------------------------------------------------------------
        # LAYOUT: BARRA LATERAL (Esquerda)
        # ---------------------------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        self.label_sidebar = ctk.CTkLabel(self.sidebar_frame, text="MEUS SCRIPTS", font=ctk.CTkFont(size=14, weight="bold"))
        self.label_sidebar.pack(pady=15)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.sidebar_frame, width=200, height=250)
        self.scrollable_frame.pack(pady=5, padx=5, fill="both", expand=True)

        self.btn_save = ctk.CTkButton(self.sidebar_frame, text="SALVAR SCRIPT", fg_color="#8B0000", hover_color="#FF0000", font=ctk.CTkFont(weight="bold"), command=self.acao_salvar)
        self.btn_save.pack(pady=5, padx=10, fill="x")

        self.btn_theme = ctk.CTkButton(self.sidebar_frame, text="MODO CLARO ☀️", fg_color="#444444", hover_color="#666666", font=ctk.CTkFont(weight="bold"), command=self.alternar_tema)
        self.btn_theme.pack(pady=10, padx=10, fill="x")

        # ---------------------------------------------------------------------
        # LAYOUT: ÁREA PRINCIPAL (Direita)
        # ---------------------------------------------------------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.label_titulo = ctk.CTkLabel(self.main_frame, text="CoToAs.net PC EDITION", font=ctk.CTkFont(size=18, weight="bold"))
        self.label_titulo.pack(pady=10)

        # Editor de Texto Principal
        self.text_box = ctk.CTkTextbox(self.main_frame, width=590, height=280, font=("Consolas", 14), text_color="#00FF00")
        self.text_box.pack(pady=5, padx=20)
        self.text_box.insert("0.0", "-- Desenvolvido por CoToAs.net...\n")
        
        # Vincula a digitação do usuário para atualizar o contador automaticamente
        self.text_box.bind("<KeyRelease>", self.atualizar_contador)

        # BARRA DE STATUS (Contador de Linhas e Caracteres)
        self.status_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=20)
        self.status_frame.pack(fill="x", padx=25, pady=0)
        
        self.label_contador = ctk.CTkLabel(self.status_frame, text="Linhas: 2 | Caracteres: 36", font=ctk.CTkFont(size=11), text_color="#888888")
        self.label_contador.pack(side="right")

        # Container inferior de botões de controle
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=20, pady=10)

        self.btn_inject = ctk.CTkButton(self.button_frame, text="INJECT", fg_color="#008B8B", hover_color="#00FFFF", font=ctk.CTkFont(weight="bold"), command=self.acao_injetar)
        self.btn_inject.pack(side="left", padx=5)

        self.btn_clear = ctk.CTkButton(self.button_frame, text="CLEAR", fg_color="#555555", hover_color="#777777", font=ctk.CTkFont(weight="bold"), command=self.acao_limpar)
        self.btn_clear.pack(side="left", padx=5)

        self.btn_execute = ctk.CTkButton(self.button_frame, text="EXECUTE", fg_color="#228B22", hover_color="#32CD32", font=ctk.CTkFont(weight="bold"), command=self.acao_executar)
        self.btn_execute.pack(side="right", padx=5)

        self.atualizar_lista_interface()

    # ---------------------------------------------------------------------
    # LÓGICA INTERNA E SEÇÃO CORRIGIDA
    # ---------------------------------------------------------------------
    def atualizar_contador(self, event=None):
        texto = self.text_box.get("0.0", "end-1c")
        caracteres = len(texto)
        linhas = len(texto.split('\n')) if caracteres > 0 else 0
        self.label_contador.configure(text=f"Linhas: {linhas} | Caracteres: {caracteres}")

    def alternar_tema(self):
        if self.tema_escuro:
            ctk.set_appearance_mode("Light")
            self.btn_theme.configure(text="MODO ESCURO 🌙", fg_color="#DADADA", text_color="black", hover_color="#B5B5B5")
            self.text_box.configure(text_color="#006400")
            self.tema_escuro = False
        else:
            ctk.set_appearance_mode("Dark")
            self.btn_theme.configure(text="MODO CLARO ☀️", fg_color="#444444", text_color="white", hover_color="#666666")
            self.text_box.configure(text_color="#00FF00")
            self.tema_escuro = True

    def atualizar_lista_interface(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not os.path.exists(self.pasta_scripts):
            return

        arquivos = [f for f in os.listdir(self.pasta_scripts) if f.endswith('.txt')]

        if not arquivos:
            ctk.CTkLabel(self.scrollable_frame, text="Nenhum script", font=ctk.CTkFont(size=11, slant="italic")).pack(pady=10)
            return

        for arquivo in arquivos:
            nome_arquivo_str = str(arquivo)
            nome_exibicao = nome_arquivo_str.replace(".txt", "")
            
            item_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)

            btn = ctk.CTkButton(
                item_frame, text=nome_exibicao, fg_color="#2D2D2D", hover_color="#3D3D3D", anchor="w", width=140,
                command=lambda name=nome_arquivo_str: self.acao_carregar(name)
            )
            btn.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(
                item_frame, text="❌", fg_color="#551A1A", hover_color="#8B0000", width=30,
                command=lambda name=nome_arquivo_str: self.acao_deletar(name)
            )
            btn_del.pack(side="right", padx=2)

    def acao_salvar(self):
        texto = self.text_box.get("0.0", "end").strip()
        if not texto or texto.startswith("-- Desenvolvido por"):
            messagebox.showwarning("Aviso", "Escreva algo válido no editor antes de salvar!")
            return

        nome = simpledialog.askstring("Salvar", "Digite o nome do arquivo do script:")
        if nome:
            nome = nome.strip()
            if not nome.endswith(".txt"):
                nome += ".txt"
            caminho = os.path.join(self.pasta_scripts, nome)
            try:
                with open(caminho, "w", encoding="utf-8") as f:
                    f.write(texto)
                messagebox.showinfo("Sucesso", "O script foi gravado localmente com sucesso!")
                self.atualizar_lista_interface()
                self.atualizar_contador()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar o arquivo:\n{e}")

    def acao_deletar(self, nome_arquivo):
        """Remove o arquivo .txt selecionado da pasta local do PC"""
        confirmar = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja apagar o script '{nome_arquivo.replace('.txt', '')}' permanentemente?")
        if confirmar:
            caminho = os.path.join(self.pasta_scripts, nome_arquivo)
            try:
                if os.path.exists(caminho):
                    os.remove(caminho)
                    self.atualizar_lista_interface()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível deletar o arquivo:\n{e}")

    def acao_carregar(self, nome_arquivo):
        caminho = os.path.join(self.pasta_scripts, nome_arquivo)
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()
            self.acao_limpar()
            self.text_box.insert("0.0", conteudo)
            self.atualizar_contador()
        except Exception as e:
            messagebox.showerror("Erro de Leitura", f"Falha interna ao tentar abrir o arquivo:\n{e}")

    def acao_limpar(self):
        self.text_box.delete("0.0", "end")
        self.atualizar_contador()

    def acao_injetar(self):
        processo_alvo = "RobloxPlayerBeta.exe"
        jogo_encontrado = False
        pid_encontrado = None

        for processo in psutil.process_iter(['pid', 'name']):
            try:
                if processo.info['name'].lower() == processo_alvo.lower():
                    jogo_encontrado = True
                    pid_encontrado = processo.info['pid']
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        if jogo_encontrado:
            messagebox.showinfo("CoToAs.net", f"Roblox detectado no sistema!\nPID associado: {pid_encontrado}")
        else:
            messagebox.showwarning("CoToAs.net", "O processo 'RobloxPlayerBeta.exe' não está rodando no momento.")

    def acao_executar(self):
        script = self.text_box.get("0.0", "end").strip()
        messagebox.showinfo("CoToAs.net", f"Simulando compilação do Bytecode Luau:\n\n{script[:60]}...")

if __name__ == "__main__":
    app = ExecutorApp()
    app.mainloop()
