# interface_cel.py
import customtkinter as ctk
from sistema import Professor, Aluno, Adm, receber_servidor, enviar_servidor
from mensagens import obter_mensagem_por_nota
from tkinter import messagebox
from PIL import Image, ImageTk

professor = Professor()
aluno = Aluno()
adm = Adm()

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("dark-blue")


# -----------------------------
# UTILITÁRIOS DE RESPONSIVIDADE
# -----------------------------
def aplicar_responsividade(tela):
    """Configura janela: tenta fullscreen e permite redimensionamento."""
    try:
        largura = tela.winfo_screenwidth()
        altura = tela.winfo_screenheight()
    except Exception:
        largura, altura = 800, 600
    tela.geometry(f"{largura}x{altura}+0+0")
    tela.resizable(True, True)
    try:
        tela.attributes("-fullscreen", True)
    except Exception:
        pass
    tela.update_idletasks()


def criar_fundo_responsivo(tela, caminho_imagem):
    """
    Adiciona um label cobrindo toda a tela com imagem redimensionável.
    Mantém referência para evitar garbage-collection.
    """
    if not hasattr(tela, "_bg_refs"):
        tela._bg_refs = {}

    def carregar(largura, altura):
        try:
            img = Image.open(caminho_imagem)
        except Exception:
            img = Image.new("RGBA", (800, 600), (30, 30, 30, 255))
        largura = max(1, int(largura))
        altura = max(1, int(altura))
        try:
            img_r = img.resize((largura, altura), Image.LANCZOS)
        except Exception:
            img_r = img.resize((largura, altura))
        return ImageTk.PhotoImage(img_r)

    label = ctk.CTkLabel(tela, text="", anchor="nw")
    label.place(x=0, y=0, relwidth=1, relheight=1)

    def redim(event=None):
        try:
            w = tela.winfo_width() or tela.winfo_screenwidth()
            h = tela.winfo_height() or tela.winfo_screenheight()
        except Exception:
            w, h = 800, 600
        tkimg = carregar(w, h)
        label.configure(image=tkimg)
        tela._bg_refs["img"] = tkimg

    tela.bind("<Configure>", redim)
    redim()
    return label


def tamanhos_proporcionais(tela, ftitle_ratio=0.06, ftext_ratio=0.035, btn_h_ratio=0.07):
    """Retorna (largura, altura, fonte_titulo_px, fonte_texto_px, btn_height_px)."""
    largura = tela.winfo_screenwidth() or 800
    altura = tela.winfo_screenheight() or 600
    f_title = max(12, int(altura * ftitle_ratio))
    f_text = max(10, int(altura * ftext_ratio))
    btn_h = max(36, int(altura * btn_h_ratio))
    return int(largura), int(altura), f_title, f_text, btn_h


# -----------------------------
# UTILITÁRIOS DE POSICIONAMENTO (sem Frames)
# -----------------------------
def place_center_label(root, text, font, relx=0.5, rely=0.2):
    lbl = ctk.CTkLabel(root, text=text, font=font)
    lbl.place(relx=relx, rely=rely, anchor="center")
    return lbl


def place_center_entry(root, placeholder, font, relx=0.5, rely=0.3, relwidth=0.6, show=None):
    e = ctk.CTkEntry(root, placeholder_text=placeholder, font=font, show=show)
    e.place(relx=relx, rely=rely, anchor="center", relwidth=relwidth)
    return e


def place_center_optionmenu(root, variable, values, font, text, relx=0.5, rely=0.5, relwidth=0.6):
    lbl = ctk.CTkLabel(root, text=text, font=font)
    lbl.place(relx=relx, rely=rely - 0.04, anchor="center")
    om = ctk.CTkOptionMenu(root, variable=variable, values=values)
    om.place(relx=relx, rely=rely, anchor="center", relwidth=relwidth)
    return om


def place_center_button(root, text, largura_total, btn_h, command=None, relx=0.5, rely=0.8, fg_color=None, hover_color=None):
    btn_w = max(120, int(largura_total * 0.30))
    if fg_color and hover_color:
        btn = ctk.CTkButton(root, text=text, width=btn_w, height=btn_h, command=command,
                            fg_color=fg_color, hover_color=hover_color)
    else:
        btn = ctk.CTkButton(root, text=text, width=btn_w, height=btn_h, command=command)
    btn.place(relx=relx, rely=rely, anchor="center")
    return btn


