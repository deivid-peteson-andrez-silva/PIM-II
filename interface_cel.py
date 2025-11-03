# interface.py
# Requisitos: sistema.py deve exportar Professor, Aluno, Adm, receber_servidor, enviar_servidor
# servidor LAM deve aceitar/retornar os tipos: "get_aluno"/"aluno", "get_professor"/"professor", "get_adm"/"adm"

from sistema import Professor, Aluno, Adm, receber_servidor, enviar_servidor
professor = Professor()
aluno = Aluno()
adm = Adm()

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from mensagens import obter_mensagem_por_nota

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("dark-blue")


# -----------------------------
# UTILITÁRIOS DE RESPONSIVIDADE
# -----------------------------
def aplicar_responsividade(tela):
    """
    Configura a janela para ocupar 100% da tela e prepara para usar dimensões proporcionais.
    (Não altera lógica do programa; apenas configura visual).
    """
    # tornar fullscreen (simula comportamento de app em celular / emulador)
    try:
        largura = tela.winfo_screenwidth()
        altura = tela.winfo_screenheight()
    except Exception:
        largura, altura = 800, 600

    tela.geometry(f"{largura}x{altura}+0+0")
    tela.resizable(True, True)
    # Alguns sistemas aceitam -fullscreen; mantemos para simular app
    try:
        tela.attributes("-fullscreen", True)
    except Exception:
        # se não permitir, ainda deixamos maximizada
        pass

    # Força atualização para obter tamanhos corretos
    tela.update_idletasks()


def criar_fundo_responsivo(tela, caminho_imagem):
    """
    Adiciona um fundo responsivo a qualquer CTk janela.
    Mantém referência da imagem para não ser garbage-collected.
    Escala com LANCZOS para melhor qualidade.
    """
    # container para armazenar imagem atual (atrelado à janela)
    if not hasattr(tela, "_bg_refs"):
        tela._bg_refs = {}

    def carregar_imagem(largura, altura):
        try:
            img_original = Image.open(caminho_imagem)
        except Exception:
            img_original = Image.new("RGBA", (800, 600), (30, 30, 30, 255))
        # evita largura/altura zero
        largura = max(1, int(largura))
        altura = max(1, int(altura))
        try:
            img_resized = img_original.resize((largura, altura), Image.LANCZOS)
        except Exception:
            img_resized = img_original.resize((largura, altura))
        img_tk = ImageTk.PhotoImage(img_resized)
        return img_tk

    # Cria label de fundo (vazio) que preenche a tela
    label_fundo = ctk.CTkLabel(tela, text="", anchor="nw")
    label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    # A função que redimensiona a imagem quando a janela muda de tamanho
    def redimensionar(event=None):
        try:
            largura = tela.winfo_width() or tela.winfo_screenwidth()
            altura = tela.winfo_height() or tela.winfo_screenheight()
        except Exception:
            largura, altura = 800, 600
        img_tk = carregar_imagem(largura, altura)
        label_fundo.configure(image=img_tk)
        # guarda referência
        tela._bg_refs["img_tk"] = img_tk

    # liga o evento de configure (resize)
    tela.bind("<Configure>", redimensionar)

    # chamada inicial para setar imagem
    redimensionar()
    return label_fundo


# -----------------------------
# AUX: cálculo de fontes e tamanhos proporcionais
# -----------------------------
def tamanhos_proporcionais(tela, font_ratio_title=0.06, font_ratio_text=0.035, btn_height_ratio=0.07):
    """
    Retorna tupla (largura, altura, fonte_titulo, fonte_texto, bot_height_px) baseada no tamanho da tela.
    """
    largura = tela.winfo_screenwidth() or 800
    altura = tela.winfo_screenheight() or 600
    fonte_titulo = max(12, int(altura * font_ratio_title))
    fonte_texto = max(10, int(altura * font_ratio_text))
    btn_height = max(36, int(altura * btn_height_ratio))
    return int(largura), int(altura), fonte_titulo, fonte_texto, btn_height


# -----------------------------
# INTERFACES (mantendo lógica original)
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

    frame = ctk.CTkFrame(cadastro, fg_color="#1a1a1a", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.88)

    txt = ctk.CTkLabel(frame, text='Insira seus dados', font=("Arial", f_title, "bold"))
    txt.pack(padx=10, pady=(10, 8))

    nome = ctk.CTkEntry(frame, placeholder_text='Nome', font=("Arial", f_text))
    nome.pack(padx=10, pady=6, fill="x")

    cpf = ctk.CTkEntry(frame, placeholder_text='CPF', font=("Arial", f_text))
    cpf.pack(padx=10, pady=6, fill="x")

    contato = ctk.CTkEntry(frame, placeholder_text='Contato', font=("Arial", f_text))
    contato.pack(padx=10, pady=6, fill="x")

    senha = ctk.CTkEntry(frame, placeholder_text='Senha', show='*', font=("Arial", f_text))
    senha.pack(padx=10, pady=6, fill="x")

    cursos = adm.listar_cursos()
    if not cursos:
        cursos = ['Nenhum curso cadastrado']

    curso_var = ctk.StringVar(value=cursos[0])
    ctk.CTkLabel(frame, text="Selecione o curso", font=("Arial", f_text)).pack(pady=(10, 0))
    menu_cursos = ctk.CTkOptionMenu(frame, variable=curso_var, values=cursos)
    menu_cursos.pack(padx=10, pady=8, fill="x")

    def profe_cadastro():
        profe_nome = nome.get()
        profe_cpf = cpf.get()
        profe_contato = contato.get()
        profe_senha = senha.get()
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

        nome.delete(0, "end")
        cpf.delete(0, "end")
        contato.delete(0, "end")
        senha.delete(0, "end")

    btn_cadastrar = ctk.CTkButton(frame, text="Cadastrar", command=profe_cadastro, height=btn_h)
    btn_cadastrar.pack(pady=12, padx=12, fill="x")

    tela_index = ctk.CTkButton(frame, text="Voltar", command=lambda: index(cadastro), height=btn_h)
    tela_index.pack(pady=6, padx=12, fill="x")

    cadastro.mainloop()


def tela_logar_professor(tela_ant):
    try:
        tela_ant.destroy()
    except Exception:
        pass

    logar_professor = ctk.CTk()
    aplicar_responsividade(logar_professor)
    criar_fundo_responsivo(logar_professor, "img.png")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(logar_professor)

    frame = ctk.CTkFrame(logar_professor, fg_color="#1a1a1a", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.5)

    Log_cpf = ctk.CTkEntry(frame, placeholder_text='cpf', font=("Arial", f_text))
    Log_cpf.pack(padx=10, pady=10, fill="x")
    log_senha = ctk.CTkEntry(frame, placeholder_text='senha', show='*', font=("Arial", f_text))
    log_senha.pack(padx=10, pady=10, fill="x")

    def profe_login():
        profe_senha = log_senha.get()
        profe_cpf = Log_cpf.get()

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
            logar_professor.destroy()
            tela_professor_1(logado_profe)

    btn_logar_prof = ctk.CTkButton(frame, text="logar", command=profe_login, height=btn_h)
    btn_logar_prof.pack(pady=8, padx=10, fill="x")

    btn_prof_cadastro = ctk.CTkButton(frame, text="cadastrar", command=lambda: tela_profe_cadastro(logar_professor), height=btn_h)
    btn_prof_cadastro.pack(pady=6, padx=10, fill="x")

    tela_index = ctk.CTkButton(frame, text="voltar", command=lambda: index(logar_professor), height=btn_h)
    tela_index.pack(pady=6, padx=10, fill="x")

    logar_professor.mainloop()


def tela_professor_1(logado_profe):
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Professor {logado_profe['professor_nome']}")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    frame = ctk.CTkFrame(tela, fg_color="#00000060", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)

    lbl = ctk.CTkLabel(frame, text=f"Bem-vindo(a), {logado_profe['professor_nome']}", font=("Arial", f_title))
    lbl.pack(pady=16)

    btn_atividade = ctk.CTkButton(frame, text="Criar nova atividade",
                                  command=lambda: tela_atividade_prof(tela, logado_profe),
                                  height=btn_h)
    btn_atividade.pack(pady=10, padx=20, fill="x")

    btn_corrigir = ctk.CTkButton(frame, text="Corrigir respostas",
                                 command=lambda: tela_corrigir(tela, logado_profe),
                                 height=btn_h)
    btn_corrigir.pack(pady=10, padx=20, fill="x")

    ctk.CTkButton(frame, text="Voltar", command=lambda: [tela.destroy(), index()], height=btn_h).pack(pady=10, padx=20, fill="x")
    tela.mainloop()