def clear_window(win):
    """Remove todos os widgets filhos da janela."""
    for w in list(win.children.values()):
        try:
            w.place_forget()
            w.destroy()
        except Exception:
            pass


# -----------------------------
# INTERFACES (sem usar Frame; com CTkScrollableFrame nas 3 telas solicitadas)
# -----------------------------
def tela_profe_cadastro(tela_ant):
    try:
        tela_ant.destroy()
    except Exception:
        pass

    cadastro = ctk.CTk()
    aplicar_responsividade(cadastro)
    criar_fundo_responsivo(cadastro, "img.png")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(cadastro)

    place_center_label(cadastro, "Insira seus dados", ("Arial", f_title, "bold"), rely=0.12)
    nome = place_center_entry(cadastro, "Nome", ("Arial", f_text), rely=0.20)
    cpf = place_center_entry(cadastro, "CPF", ("Arial", f_text), rely=0.28)
    contato = place_center_entry(cadastro, "Contato", ("Arial", f_text), rely=0.36)
    senha = place_center_entry(cadastro, "Senha", ("Arial", f_text), rely=0.44, show="*")

    cursos = adm.listar_cursos() or ['Nenhum curso cadastrado']
    curso_var = ctk.StringVar(value=cursos[0])
    place_center_optionmenu(cadastro, curso_var, cursos, ("Arial", f_text), "Selecione o curso", rely=0.54)

    def profe_cadastro_action():
        profe_nome = nome.get().strip()
        profe_cpf = cpf.get().strip()
        profe_contato = contato.get().strip()
        profe_senha = senha.get().strip()
        profe_curso = curso_var.get()

        if not (profe_nome and profe_cpf and profe_contato and profe_senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        ve_profe = professor.cadastro(profe_nome, profe_cpf, profe_contato, profe_curso, profe_senha)
        if ve_profe == 3:
            messagebox.showinfo('Atenção', "Professor não cadastrado por um ADM")
        else:
            messagebox.showinfo("Sucesso", f"Professor {profe_nome} cadastrado no curso {profe_curso}!")
            tela_logar_professor(cadastro)

        for w in (nome, cpf, contato, senha):
            w.delete(0, "end")

    place_center_button(cadastro, "Cadastrar", largura, btn_h, command=profe_cadastro_action, rely=0.72)
    place_center_button(cadastro, "Voltar", largura, btn_h, command=lambda: index(cadastro), rely=0.82)

    cadastro.mainloop()


def tela_logar_professor(tela_ant):
    try:
        tela_ant.destroy()
    except Exception:
        pass

    logar = ctk.CTk()
    aplicar_responsividade(logar)
    criar_fundo_responsivo(logar, "img.png")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(logar)

    place_center_label(logar, "Login Professor", ("Arial", f_title, "bold"), rely=0.16)
    Log_cpf = place_center_entry(logar, "cpf", ("Arial", f_text), rely=0.28)
    log_senha = place_center_entry(logar, "senha", ("Arial", f_text), rely=0.38, show="*")

    def profe_login():
        profe_senha = log_senha.get().strip()
        profe_cpf = Log_cpf.get().strip()
        if not (profe_cpf and profe_senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        logado_profe = professor.logar(profe_cpf, profe_senha)
        if logado_profe == 1:
            messagebox.showinfo('Aviso', f"Professor com cpf {profe_cpf} não encontrado")
        elif logado_profe == 2:
            messagebox.showinfo('Aviso', "Senha inválida")
        elif isinstance(logado_profe, dict):
            log_senha.delete(0, "end")
            Log_cpf.delete(0, "end")
            logar.destroy()
            tela_professor_1(logado_profe)

    place_center_button(logar, "Logar", largura, btn_h, command=profe_login, rely=0.60)
    place_center_button(logar, "Cadastrar", largura, btn_h, command=lambda: tela_profe_cadastro(logar), rely=0.70)
    place_center_button(logar, "Voltar", largura, btn_h, command=lambda: index(logar), rely=0.80)

    logar.mainloop()


def tela_professor_1(logado_profe):
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Professor {logado_profe['professor_nome']}")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, f"Bem-vindo(a), {logado_profe['professor_nome']}", ("Arial", f_title), rely=0.14)
    place_center_button(tela, "Criar nova atividade", largura, btn_h,
                        command=lambda: tela_atividade_prof(tela, logado_profe), rely=0.30)
    place_center_button(tela, "Corrigir respostas", largura, btn_h,
                        command=lambda: tela_corrigir(tela, logado_profe), rely=0.42)
    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), index()], rely=0.54)

    tela.mainloop()