def tela_atividade_prof(tela_ant, logado_profe):
    try:
        tela_ant.destroy()
    except Exception:
        pass

    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title("Nova Atividade")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    frame = ctk.CTkFrame(tela, fg_color="#1a1a1a", corner_radius=10)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.9)

    lbl = ctk.CTkLabel(frame, text="Digite o enunciado da atividade:", font=("Arial", f_text))
    lbl.pack(pady=10)

    chat = ctk.CTkTextbox(frame, width=int(largura * 0.85), height=int(altura * 0.45), font=("Arial", f_text))
    chat.pack(pady=10, padx=10, fill="both", expand=False)

    def salvar_atividade():
        texto = chat.get("1.0", "end").strip()
        if texto:
            # atualiza no servidor via método Professor.atividade (que chama enviar_servidor)
            professor.atividade(logado_profe["professor_nome"], texto)
            tela.destroy()  # destrói a tela de atividade antes de abrir a próxima
            messagebox.showinfo("Sucesso", "Atividade cadastrada!")
            tela_professor_1(logado_profe)  # abre a tela do professor
        else:
            messagebox.showwarning("Erro", "O campo não pode estar vazio.")

    btn_salvar = ctk.CTkButton(frame, text="Salvar atividade", command=salvar_atividade, height=btn_h)
    btn_salvar.pack(pady=12, padx=12, fill="x")

    btn_voltar = ctk.CTkButton(frame, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(logado_profe)], height=btn_h)
    btn_voltar.pack(pady=6, padx=12, fill="x")

    tela.mainloop()


def tela_corrigir(tela_ant, prof_logado):
    try:
        tela_ant.destroy()
    except Exception:
        pass

    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Corrigir Respostas - {prof_logado['professor_nome']}")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    ctk.CTkLabel(
        tela,
        text=f"Correção de Respostas - Professor {prof_logado['professor_nome']}",
        font=("Arial", f_title, "bold")
    ).pack(pady=12)

    # pegar alunos do servidor
    alunos = receber_servidor("get_aluno") or []

    if not alunos:
        ctk.CTkLabel(tela, text="Nenhum aluno cadastrado no servidor.", font=("Arial", f_text)).pack(pady=20)
        ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(prof_logado)], height=btn_h).pack(pady=10)
        tela.mainloop()
        return

    respostas_para_corrigir = []
    for alu in alunos:
        for r in alu.get("respostas", []):
            if r.get("professor") == prof_logado["professor_nome"] and not r.get("corrigida", False):
                respostas_para_corrigir.append({
                    "aluno": alu["nome"],
                    "atividade": r.get("atividade"),
                    "resposta": r.get("resposta")
                })

    frame_scroll = ctk.CTkScrollableFrame(tela, width=int(largura * 0.95), height=int(altura * 0.65))
    frame_scroll.pack(padx=15, pady=10, fill="both", expand=True)

    entradas_notas = []

    if not respostas_para_corrigir:
        ctk.CTkLabel(frame_scroll, text="Nenhuma resposta pendente no momento.", font=("Arial", f_text)).pack(pady=20)
        ctk.CTkButton(frame_scroll, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(prof_logado)], height=btn_h).pack(pady=8)
        tela.mainloop()
        return
    else:
        for item in respostas_para_corrigir:
            bloco = ctk.CTkFrame(frame_scroll, corner_radius=8)
            bloco.pack(fill="x", padx=8, pady=8)

            ctk.CTkLabel(bloco, text=f"Aluno: {item['aluno']}", font=("Arial", f_text, "bold")).pack(anchor="w", padx=8, pady=4)
            ctk.CTkLabel(bloco, text=f"Atividade:\n{item['atividade']}", wraplength=int(largura * 0.9), justify="left", font=("Arial", f_text)).pack(anchor="w", padx=12)
            ctk.CTkLabel(bloco, text=f"Resposta:\n{item['resposta']}", wraplength=int(largura * 0.9), justify="left",
                         text_color="#bfbfbf", font=("Arial", f_text)).pack(anchor="w", padx=12, pady=(6, 4))

            # Entrada da nota
            linha_nota = ctk.CTkFrame(bloco)
            linha_nota.pack(anchor="w", padx=12, pady=6, fill="x")
            ctk.CTkLabel(linha_nota, text="Nota (0-10):", font=("Arial", f_text)).pack(side="left", padx=(0, 6))
            entrada_nota = ctk.CTkEntry(linha_nota, placeholder_text="ex: 8.5", width=140, font=("Arial", f_text))
            entrada_nota.pack(side="left")

            # Entrada da mensagem opcional
            ctk.CTkLabel(bloco, text="Mensagem para o aluno (opcional):", font=("Arial", f_text)).pack(anchor="w", padx=12, pady=(6, 2))
            entrada_msg = ctk.CTkEntry(bloco, placeholder_text="Digite uma mensagem ou deixe vazio para automática", width=int(largura * 0.6), font=("Arial", f_text))
            entrada_msg.pack(anchor="w", padx=12, pady=(0, 6))

            entradas_notas.append({
                "aluno": item["aluno"],
                "atividade": item["atividade"],
                "entry": entrada_nota,
                "mensagem": entrada_msg
            })

    def salvar_notas():
        nonlocal alunos
        if not entradas_notas:
            messagebox.showinfo("Aviso", "Não há respostas para corrigir.")
            return

        # Recarregar alunos do servidor para garantir atualização
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

            # Mensagem: se o professor digitou, usa; senão automática
            msg = item["mensagem"].get().strip()
            if not msg:
                msg = obter_mensagem_por_nota(nota_val)

            # Atualiza aluno localmente (na lista 'alunos')
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
            # envia lista inteira de alunos para o servidor salvar
            enviar_servidor("aluno", alunos)
            messagebox.showinfo("Sucesso", "Notas e mensagens salvas com sucesso!")
            tela.destroy()
            tela_professor_1(prof_logado)
        else:
            messagebox.showinfo("Aviso", "Nenhuma nota foi atribuída.")

    botoes = ctk.CTkFrame(tela)
    botoes.pack(pady=10)

    ctk.CTkButton(botoes, text="Salvar Notas", command=salvar_notas, width=160, height=btn_h).pack(side="left", padx=8)
    ctk.CTkButton(botoes, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(prof_logado)], width=160, height=btn_h).pack(side="left", padx=8)

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

    frame = ctk.CTkFrame(tela, fg_color="#1a1a1a", corner_radius=10)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)

    ctk.CTkLabel(frame, text="Atribuir Nota a um Aluno", font=("Arial", f_title)).pack(pady=15)

    nome_aluno = ctk.CTkEntry(frame, placeholder_text="Nome do Aluno", font=("Arial", f_text))
    nome_aluno.pack(pady=8, padx=12, fill="x")

    atividade = ctk.CTkEntry(frame, placeholder_text="Nome ou texto da atividade", font=("Arial", f_text))
    atividade.pack(pady=8, padx=12, fill="x")

    nota = ctk.CTkEntry(frame, placeholder_text="Nota (0 - 10)", font=("Arial", f_text))
    nota.pack(pady=8, padx=12, fill="x")

    def atribuir_nota_server(prof_name, nome_a, atividade_t, nota_num):
        """
        Função local para atribuir nota via servidor:
        - busca lista de alunos (get_aluno)
        - encontra aluno e responde/atualiza
        - envia lista atualizada para servidor (aluno)
        Retorna: 0 = arquivo / servidor não disponível, 1 = aluno não encontrado, 2 = sucesso
        """
        alunos = receber_servidor("get_aluno")
        if alunos is None:
            return 0
        encontrado = False
        for a in alunos:
            if a.get("nome") == nome_a:
                encontrado = True
                # adiciona notas/atualiza respostas
                a.setdefault("notas", [])
                updated = False
                for r in a.get("respostas", []):
                    if r.get("atividade") == atividade_t and r.get("professor") == prof_name:
                        r["nota"] = nota_num
                        r["corrigida"] = True
                        # gerar mensagem automática
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
                    # se aluno não tiver respondido essa atividade, adiciona a nota diretamente
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
        # envia para servidor
        enviar_servidor("aluno", alunos)
        return 2

    def salvar_nota():
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

        resultado = atribuir_nota_server(
            logado_profe["professor_nome"],
            nome_a,
            atividade_t,
            nota_num
        )

        if resultado == 0:
            messagebox.showerror("Erro", "Servidor indisponível ou erro ao acessar alunos.")
        elif resultado == 1:
            messagebox.showerror("Erro", "Aluno não encontrado.")
        elif resultado == 2:
            messagebox.showinfo("Sucesso", f"Nota {nota_num} atribuída a {nome_a} na atividade '{atividade_t}'!")
            tela.destroy()
            tela_professor_1(logado_profe)

    btn_salvar = ctk.CTkButton(frame, text="Salvar Nota", command=salvar_nota, height=btn_h)
    btn_salvar.pack(pady=12, padx=12, fill="x")

    btn_voltar = ctk.CTkButton(frame, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(logado_profe)], height=btn_h)
    btn_voltar.pack(pady=6, padx=12, fill="x")

    tela.mainloop()