def tela_atividade_prof(tela_ant, logado_profe):
    """NOTA: Criar atividade — aqui não costuma listar muitos itens, mas a tela 'Fazer Atividade'
    (tela do aluno) terá scroll. Mantemos a criação de atividade simples."""
    try:
        tela_ant.destroy()
    except Exception:
        pass

    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title("Nova Atividade")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, "Digite o enunciado da atividade:", ("Arial", f_text), rely=0.10)

    # Textbox central (relativamente grande)
    chat = ctk.CTkTextbox(tela, font=("Arial", f_text))
    chat.place(relx=0.5, rely=0.30, anchor="center", relwidth=0.85, relheight=0.45)

    def salvar_atividade():
        texto = chat.get("1.0", "end").strip()
        if texto:
            professor.atividade(logado_profe["professor_nome"], texto)
            tela.destroy()
            messagebox.showinfo("Sucesso", "Atividade cadastrada!")
            tela_professor_1(logado_profe)
        else:
            messagebox.showwarning("Erro", "O campo não pode estar vazio.")

    place_center_button(tela, "Salvar atividade", largura, btn_h, command=salvar_atividade, rely=0.80)
    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_professor_1(logado_profe)], rely=0.88)

    tela.mainloop()


def tela_corrigir(tela_ant, prof_logado):
    """
    Corrigir Respostas — usa CTkScrollableFrame para exibir todas as respostas pendentes.
    Mantém funcionalidade original de atribuir nota/mensagem.
    """
    try:
        tela_ant.destroy()
    except Exception:
        pass

    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Corrigir Respostas - {prof_logado['professor_nome']}")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, f"Correção de Respostas - Professor {prof_logado['professor_nome']}", ("Arial", f_title, "bold"), rely=0.04)

    alunos = receber_servidor("get_aluno") or []
    respostas_para_corrigir = []
    for alu in alunos:
        for r in alu.get("respostas", []):
            if r.get("professor") == prof_logado["professor_nome"] and not r.get("corrigida", False):
                respostas_para_corrigir.append({
                    "aluno": alu["nome"],
                    "atividade": r.get("atividade"),
                    "resposta": r.get("resposta")
                })

    if not respostas_para_corrigir:
        place_center_label(tela, "Nenhuma resposta pendente no momento.", ("Arial", f_text), rely=0.40)
        place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_professor_1(prof_logado)], rely=0.70)
        tela.mainloop()
        return

    # Scrollable frame para mostrar todas as respostas
    scroll_h = 0.70
    sf = ctk.CTkScrollableFrame(tela, width=int(largura * 0.92), height=int(altura * scroll_h))
    sf.place(relx=0.5, rely=0.12 + scroll_h / 2, anchor="center")

    entradas_notas = []
    # cada bloco dentro do scrollable frame (empilhando com pack)
    y_idx = 0
    for item in respostas_para_corrigir:
        bloco = ctk.CTkLabel(sf, text=f"Aluno: {item['aluno']}", font=("Arial", f_text, "bold"), anchor="w")
        bloco.pack(fill="x", padx=8, pady=(10, 2))
        lbl_at = ctk.CTkLabel(sf, text=f"Atividade:\n{item['atividade']}", wraplength=int(largura * 0.8), justify="left")
        lbl_at.pack(fill="x", padx=12, pady=(0, 4))
        lbl_res = ctk.CTkLabel(sf, text=f"Resposta:\n{item['resposta']}", wraplength=int(largura * 0.8), justify="left", text_color="#bfbfbf")
        lbl_res.pack(fill="x", padx=12, pady=(0, 6))

        linha_nota = ctk.CTkLabel(sf, text="Nota (0-10):", anchor="w")
        linha_nota.pack(fill="x", padx=12, pady=(0, 2))
        entrada_nota = ctk.CTkEntry(sf, placeholder_text="ex: 8.5", width=140)
        entrada_nota.pack(padx=12, pady=(0, 6), anchor="w")

        ctk.CTkLabel(sf, text="Mensagem para o aluno (opcional):", anchor="w").pack(fill="x", padx=12, pady=(2, 2))
        entrada_msg = ctk.CTkEntry(sf, placeholder_text="Digite uma mensagem ou deixe vazio para automática")
        entrada_msg.pack(fill="x", padx=12, pady=(0, 10))

        entradas_notas.append({
            "aluno": item["aluno"],
            "atividade": item["atividade"],
            "entry": entrada_nota,
            "mensagem": entrada_msg
        })
        y_idx += 1

    def salvar_notas():
        nonlocal alunos
        if not entradas_notas:
            messagebox.showinfo("Aviso", "Não há respostas para corrigir.")
            return
        alunos = receber_servidor("get_aluno") or []
        alterou = False
        for item in entradas_notas:
            valor = item["entry"].get().strip()
            if valor == "":
                continue
            try:
                nota_val = float(valor)
                if not (0 <= nota_val <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Erro", f"Nota inválida para {item['aluno']}. Use número entre 0 e 10.")
                return
            msg = item["mensagem"].get().strip()
            if not msg:
                msg = obter_mensagem_por_nota(nota_val)
            for a in alunos:
                if a.get("nome") == item["aluno"]:
                    a.setdefault("notas", [])
                    for r in a.get("respostas", []):
                        if r.get("atividade") == item["atividade"] and r.get("professor") == prof_logado["professor_nome"] and not r.get("corrigida", False):
                            r["nota"] = nota_val
                            r["corrigida"] = True
                            r["mensagem"] = msg
                            a["notas"].append({
                                "professor": prof_logado["professor_nome"],
                                "atividade": item["atividade"],
                                "nota": nota_val,
                                "mensagem": msg
                            })
                            alterou = True
                            break
                    break
        if alterou:
            enviar_servidor("aluno", alunos)
            messagebox.showinfo("Sucesso", "Notas e mensagens salvas com sucesso!")
            tela.destroy()
            tela_professor_1(prof_logado)
        else:
            messagebox.showinfo("Aviso", "Nenhuma nota foi atribuída.")

    place_center_button(tela, "Salvar Notas", largura, btn_h, command=salvar_notas, rely=0.88)
    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_professor_1(prof_logado)], rely=0.94)

    tela.mainloop()