# -----------------------------
# TELAS DO ALUNO (mantida lógica)
# -----------------------------
def tela_aluno_cadastro(tela_ant):
    try:
        tela_ant.destroy()
    except Exception:
        pass

    tela_aluno_ca = ctk.CTk()
    aplicar_responsividade(tela_aluno_ca)
    criar_fundo_responsivo(tela_aluno_ca, "img.png")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela_aluno_ca)

    frame = ctk.CTkFrame(tela_aluno_ca, fg_color="#1a1a1a", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    txt = ctk.CTkLabel(frame, text='Insira seus dados', font=("Arial", f_title))
    txt.pack(padx=10, pady=10)

    nome = ctk.CTkEntry(frame, placeholder_text='Nome', font=("Arial", f_text))
    nome.pack(padx=10, pady=6, fill="x")
    nascimento = ctk.CTkEntry(frame, placeholder_text='Data de Nascimento', font=("Arial", f_text))
    nascimento.pack(padx=10, pady=6, fill="x")
    cpf = ctk.CTkEntry(frame, placeholder_text='CPF', font=("Arial", f_text))
    cpf.pack(padx=10, pady=6, fill="x")
    contato = ctk.CTkEntry(frame, placeholder_text='Telefone', font=("Arial", f_text))
    contato.pack(padx=10, pady=6, fill="x")
    endereco = ctk.CTkEntry(frame, placeholder_text='Endereço', font=("Arial", f_text))
    endereco.pack(padx=10, pady=6, fill="x")
    senha = ctk.CTkEntry(frame, placeholder_text='Senha', show='*', font=("Arial", f_text))
    senha.pack(padx=10, pady=6, fill="x")

    cursos = adm.listar_cursos()
    if not cursos:
        cursos = ['Nenhum curso cadastrado']
    curso_var = ctk.StringVar(value=cursos[0])
    ctk.CTkLabel(frame, text="Selecione o Curso", font=("Arial", f_text)).pack(pady=(10, 0))
    menu_cursos = ctk.CTkOptionMenu(frame, variable=curso_var, values=cursos)
    menu_cursos.pack(padx=10, pady=8, fill="x")

    def aluno_cadastro():
        aluno_nome = nome.get()
        aluno_cpf = cpf.get()
        aluno_contato = contato.get()
        data_nascimento = nascimento.get()
        aluno_endereco = endereco.get()
        aluno_senha = senha.get()
        aluno_curso = curso_var.get()

        if not (aluno_nome and aluno_cpf and aluno_contato and data_nascimento and aluno_senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        aluno.cadastrar_aluno(aluno_nome, aluno_cpf, data_nascimento, aluno_endereco, aluno_contato, aluno_senha, aluno_curso)
        messagebox.showinfo("Sucesso", f"Aluno '{aluno_nome}' cadastrado no curso '{aluno_curso}'!")

        nome.delete(0, "end")
        cpf.delete(0, "end")
        contato.delete(0, "end")
        nascimento.delete(0, "end")
        endereco.delete(0, "end")
        senha.delete(0, "end")
        curso_var.set(cursos[0])

    btn_cadastrar = ctk.CTkButton(frame, text="Cadastrar", command=aluno_cadastro, height=btn_h)
    btn_cadastrar.pack(pady=12, padx=12, fill="x")

    tela_index = ctk.CTkButton(frame, text="voltar", command=lambda: index(tela_aluno_ca), height=btn_h)
    tela_index.pack(pady=6, padx=12, fill="x")

    tela_aluno_ca.mainloop()


def tela_logar_aluno(tela_ant):
    try:
        tela_ant.destroy()
    except Exception:
        pass

    logar_aluno = ctk.CTk()
    aplicar_responsividade(logar_aluno)
    criar_fundo_responsivo(logar_aluno, "img.png")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(logar_aluno)

    frame = ctk.CTkFrame(logar_aluno, fg_color="#1a1a1a", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.5)

    Log_cpf = ctk.CTkEntry(frame, placeholder_text='cpf', font=("Arial", f_text))
    Log_cpf.pack(padx=10, pady=10, fill="x")
    log_senha = ctk.CTkEntry(frame, placeholder_text='senha', show='*', font=("Arial", f_text))
    log_senha.pack(padx=10, pady=10, fill="x")

    def aluno_login():
        aluno_senha = log_senha.get()
        aluno_cpf = Log_cpf.get()

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
            logar_aluno.destroy()
            tela_aluno_principal(logado_aluno)

    btn_logar_aluno = ctk.CTkButton(frame, text="logar", command=aluno_login, height=btn_h)
    btn_logar_aluno.pack(pady=8, padx=10, fill="x")

    btn_aluno_cadastro = ctk.CTkButton(frame, text="cadastrar", command=lambda: tela_aluno_cadastro(logar_aluno), height=btn_h)
    btn_aluno_cadastro.pack(pady=6, padx=10, fill="x")

    tela_index = ctk.CTkButton(frame, text="sair", command=lambda: index(logar_aluno), height=btn_h)
    tela_index.pack(pady=6, padx=10, fill="x")

    logar_aluno.mainloop()


def tela_aluno_principal(logado_aluno):
    """Tela inicial do aluno com botões de atividades e média de notas."""
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Aluno {logado_aluno['nome']}")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    frame = ctk.CTkFrame(tela, fg_color="#00000060", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.85)

    ctk.CTkLabel(frame, text=f"Bem-vindo(a), {logado_aluno['nome']}", font=("Arial", f_title)).pack(pady=12)

    # Botão para fazer atividade
    btn_atividade = ctk.CTkButton(frame, text="Fazer Atividade", command=lambda: [tela.destroy(), tela_aluno_1(logado_aluno)], height=btn_h)
    btn_atividade.pack(pady=10, padx=12, fill="x")

    # Botão para ver média
    btn_media = ctk.CTkButton(frame, text="Ver Média das Notas", command=lambda: [tela.destroy(), tela_media_notas(logado_aluno)], height=btn_h)
    btn_media.pack(pady=10, padx=12, fill="x")

    btn_ver_notas = ctk.CTkButton(frame, text="Ver Notas Detalhadas", command=lambda: [tela.destroy(), tela_aluno_ver_notas_atividades(logado_aluno)], height=btn_h)
    btn_ver_notas.pack(pady=10, padx=12, fill="x")

    # Botão voltar para index
    btn_voltar = ctk.CTkButton(frame, text="Voltar", command=lambda: [tela.destroy(), index()], height=btn_h)
    btn_voltar.pack(pady=10, padx=12, fill="x")

    tela.mainloop()


def tela_media_notas(logado_aluno):
    aluno_obj = Aluno()
    medias = aluno_obj.calcular_media(logado_aluno["nome"])

    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Média das Notas - {logado_aluno['nome']}")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    frame = ctk.CTkFrame(tela, fg_color="#1a1a1a", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.85)

    ctk.CTkLabel(frame, text="Média das Notas por Professor", font=("Arial", f_title)).pack(pady=12)

    if not medias:
        ctk.CTkLabel(frame, text="Nenhuma nota registrada ainda.", font=("Arial", f_text)).pack(pady=12)
    else:
        for prof, media in medias.items():
            ctk.CTkLabel(frame, text=f"{prof}: {media:.2f}", font=("Arial", f_text)).pack(pady=5)
            mensagem = obter_mensagem_por_nota(media)
            ctk.CTkLabel(frame, text=mensagem, wraplength=int(largura * 0.85), justify="left", text_color="#b0b0b0", font=("Arial", f_text)).pack(pady=4)

    btn_voltar = ctk.CTkButton(frame, text="Voltar", command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)], height=btn_h)
    btn_voltar.pack(pady=10, padx=12, fill="x")

    tela.mainloop()