def tela_atribuir_nota(tela_ant, logado_profe):
    try:
        tela_ant.destroy()
    except Exception:
        pass
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title("Atribuir Nota")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, "Atribuir Nota a um Aluno", ("Arial", f_title), rely=0.12)
    nome_aluno = place_center_entry(tela, "Nome do Aluno", ("Arial", f_text), rely=0.24)
    atividade = place_center_entry(tela, "Nome ou texto da atividade", ("Arial", f_text), rely=0.34)
    nota = place_center_entry(tela, "Nota (0 - 10)", ("Arial", f_text), rely=0.44)

    def atribuir_nota_server(prof_name, nome_a, atividade_t, nota_num):
        alunos = receber_servidor("get_aluno")
        if alunos is None:
            return 0
        encontrado = False
        for a in alunos:
            if a.get("nome") == nome_a:
                encontrado = True
                a.setdefault("notas", [])
                updated = False
                for r in a.get("respostas", []):
                    if r.get("atividade") == atividade_t and r.get("professor") == prof_name:
                        r["nota"] = nota_num
                        r["corrigida"] = True
                        r["mensagem"] = obter_mensagem_por_nota(nota_num)
                        a["notas"].append({
                            "professor": prof_name,
                            "atividade": atividade_t,
                            "nota": nota_num,
                            "mensagem": r["mensagem"]
                        })
                        updated = True
                        break
                if not updated:
                    a["respostas"] = a.get("respostas", [])
                    a["respostas"].append({
                        "professor": prof_name,
                        "atividade": atividade_t,
                        "resposta": "",
                        "nota": nota_num,
                        "corrigida": True,
                        "mensagem": obter_mensagem_por_nota(nota_num)
                    })
                    a["notas"].append({
                        "professor": prof_name,
                        "atividade": atividade_t,
                        "nota": nota_num,
                        "mensagem": obter_mensagem_por_nota(nota_num)
                    })
                break
        if not encontrado:
            return 1
        enviar_servidor("aluno", alunos)
        return 2

    def salvar_nota_wrapper():
        nome_a = nome_aluno.get().strip()
        atividade_t = atividade.get().strip()
        nota_val = nota.get().strip()
        if not (nome_a and atividade_t and nota_val):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        try:
            nota_num = float(nota_val)
            if nota_num < 0 or nota_num > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite uma nota válida entre 0 e 10.")
            return
        resultado = atribuir_nota_server(logado_profe["professor_nome"], nome_a, atividade_t, nota_num)
        if resultado == 0:
            messagebox.showerror("Erro", "Servidor indisponível ou erro ao acessar alunos.")
        elif resultado == 1:
            messagebox.showerror("Erro", "Aluno não encontrado.")
        elif resultado == 2:
            messagebox.showinfo("Sucesso", f"Nota {nota_num} atribuída a {nome_a} na atividade '{atividade_t}'!")
            tela.destroy()
            tela_professor_1(logado_profe)

    place_center_button(tela, "Salvar Nota", largura, btn_h, command=salvar_nota_wrapper, rely=0.70)
    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_professor_1(logado_profe)], rely=0.80)

    tela.mainloop()


# -----------------------------
# TELAS DO ALUNO (com scroll nas 2 telas pedidas)
# -----------------------------
def tela_aluno_cadastro(tela_ant):
    try:
        tela_ant.destroy()
    except Exception:
        pass
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, "Insira seus dados", ("Arial", f_title), rely=0.10)
    nome = place_center_entry(tela, "Nome", ("Arial", f_text), rely=0.18)
    nascimento = place_center_entry(tela, "Data de Nascimento", ("Arial", f_text), rely=0.26)
    cpf = place_center_entry(tela, "CPF", ("Arial", f_text), rely=0.34)
    contato = place_center_entry(tela, "Telefone", ("Arial", f_text), rely=0.42)
    endereco = place_center_entry(tela, "Endereço", ("Arial", f_text), rely=0.50)
    senha = place_center_entry(tela, "Senha", ("Arial", f_text), rely=0.58, show="*")

    cursos = adm.listar_cursos() or ['Nenhum curso cadastrado']
    curso_var = ctk.StringVar(value=cursos[0])
    place_center_optionmenu(tela, curso_var, cursos, ("Arial", f_text), "Selecione o Curso", rely=0.66)

    def aluno_cadastrar_action():
        aluno_nome = nome.get().strip()
        aluno_cpf = cpf.get().strip()
        aluno_contato = contato.get().strip()
        data_nascimento = nascimento.get().strip()
        aluno_endereco = endereco.get().strip()
        aluno_senha = senha.get().strip()
        aluno_curso = curso_var.get()
        if not (aluno_nome and aluno_cpf and aluno_contato and data_nascimento and aluno_senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        aluno.cadastrar_aluno(aluno_nome, aluno_cpf, data_nascimento, aluno_endereco, aluno_contato, aluno_senha, aluno_curso)
        messagebox.showinfo("Sucesso", f"Aluno '{aluno_nome}' cadastrado no curso '{aluno_curso}'!")
        for w in (nome, cpf, contato, nascimento, endereco, senha):
            w.delete(0, "end")
        curso_var.set(cursos[0])

    place_center_button(tela, "Cadastrar", largura, btn_h, command=aluno_cadastrar_action, rely=0.82)
    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: index(tela), rely=0.90)

    tela.mainloop()