def tela_aluno_ver_notas_atividades(logado_aluno):
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Notas Detalhadas - {logado_aluno['nome']}")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    ctk.CTkLabel(tela, text=f"Notas de {logado_aluno['nome']}", font=("Arial", f_title)).pack(pady=12)

    # Carregar alunos do servidor
    alunos = receber_servidor("get_aluno") or []

    notas = []
    for al in alunos:
        if al["nome"] == logado_aluno["nome"]:
            notas = al.get("notas", [])
            break

    frame_scroll = ctk.CTkScrollableFrame(tela, width=int(largura * 0.95), height=int(altura * 0.7))
    frame_scroll.pack(pady=10, padx=10, fill="both", expand=True)

    if not notas:
        ctk.CTkLabel(frame_scroll, text="Nenhuma nota registrada ainda.", font=("Arial", f_text)).pack(pady=20)
    else:
        for item in notas:
            bloco = ctk.CTkFrame(frame_scroll, corner_radius=8)
            bloco.pack(pady=8, padx=8, fill="x")

            ctk.CTkLabel(bloco, text=f"Professor: {item['professor']}", font=("Arial", f_text, "bold")).pack(anchor="w", padx=10, pady=3)
            ctk.CTkLabel(bloco, text=f"Atividade:\n{item['atividade']}", wraplength=int(largura * 0.85), justify="left", font=("Arial", f_text)).pack(anchor="w", padx=12, pady=3)
            ctk.CTkLabel(bloco, text=f"Nota: {item['nota']}", font=("Arial", f_text)).pack(anchor="w", padx=12, pady=3)
            ctk.CTkLabel(bloco, text=f"Mensagem:\n{item.get('mensagem', obter_mensagem_por_nota(float(item['nota'])))}", wraplength=int(largura * 0.85), justify="left", text_color="#bfbfbf", font=("Arial", f_text)).pack(anchor="w", padx=12, pady=3)

    btn_voltar = ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)], height=btn_h)
    btn_voltar.pack(pady=12, padx=12)

    tela.mainloop()