def tela_logar_aluno(tela_ant):
    try:
        tela_ant.destroy()
    except Exception:
        pass
    logar = ctk.CTk()
    aplicar_responsividade(logar)
    criar_fundo_responsivo(logar, "img.png")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(logar)

    place_center_label(logar, "Login Aluno", ("Arial", f_title, "bold"), rely=0.16)
    Log_cpf = place_center_entry(logar, "cpf", ("Arial", f_text), rely=0.28)
    log_senha = place_center_entry(logar, "senha", ("Arial", f_text), rely=0.38, show="*")

    def aluno_login():
        aluno_senha = log_senha.get().strip()
        aluno_cpf = Log_cpf.get().strip()
        if not (aluno_cpf and aluno_senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        logado_aluno = aluno.logar_aluno(aluno_cpf, aluno_senha)
        if logado_aluno == 1:
            messagebox.showinfo('Aviso', f"Aluno com cpf {aluno_cpf} não encontrado")
        elif logado_aluno == 2:
            messagebox.showinfo('Aviso', "Senha inválida")
        elif isinstance(logado_aluno, dict):
            log_senha.delete(0, "end")
            Log_cpf.delete(0, "end")
            logar.destroy()
            tela_aluno_principal(logado_aluno)

    place_center_button(logar, "Logar", largura, btn_h, command=aluno_login, rely=0.60)
    place_center_button(logar, "Cadastrar", largura, btn_h, command=lambda: tela_aluno_cadastro(logar), rely=0.70)
    place_center_button(logar, "Sair", largura, btn_h, command=lambda: index(logar), rely=0.80)

    logar.mainloop()


def tela_aluno_principal(logado_aluno):
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Aluno {logado_aluno['nome']}")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, f"Bem-vindo(a), {logado_aluno['nome']}", ("Arial", f_title), rely=0.12)
    place_center_button(tela, "Fazer Atividade", largura, btn_h, command=lambda: [tela.destroy(), tela_aluno_1(logado_aluno)], rely=0.28)
    place_center_button(tela, "Ver Média das Notas", largura, btn_h, command=lambda: [tela.destroy(), tela_media_notas(logado_aluno)], rely=0.40)
    place_center_button(tela, "Ver Notas Detalhadas", largura, btn_h, command=lambda: [tela.destroy(), tela_aluno_ver_notas_atividades(logado_aluno)], rely=0.52)
    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), index()], rely=0.64)

    tela.mainloop()


def tela_media_notas(logado_aluno):
    aluno_obj = Aluno()
    medias = aluno_obj.calcular_media(logado_aluno["nome"])
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Média das Notas - {logado_aluno['nome']}")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, "Média das Notas por Professor", ("Arial", f_title), rely=0.12)
    if not medias:
        place_center_label(tela, "Nenhuma nota registrada ainda.", ("Arial", f_text), rely=0.30)
    else:
        y = 0.26
        for prof, media in medias.items():
            place_center_label(tela, f"{prof}: {media:.2f}", ("Arial", f_text), rely=y)
            mensagem = obter_mensagem_por_nota(media)
            place_center_label(tela, mensagem, ("Arial", int(f_text * 0.9)), rely=y + 0.04)
            y += 0.12

    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)], rely=0.86)
    tela.mainloop()


def tela_aluno_ver_notas_atividades(logado_aluno):
    """
    Ver Notas Detalhadas — usa CTkScrollableFrame para mostrar todas as notas.
    """
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Notas Detalhadas - {logado_aluno['nome']}")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, f"Notas de {logado_aluno['nome']}", ("Arial", f_title), rely=0.06)

    alunos = receber_servidor("get_aluno") or []
    notas = []
    for al in alunos:
        if al["nome"] == logado_aluno["nome"]:
            notas = al.get("notas", [])
            break

    if not notas:
        place_center_label(tela, "Nenhuma nota registrada ainda.", ("Arial", f_text), rely=0.30)
        place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)], rely=0.80)
        tela.mainloop()
        return

    scroll_h = 0.72
    sf = ctk.CTkScrollableFrame(tela, width=int(largura * 0.92), height=int(altura * scroll_h))
    sf.place(relx=0.5, rely=0.12 + scroll_h / 2, anchor="center")

    for item in notas:
        lbl_prof = ctk.CTkLabel(sf, text=f"Professor: {item['professor']}", font=("Arial", f_text, "bold"), anchor="w")
        lbl_prof.pack(fill="x", padx=8, pady=(8, 2))
        lbl_at = ctk.CTkLabel(sf, text=f"Atividade:\n{item['atividade']}", wraplength=int(largura * 0.8), justify="left")
        lbl_at.pack(fill="x", padx=12, pady=(0, 4))
        lbl_nota = ctk.CTkLabel(sf, text=f"Nota: {item['nota']}")
        lbl_nota.pack(fill="x", padx=12, pady=(0, 4))
        mensagem = item.get('mensagem', obter_mensagem_por_nota(float(item['nota'])) if item.get('nota') is not None else "")
        lbl_msg = ctk.CTkLabel(sf, text=f"Mensagem:\n{mensagem}", wraplength=int(largura * 0.8), justify="left", text_color="#bfbfbf")
        lbl_msg.pack(fill="x", padx=12, pady=(0, 8))

    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)], rely=0.92)
    tela.mainloop()


def tela_aluno_1(logado_aluno):
    """
    Fazer Atividade — usa CTkScrollableFrame para listar todas as atividades disponíveis
    e permitir que o aluno responda cada uma.
    """
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Aluno {logado_aluno['nome']}")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, f"Bem-vindo(a), {logado_aluno['nome']}", ("Arial", f_title), rely=0.06)

    atividades = aluno.ver_atividades(logado_aluno["nome"]) or []
    if not atividades:
        place_center_label(tela, "Nenhuma atividade disponível.", ("Arial", f_text), rely=0.40)
        place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)], rely=0.80)
        tela.mainloop()
        return

    scroll_h = 0.78
    sf = ctk.CTkScrollableFrame(tela, width=int(largura * 0.92), height=int(altura * scroll_h))
    sf.place(relx=0.5, rely=0.10 + scroll_h / 2, anchor="center")

    for atv in atividades:
        lbl_prof = ctk.CTkLabel(sf, text=f"Professor: {atv['professor']}", font=("Arial", f_text, "bold"), anchor="w")
        lbl_prof.pack(fill="x", padx=8, pady=(8, 2))
        lbl_txt = ctk.CTkLabel(sf, text=f"Atividade:\n{atv['texto']}", wraplength=int(largura * 0.8), justify="left")
        lbl_txt.pack(fill="x", padx=12, pady=(0, 6))

        resposta_box = ctk.CTkTextbox(sf, height=120)
        resposta_box.pack(padx=12, pady=(0, 6), fill="x")

        def enviar_resposta(atv_ref=atv, box=resposta_box):
            resposta = box.get("1.0", "end").strip()
            if resposta:
                aluno.enviar_resposta(logado_aluno["nome"], atv_ref["professor"], resposta, atv_ref["texto"])
                messagebox.showinfo("Sucesso", "Resposta enviada com sucesso!")
                # depois de enviar, atualiza a tela (reabre)
                tela.destroy()
                tela_aluno_1(logado_aluno)
            else:
                messagebox.showwarning("Erro", "Digite uma resposta antes de enviar.")

        btn = ctk.CTkButton(sf, text="Enviar Resposta", width=max(140, int(largura * 0.30)), height=btn_h, command=enviar_resposta)
        btn.pack(pady=(0, 8))

    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)], rely=0.92)
    tela.mainloop()


def tela_ver_notas(tela_ant, logado_aluno):
    try:
        tela_ant.destroy()
    except Exception:
        pass
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title("Minhas Notas")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    place_center_label(tela, f"Notas de {logado_aluno['nome']}", ("Arial", f_title), rely=0.10)

    alunos = receber_servidor("get_aluno") or []
    notas = []
    for al in alunos:
        if al["nome"] == logado_aluno["nome"]:
            notas = al.get("notas", [])
            break

    if not notas:
        place_center_label(tela, "Você ainda não possui notas registradas.", ("Arial", f_text), rely=0.30)
    else:
        y = 0.22
        for item in notas:
            place_center_label(tela, f"Professor: {item['professor']}", ("Arial", f_text, "bold"), rely=y)
            place_center_label(tela, f"Atividade: {item['atividade']}", ("Arial", int(f_text * 0.95)), rely=y + 0.04)
            place_center_label(tela, f"Nota: {item['nota']}", ("Arial", f_text), rely=y + 0.08)
            y += 0.16
            if y > 0.75:
                place_center_label(tela, f"...{len(notas) - int((y - 0.22) / 0.16)} itens não mostrados", ("Arial", int(f_text * 0.9)), rely=0.78)
                break

    place_center_button(tela, "Voltar", largura, btn_h, command=lambda: [tela.destroy(), tela_aluno_1(logado_aluno)], rely=0.88)
    tela.mainloop()