def tela_aluno_1(logado_aluno):
    tela = ctk.CTk()
    aplicar_responsividade(tela)
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Aluno {logado_aluno['nome']}")

    largura, altura, f_title, f_text, btn_h = tamanhos_proporcionais(tela)

    ctk.CTkLabel(tela, text=f"Bem-vindo(a), {logado_aluno['nome']}", font=("Arial", f_title)).pack(pady=8)

    frame_scroll = ctk.CTkScrollableFrame(tela, width=int(largura * 0.95), height=int(altura * 0.75))
    frame_scroll.pack(pady=10, padx=10, fill="both", expand=True)

    # Pega apenas atividades que o aluno ainda não respondeu (usa Aluno.ver_atividades que foi adaptada para servidor)
    atividades = aluno.ver_atividades(logado_aluno["nome"])

    if not atividades:
        ctk.CTkLabel(frame_scroll, text="Nenhuma atividade disponível.", font=("Arial", f_text)).pack(pady=20)
    else:
        for atv in atividades:
            frame = ctk.CTkFrame(frame_scroll, corner_radius=8)
            frame.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"Professor: {atv['professor']}", font=("Arial", f_text, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame, text=f"Atividade:\n{atv['texto']}", wraplength=int(largura * 0.85), justify="left", font=("Arial", f_text)).pack(anchor="w", padx=20)

            resposta_box = ctk.CTkTextbox(frame, width=int(largura * 0.8), height=int(altura * 0.12), font=("Arial", f_text))
            resposta_box.pack(padx=10, pady=5)

            def enviar_resposta(atv_ref=atv, box=resposta_box):
                resposta = box.get("1.0", "end").strip()
                if resposta:
                    aluno.enviar_resposta(logado_aluno["nome"], atv_ref["professor"], resposta, atv_ref["texto"])
                    messagebox.showinfo("Sucesso", "Resposta enviada com sucesso!")
                    tela.destroy()
                    tela_aluno_1(logado_aluno)
                else:
                    messagebox.showwarning("Erro", "Digite uma resposta antes de enviar.")

            btn_enviar = ctk.CTkButton(frame, text="Enviar Resposta", command=enviar_resposta, height=btn_h)
            btn_enviar.pack(pady=5, padx=10)

    ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)], height=btn_h).pack(pady=10)
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

    ctk.CTkLabel(tela, text=f"Notas de {logado_aluno['nome']}", font=("Arial", f_title)).pack(pady=12)

    # Carregar alunos do servidor
    alunos = receber_servidor("get_aluno") or []

    notas = []
    for al in alunos:
        if al["nome"] == logado_aluno["nome"]:
            notas = al.get("notas", [])
            break

    if not notas:
        ctk.CTkLabel(tela, text="Você ainda não possui notas registradas.", font=("Arial", f_text)).pack(pady=20)
    else:
        for item in notas:
            frame = ctk.CTkFrame(tela, corner_radius=8)
            frame.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"Professor: {item['professor']}", font=("Arial", f_text, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame, text=f"Atividade: {item['atividade']}", wraplength=int(largura * 0.85), justify="left", font=("Arial", f_text)).pack(anchor="w", padx=20)
            ctk.CTkLabel(frame, text=f"Nota: {item['nota']}", font=("Arial", f_text)).pack(anchor="w", padx=20, pady=5)

    btn_voltar = ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_aluno_1(logado_aluno)], height=btn_h)
    btn_voltar.pack(pady=12)
    tela.mainloop()