# -----------------------------
# TELAS ADM (sem frames)
# -----------------------------
def tela_adm(tela_ant):
    try:
        tela_ant.destroy()
    except Exception:
        pass
    tela_adm = ctk.CTk()
    aplicar_responsividade(tela_adm)
    criar_fundo_responsivo(tela_adm, "img.png")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela_adm)

    place_center_label(tela_adm, "Área Administrativa", ("Arial", f_title), rely=0.12)
    nome = place_center_entry(tela_adm, "Nome do Professor", ("Arial", f_text), rely=0.22)
    cpf = place_center_entry(tela_adm, "CPF do Professor", ("Arial", f_text), rely=0.30)

    place_center_label(tela_adm, "É Coordenador?", ("Arial", f_text), rely=0.38)
    var_coord = ctk.BooleanVar(value=False)
    switch_coord = ctk.CTkSwitch(tela_adm, text="Coordenador", variable=var_coord, onvalue=True, offvalue=False)
    switch_coord.place(relx=0.5, rely=0.44, anchor="center")

    def cadastro_cpf_prof():
        nome_profe = nome.get().strip()
        profe_cpf = cpf.get().strip()
        is_coord = var_coord.get()
        if not (nome_profe and profe_cpf):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        adm.cadastrar_professor_cpf(nome_profe, profe_cpf, is_coord)
        messagebox.showinfo("Sucesso", f"Professor '{nome_profe}' cadastrado! Coordenador: {is_coord}")
        nome.delete(0, "end")
        cpf.delete(0, "end")
        var_coord.set(False)

    place_center_button(tela_adm, "Cadastrar Professor", largura, btn_h, command=cadastro_cpf_prof, rely=0.64)
    place_center_button(tela_adm, "Cadastrar Curso", largura, btn_h, command=lambda: tela_cadastrar_curso(tela_adm), rely=0.74)
    place_center_button(tela_adm, "Voltar", largura, btn_h, command=lambda: index(tela_adm), rely=0.84)

    tela_adm.mainloop()


def tela_cadastrar_curso(tela_ant):
    try:
        tela_ant.destroy()
    except Exception:
        pass
    tela_curso = ctk.CTk()
    aplicar_responsividade(tela_curso)
    criar_fundo_responsivo(tela_curso, "img.png")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela_curso)

    place_center_label(tela_curso, "Cadastro de Curso", ("Arial", f_title), rely=0.12)
    nome_curso = place_center_entry(tela_curso, "Nome do Curso", ("Arial", f_text), rely=0.22)
    carga_hora = place_center_entry(tela_curso, "Carga Horária (em horas)", ("Arial", f_text), rely=0.30)

    coordenadores = adm.listar_coordenadores() or ['Nenhum coordenador disponível']
    coord_var = ctk.StringVar(value=coordenadores[0])
    place_center_optionmenu(tela_curso, coord_var, coordenadores, ("Arial", f_text), "Selecione o Coordenador", rely=0.40)

    def cadastrar_curso():
        nome = nome_curso.get().strip()
        coordenador = coord_var.get()
        carga = carga_hora.get().strip()
        if not (nome and coordenador and carga):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        try:
            adm.cadastrar_curso(nome, coordenador, carga)
            messagebox.showinfo("Sucesso", f"Curso '{nome}' cadastrado com sucesso!")
            nome_curso.delete(0, "end")
            carga_hora.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    place_center_button(tela_curso, "Cadastrar Curso", largura, btn_h, command=cadastrar_curso, rely=0.70)
    place_center_button(tela_curso, "Voltar", largura, btn_h, command=lambda: index(tela_curso), rely=0.80)

    tela_curso.mainloop()


# -----------------------------
# TELA INICIAL (INDEX)
# -----------------------------
def index(tela_ant=None):
    if tela_ant:
        try:
            tela_ant.destroy()
        except Exception:
            pass
    janela = ctk.CTk()
    aplicar_responsividade(janela)
    criar_fundo_responsivo(janela, "img.png")
    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(janela)

    place_center_label(janela, "Sistema - Menu", ("Arial", f_title), rely=0.12)
    place_center_button(janela, "Professor", largura, btn_h, command=lambda: tela_logar_professor(janela), rely=0.30)
    place_center_button(janela, "Administração", largura, btn_h, command=lambda: tela_adm(janela), rely=0.42)
    place_center_button(janela, "Aluno", largura, btn_h, command=lambda: tela_logar_aluno(janela), rely=0.54)

    def fechar_e_sair():
        try:
            janela.attributes("-fullscreen", False)
        except Exception:
            pass
        janela.destroy()

    place_center_button(janela, "Sair", largura, btn_h, command=fechar_e_sair, rely=0.70, fg_color="#aa3333", hover_color="#cc4444")
    janela.mainloop()


# -----------------------------
# PONTO DE ENTRADA
# -----------------------------
if __name__ == "__main__":
    index()