# -----------------------------
# TELAS ADM (mantida lógica)
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

    frame = ctk.CTkFrame(tela_adm, fg_color="#1a1a1a", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    txt = ctk.CTkLabel(frame, text='', font=("Arial", f_title))
    txt.pack(padx=10, pady=10)
    nome = ctk.CTkEntry(frame, placeholder_text='Nome do Professor', font=("Arial", f_text))
    nome.pack(padx=10, pady=8, fill="x")

    cpf = ctk.CTkEntry(frame, placeholder_text='CPF do Professor', font=("Arial", f_text))
    cpf.pack(padx=10, pady=8, fill="x")

    ctk.CTkLabel(frame, text="É Coordenador?", font=("Arial", f_text)).pack(pady=(10, 0))
    var_coord = ctk.BooleanVar(value=False)
    switch_coord = ctk.CTkSwitch(frame, text="Coordenador", variable=var_coord, onvalue=True, offvalue=False)
    switch_coord.pack(pady=8)

    def cadastro_cpf_prof():
        nome_profe = nome.get()
        profe_cpf = cpf.get()
        is_coord = var_coord.get()

        if not (nome_profe and profe_cpf):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        adm.cadastrar_professor_cpf(nome_profe, profe_cpf, is_coord)
        messagebox.showinfo("Sucesso", f"Professor '{nome_profe}' cadastrado! Coordenador: {is_coord}")

        nome.delete(0, "end")
        cpf.delete(0, "end")
        var_coord.set(False)

    btn_cpf_prof = ctk.CTkButton(frame, text="Cadastrar Professor", command=cadastro_cpf_prof, height=btn_h)
    btn_cpf_prof.pack(pady=12, padx=12, fill="x")

    btn_cadastrar_curso = ctk.CTkButton(frame, text="Cadastrar Curso", command=lambda: tela_cadastrar_curso(tela_adm), height=btn_h)
    btn_cadastrar_curso.pack(pady=8, padx=12, fill="x")

    tela_index = ctk.CTkButton(frame, text="Voltar", command=lambda: index(tela_adm), height=btn_h)
    tela_index.pack(pady=8, padx=12, fill="x")

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

    frame = ctk.CTkFrame(tela_curso, fg_color="#1a1a1a", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    txt = ctk.CTkLabel(frame, text='Cadastro de Curso', font=('Arial', f_title))
    txt.pack(padx=10, pady=12)

    nome_curso = ctk.CTkEntry(frame, placeholder_text='Nome do Curso', font=("Arial", f_text))
    nome_curso.pack(padx=10, pady=8, fill="x")

    carga_hora = ctk.CTkEntry(frame, placeholder_text='Carga Horária (em horas)', font=("Arial", f_text))
    carga_hora.pack(padx=10, pady=8, fill="x")

    coordenadores = adm.listar_coordenadores()
    if not coordenadores:
        coordenadores = ['Nenhum coordenador disponível']

    coord_var = ctk.StringVar(value=coordenadores[0])
    ctk.CTkLabel(frame, text="Selecione o Coordenador", font=("Arial", f_text)).pack(pady=(10, 0))
    menu_coord = ctk.CTkOptionMenu(frame, variable=coord_var, values=coordenadores)
    menu_coord.pack(padx=10, pady=8, fill="x")

    def cadastrar_curso():
        nome = nome_curso.get()
        coordenador = coord_var.get()
        carga = carga_hora.get()

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

    btn_cadastrar = ctk.CTkButton(frame, text="Cadastrar Curso", command=cadastrar_curso, height=btn_h)
    btn_cadastrar.pack(pady=12, padx=12, fill="x")

    btn_voltar = ctk.CTkButton(frame, text="Voltar", command=lambda: index(tela_curso), height=btn_h)
    btn_voltar.pack(pady=8, padx=12, fill="x")

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

    frame = ctk.CTkFrame(janela, fg_color="#1a1a1a", corner_radius=20)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.85)

    txt = ctk.CTkLabel(frame, text='', font=("Arial", f_title))
    txt.pack(padx=10, pady=32)

    btn_professor = ctk.CTkButton(frame, text="professor", command=lambda: tela_logar_professor(janela), height=btn_h)
    btn_professor.pack(pady=12, padx=20, fill="x")

    btn_adm = ctk.CTkButton(frame, text="administração", command=lambda: tela_adm(janela), height=btn_h)
    btn_adm.pack(pady=12, padx=20, fill="x")

    btn_aluno = ctk.CTkButton(frame, text='aluno', command=lambda: tela_logar_aluno(janela), height=btn_h)
    btn_aluno.pack(pady=12, padx=20, fill="x")

    # botão para sair / fechar fullscreen
    def fechar_e_sair():
        try:
            janela.attributes("-fullscreen", False)
        except Exception:
            pass
        janela.destroy()

    btn_sair = ctk.CTkButton(frame, text="Sair", command=fechar_e_sair, fg_color="#aa3333", hover_color="#cc4444", height=btn_h)
    btn_sair.pack(pady=12, padx=20, fill="x")

    janela.mainloop()


# -----------------------------
# PONTO DE ENTRADA
# -----------------------------
if __name__ == "__main__":
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme("dark-blue")
    index()
