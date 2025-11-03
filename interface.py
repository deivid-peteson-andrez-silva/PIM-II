from sistema import Professor, Aluno, Adm, receber_servidor, enviar_servidor
professor = Professor()
aluno = Aluno()
adm = Adm()

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from mensagens import obter_mensagem_por_nota

# telas professor
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("dark-blue")

from PIL import Image, ImageTk


def criar_fundo_responsivo(tela, caminho_imagem):
    """
    Adiciona um fundo responsivo a qualquer CTk janela.
    """
    try:
        img_original = Image.open(caminho_imagem)
    except Exception:

        img_original = Image.new("RGBA", (800, 600), (30, 30, 30, 255))

    label_fundo = ctk.CTkLabel(tela, text="")
    label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    def redimensionar(event):
        largura = max(1, event.width)
        altura = max(1, event.height)
        img_resized = img_original.resize((largura, altura))
        img_tk = ImageTk.PhotoImage(img_resized)
        label_fundo.configure(image=img_tk)
        label_fundo.image = img_tk 

    tela.bind("<Configure>", redimensionar)
    return label_fundo


def tela_profe_cadastro(tela_ant):
    tela_ant.destroy()
    cadastro = ctk.CTk()
    cadastro.geometry('500x550')

    criar_fundo_responsivo(cadastro, "img.png")

    txt = ctk.CTkLabel(cadastro, text='Insira seus dados')
    txt.pack(padx=10, pady=10)

    nome = ctk.CTkEntry(cadastro, placeholder_text='Nome')
    nome.pack(padx=10, pady=10)
    cpf = ctk.CTkEntry(cadastro, placeholder_text='CPF')
    cpf.pack(padx=10, pady=10)
    contato = ctk.CTkEntry(cadastro, placeholder_text='Contato')
    contato.pack(padx=10, pady=10)
    senha = ctk.CTkEntry(cadastro, placeholder_text='Senha', show='*')
    senha.pack(padx=10, pady=10)

    cursos = adm.listar_cursos()
    if not cursos:
        cursos = ['Nenhum curso cadastrado']

    curso_var = ctk.StringVar(value=cursos[0])
    ctk.CTkLabel(cadastro, text="Selecione o curso").pack(pady=(10, 0))
    menu_cursos = ctk.CTkOptionMenu(cadastro, variable=curso_var, values=cursos)
    menu_cursos.pack(padx=10, pady=10)

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

    btn_cadastrar = ctk.CTkButton(cadastro, text="Cadastrar", command=profe_cadastro)
    btn_cadastrar.pack(pady=15)

    tela_index = ctk.CTkButton(cadastro, text="Voltar", command=lambda: index(cadastro))
    tela_index.pack(pady=15)

    cadastro.mainloop()


def tela_logar_professor(tela_ant):
    tela_ant.destroy()
    logar_professor = ctk.CTk()
    logar_professor.geometry('500x500')

    criar_fundo_responsivo(logar_professor, "img.png")

    Log_cpf = ctk.CTkEntry(logar_professor, placeholder_text='cpf')
    Log_cpf.pack(padx=10, pady=10)
    log_senha = ctk.CTkEntry(logar_professor, placeholder_text='senha', show='*')
    log_senha.pack(padx=10, pady=10)

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

    btn_logar_prof = ctk.CTkButton(logar_professor, text="logar", command=profe_login)
    btn_logar_prof.pack(pady=15)

    btn_prof_cadastro = ctk.CTkButton(logar_professor, text="cadastrar", command=lambda: tela_profe_cadastro(logar_professor))
    btn_prof_cadastro.pack(pady=15)
    tela_index = ctk.CTkButton(logar_professor, text="voltar", command=lambda: index(logar_professor))
    tela_index.pack(pady=15)
    logar_professor.mainloop()


def tela_professor_1(logado_profe):
    tela = ctk.CTk()
    tela.geometry("700x500")
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Professor {logado_profe['professor_nome']}")

    lbl = ctk.CTkLabel(tela, text=f"Bem-vindo(a), {logado_profe['professor_nome']}", font=("Arial", 16))
    lbl.pack(pady=20)

    btn_atividade = ctk.CTkButton(tela, text="Criar nova atividade",
                                  command=lambda: tela_atividade_prof(tela, logado_profe))
    btn_atividade.pack(pady=10)

    btn_corrigir = ctk.CTkButton(tela, text="Corrigir respostas",
                                 command=lambda: tela_corrigir(tela, logado_profe))
    btn_corrigir.pack(pady=10)

    ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), index()]).pack(pady=10)
    tela.mainloop()


def tela_atividade_prof(tela_ant, logado_profe):
    tela_ant.destroy()  
    tela = ctk.CTk()
    tela.geometry("600x500")
    tela.title("Nova Atividade")

    criar_fundo_responsivo(tela, "img.png")

    lbl = ctk.CTkLabel(tela, text="Digite o enunciado da atividade:", font=("Arial", 14))
    lbl.pack(pady=10)

    chat = ctk.CTkTextbox(tela, width=500, height=250)
    chat.pack(pady=10)

    def salvar_atividade():
        texto = chat.get("1.0", "end").strip()
        if texto:
  
            professor.atividade(logado_profe["professor_nome"], texto)
            tela.destroy()  
            messagebox.showinfo("Sucesso", "Atividade cadastrada!")
            tela_professor_1(logado_profe)  
        else:
            messagebox.showwarning("Erro", "O campo não pode estar vazio.")

    btn_salvar = ctk.CTkButton(tela, text="Salvar atividade", command=salvar_atividade)
    btn_salvar.pack(pady=20)

    btn_voltar = ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(logado_profe)])
    btn_voltar.pack()

    tela.mainloop()


def tela_corrigir(tela_ant, prof_logado):
    try:
        tela_ant.destroy()
    except:
        pass

    tela = ctk.CTk()
    tela.geometry("820x600")
    criar_fundo_responsivo(tela, "img.png")
    tela.title(f"Corrigir Respostas - {prof_logado['professor_nome']}")

    ctk.CTkLabel(
        tela,
        text=f"Correção de Respostas - Professor {prof_logado['professor_nome']}",
        font=("Arial", 18, "bold")
    ).pack(pady=12)


    alunos = receber_servidor("get_aluno") or []

    if not alunos:
        ctk.CTkLabel(tela, text="Nenhum aluno cadastrado no servidor.", font=("Arial", 12)).pack(pady=20)
        ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(prof_logado)]).pack(pady=10)
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

    frame_scroll = ctk.CTkScrollableFrame(tela, width=780, height=420)
    frame_scroll.pack(padx=15, pady=10, fill="both", expand=True)

    entradas_notas = []

    if not respostas_para_corrigir:
        ctk.CTkLabel(frame_scroll, text="Nenhuma resposta pendente no momento.", font=("Arial", 13)).pack(pady=20)
        ctk.CTkButton(frame_scroll, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(prof_logado)]).pack(pady=8)
        tela.mainloop()
        return
    else:
        for item in respostas_para_corrigir:
            bloco = ctk.CTkFrame(frame_scroll)
            bloco.pack(fill="x", padx=8, pady=8)

            ctk.CTkLabel(bloco, text=f"Aluno: {item['aluno']}", font=("Arial", 12, "bold")).pack(anchor="w", padx=8, pady=4)
            ctk.CTkLabel(bloco, text=f"Atividade:\n{item['atividade']}", wraplength=740, justify="left").pack(anchor="w", padx=12)
            ctk.CTkLabel(bloco, text=f"Resposta:\n{item['resposta']}", wraplength=740, justify="left",
                         text_color="#bfbfbf").pack(anchor="w", padx=12, pady=(6, 4))

      
            linha_nota = ctk.CTkFrame(bloco)
            linha_nota.pack(anchor="w", padx=12, pady=6)
            ctk.CTkLabel(linha_nota, text="Nota (0-10):", font=("Arial", 11)).pack(side="left", padx=(0, 6))
            entrada_nota = ctk.CTkEntry(linha_nota, placeholder_text="ex: 8.5", width=120)
            entrada_nota.pack(side="left")

        
            ctk.CTkLabel(bloco, text="Mensagem para o aluno (opcional):", font=("Arial", 11)).pack(anchor="w", padx=12, pady=(6, 2))
            entrada_msg = ctk.CTkEntry(bloco, placeholder_text="Digite uma mensagem ou deixe vazio para automática", width=600)
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

    botoes = ctk.CTkFrame(tela)
    botoes.pack(pady=10)

    ctk.CTkButton(botoes, text="Salvar Notas", command=salvar_notas, width=140).pack(side="left", padx=8)
    ctk.CTkButton(botoes, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(prof_logado)], width=120).pack(side="left", padx=8)

    tela.mainloop()


def tela_atribuir_nota(tela_ant, logado_profe):
    tela_ant.destroy()
    tela = ctk.CTk()
    tela.geometry("700x500")
    tela.title("Atribuir Nota")
    criar_fundo_responsivo(tela, "img.png")

    ctk.CTkLabel(tela, text="Atribuir Nota a um Aluno", font=("Arial", 16)).pack(pady=15)

    nome_aluno = ctk.CTkEntry(tela, placeholder_text="Nome do Aluno")
    nome_aluno.pack(pady=10)

    atividade = ctk.CTkEntry(tela, placeholder_text="Nome ou texto da atividade")
    atividade.pack(pady=10)

    nota = ctk.CTkEntry(tela, placeholder_text="Nota (0 - 10)")
    nota.pack(pady=10)

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

    btn_salvar = ctk.CTkButton(tela, text="Salvar Nota", command=salvar_nota)
    btn_salvar.pack(pady=15)

    btn_voltar = ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(logado_profe)])
    btn_voltar.pack(pady=15)

    tela.mainloop()


# telas do aluno


def tela_aluno_cadastro(tela_ant):
    tela_ant.destroy()
    tela_aluno_ca = ctk.CTk()
    tela_aluno_ca.geometry('500x550')

    criar_fundo_responsivo(tela_aluno_ca, "img.png")

    txt = ctk.CTkLabel(tela_aluno_ca, text='Insira seus dados')
    txt.pack(padx=10, pady=10)

    nome = ctk.CTkEntry(tela_aluno_ca, placeholder_text='Nome')
    nome.pack(padx=10, pady=10)
    nascimento = ctk.CTkEntry(tela_aluno_ca, placeholder_text='Data de Nascimento')
    nascimento.pack(padx=10, pady=10)
    cpf = ctk.CTkEntry(tela_aluno_ca, placeholder_text='CPF')
    cpf.pack(padx=10, pady=10)
    contato = ctk.CTkEntry(tela_aluno_ca, placeholder_text='Telefone')
    contato.pack(padx=10, pady=10)
    endereco = ctk.CTkEntry(tela_aluno_ca, placeholder_text='Endereço')
    endereco.pack(padx=10, pady=10)
    senha = ctk.CTkEntry(tela_aluno_ca, placeholder_text='Senha', show='*')
    senha.pack(padx=10, pady=10)

    cursos = adm.listar_cursos()
    if not cursos:
        cursos = ['Nenhum curso cadastrado']
    curso_var = ctk.StringVar(value=cursos[0])
    ctk.CTkLabel(tela_aluno_ca, text="Selecione o Curso").pack(pady=(10, 0))
    menu_cursos = ctk.CTkOptionMenu(tela_aluno_ca, variable=curso_var, values=cursos)
    menu_cursos.pack(padx=10, pady=10)

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

    btn_cadastrar = ctk.CTkButton(tela_aluno_ca, text="Cadastrar", command=aluno_cadastro)
    btn_cadastrar.pack(pady=15)

    tela_index = ctk.CTkButton(tela_aluno_ca, text="voutar", command=lambda: index(tela_aluno_ca))
    tela_index.pack(pady=15)

    tela_aluno_ca.mainloop()


def tela_logar_aluno(tela_ant):
    tela_ant.destroy()
    logar_aluno = ctk.CTk()
    logar_aluno.geometry('500x500')

    criar_fundo_responsivo(logar_aluno, "img.png")

    Log_cpf = ctk.CTkEntry(logar_aluno, placeholder_text='cpf')
    Log_cpf.pack(padx=10, pady=10)
    log_senha = ctk.CTkEntry(logar_aluno, placeholder_text='senha', show='*')
    log_senha.pack(padx=10, pady=10)

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

    btn_logar_aluno = ctk.CTkButton(logar_aluno, text="logar", command=aluno_login)
    btn_logar_aluno.pack(pady=15)

    btn_aluno_cadastro = ctk.CTkButton(logar_aluno, text="cadastrar", command=lambda: tela_aluno_cadastro(logar_aluno))
    btn_aluno_cadastro.pack(pady=15)
    tela_index = ctk.CTkButton(logar_aluno, text="sair", command=lambda: index(logar_aluno))
    tela_index.pack(pady=15)
    logar_aluno.mainloop()


def tela_aluno_principal(logado_aluno):
    """Tela inicial do aluno com botões de atividades e média de notas."""
    tela = ctk.CTk()
    tela.geometry("500x400")
    tela.title(f"Aluno {logado_aluno['nome']}")

    ctk.CTkLabel(tela, text=f"Bem-vindo(a), {logado_aluno['nome']}", font=("Arial", 16)).pack(pady=20)
    criar_fundo_responsivo(tela, "img.png")


    btn_atividade = ctk.CTkButton(
        tela,
        text="Fazer Atividade",
        command=lambda: [tela.destroy(), tela_aluno_1(logado_aluno)]
    )
    btn_atividade.pack(pady=20)

    btn_media = ctk.CTkButton(
        tela,
        text="Ver Média das Notas",
        command=lambda: [tela.destroy(), tela_media_notas(logado_aluno)]
    )
    btn_media.pack(pady=20)

    btn_ver_notas = ctk.CTkButton(
        tela,
        text="Ver Notas Detalhadas",
        command=lambda: [tela.destroy(), tela_aluno_ver_notas_atividades(logado_aluno)]
    )
    btn_ver_notas.pack(pady=20)
 
    btn_voltar = ctk.CTkButton(
        tela,
        text="Voltar",
        command=lambda: [tela.destroy(), index()]
    )
    btn_voltar.pack(pady=20)

    tela.mainloop()


def tela_media_notas(logado_aluno):
    aluno_obj = Aluno()
    medias = aluno_obj.calcular_media(logado_aluno["nome"])

    tela = ctk.CTk()
    tela.geometry("500x500")
    tela.title(f"Média das Notas - {logado_aluno['nome']}")
    criar_fundo_responsivo(tela, "img.png")

    ctk.CTkLabel(tela, text="Média das Notas por Professor", font=("Arial", 16)).pack(pady=20)

    if not medias:
        ctk.CTkLabel(tela, text="Nenhuma nota registrada ainda.").pack(pady=20)
    else:
        for prof, media in medias.items():
            ctk.CTkLabel(tela, text=f"{prof}: {media:.2f}", font=("Arial", 14)).pack(pady=5)


            mensagem = obter_mensagem_por_nota(media)
            ctk.CTkLabel(
                tela,
                text=mensagem,
                wraplength=450,
                justify="left",
                text_color="#b0b0b0",
                font=("Arial", 12)
            ).pack(pady=4)

    btn_voltar = ctk.CTkButton(
        tela,
        text="Voltar",
        command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)]
    )
    btn_voltar.pack(pady=20)

    tela.mainloop()


def tela_aluno_ver_notas_atividades(logado_aluno):
    tela = ctk.CTk()
    tela.geometry("750x550")
    tela.title(f"Notas Detalhadas - {logado_aluno['nome']}")

    criar_fundo_responsivo(tela, "img.png")

    ctk.CTkLabel(tela, text=f"Notas de {logado_aluno['nome']}", font=("Arial", 16)).pack(pady=15)


    alunos = receber_servidor("get_aluno") or []

    notas = []
    for al in alunos:
        if al["nome"] == logado_aluno["nome"]:
            notas = al.get("notas", [])
            break

    frame_scroll = ctk.CTkScrollableFrame(tela, width=720, height=400)
    frame_scroll.pack(pady=10, padx=10, fill="both", expand=True)

    if not notas:
        ctk.CTkLabel(frame_scroll, text="Nenhuma nota registrada ainda.", font=("Arial", 14)).pack(pady=20)
    else:
        for item in notas:
            bloco = ctk.CTkFrame(frame_scroll)
            bloco.pack(pady=8, padx=8, fill="x")

            ctk.CTkLabel(bloco, text=f"Professor: {item['professor']}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=3)
            ctk.CTkLabel(bloco, text=f"Atividade:\n{item['atividade']}", wraplength=680, justify="left").pack(anchor="w", padx=12, pady=3)
            ctk.CTkLabel(bloco, text=f"Nota: {item['nota']}", font=("Arial", 12)).pack(anchor="w", padx=12, pady=3)
            ctk.CTkLabel(
                bloco,
                text=f"Mensagem:\n{item.get('mensagem', obter_mensagem_por_nota(float(item['nota'])))}",
                wraplength=680,
                justify="left",
                text_color="#bfbfbf",
                font=("Arial", 11)
            ).pack(anchor="w", padx=12, pady=3)

    btn_voltar = ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)])
    btn_voltar.pack(pady=15)

    tela.mainloop()


def tela_aluno_1(logado_aluno):
    tela = ctk.CTk()
    tela.geometry("700x500")
    tela.title(f"Aluno {logado_aluno['nome']}")

    criar_fundo_responsivo(tela, "img.png")

    ctk.CTkLabel(tela, text=f"Bem-vindo(a), {logado_aluno['nome']}", font=("Arial", 16)).pack(pady=10)

    frame_scroll = ctk.CTkScrollableFrame(tela, width=650, height=380)
    frame_scroll.pack(pady=10, padx=10, fill="both", expand=True)


    atividades = aluno.ver_atividades(logado_aluno["nome"])

    if not atividades:
        ctk.CTkLabel(frame_scroll, text="Nenhuma atividade disponível.").pack(pady=20)
    else:
        for atv in atividades:
            frame = ctk.CTkFrame(frame_scroll)
            frame.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"Professor: {atv['professor']}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame, text=f"Atividade:\n{atv['texto']}", wraplength=600, justify="left").pack(anchor="w", padx=20)

            resposta_box = ctk.CTkTextbox(frame, width=600, height=80)
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

            btn_enviar = ctk.CTkButton(frame, text="Enviar Resposta", command=enviar_resposta)
            btn_enviar.pack(pady=5)

    ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_aluno_principal(logado_aluno)]).pack(pady=10)
    tela.mainloop()


def tela_ver_notas(tela_ant, logado_aluno):
    tela_ant.destroy()
    tela = ctk.CTk()
    tela.geometry("700x500")
    tela.title("Minhas Notas")

    criar_fundo_responsivo(tela, "img.png")

    ctk.CTkLabel(tela, text=f"Notas de {logado_aluno['nome']}", font=("Arial", 16)).pack(pady=15)

    alunos = receber_servidor("get_aluno") or []

    notas = []
    for al in alunos:
        if al["nome"] == logado_aluno["nome"]:
            notas = al.get("notas", [])
            break

    if not notas:
        ctk.CTkLabel(tela, text="Você ainda não possui notas registradas.").pack(pady=20)
    else:
        for item in notas:
            frame = ctk.CTkFrame(tela)
            frame.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"Professor: {item['professor']}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame, text=f"Atividade: {item['atividade']}", wraplength=600, justify="left").pack(anchor="w", padx=20)
            ctk.CTkLabel(frame, text=f"Nota: {item['nota']}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)

    btn_voltar = ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_aluno_1(logado_aluno)])
    btn_voltar.pack(pady=20)

    tela.mainloop()


# telas adm

def tela_adm(tela_ant):
    tela_ant.destroy()
    tela_adm = ctk.CTk()
    tela_adm.geometry('500x500')

    criar_fundo_responsivo(tela_adm, "img.png")
    txt = ctk.CTkLabel(tela_adm, text='')
    txt.pack(padx=10, pady=30)
    nome = ctk.CTkEntry(tela_adm, placeholder_text='Nome do Professor')
    nome.pack(padx=10, pady=10)

    cpf = ctk.CTkEntry(tela_adm, placeholder_text='CPF do Professor')
    cpf.pack(padx=10, pady=10)

    ctk.CTkLabel(tela_adm, text="É Coordenador?").pack(pady=(10, 0))
    var_coord = ctk.BooleanVar(value=False)
    switch_coord = ctk.CTkSwitch(
        tela_adm, text="Coordenador", variable=var_coord,
        onvalue=True, offvalue=False
    )
    switch_coord.pack(pady=10)

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

    btn_cpf_prof = ctk.CTkButton(tela_adm, text="Cadastrar Professor", command=cadastro_cpf_prof)
    btn_cpf_prof.pack(pady=15)

    btn_cadastrar_curso = ctk.CTkButton(tela_adm, text="Cadastrar Curso", command=lambda: tela_cadastrar_curso(tela_adm))
    btn_cadastrar_curso.pack(pady=10)

    tela_index = ctk.CTkButton(tela_adm, text="Voltar", command=lambda: index(tela_adm))
    tela_index.pack(pady=15)

    tela_adm.mainloop()


def tela_cadastrar_curso(tela_ant):
    tela_ant.destroy()
    tela_curso = ctk.CTk()
    tela_curso.geometry('500x500')

    criar_fundo_responsivo(tela_curso, "img.png")

    txt = ctk.CTkLabel(tela_curso, text='Cadastro de Curso', font=('Arial', 18))
    txt.pack(padx=10, pady=20)

    nome_curso = ctk.CTkEntry(tela_curso, placeholder_text='Nome do Curso')
    nome_curso.pack(padx=10, pady=10)

    carga_hora = ctk.CTkEntry(tela_curso, placeholder_text='Carga Horária (em horas)')
    carga_hora.pack(padx=10, pady=10)

    coordenadores = adm.listar_coordenadores()
    if not coordenadores:
        coordenadores = ['Nenhum coordenador disponível']

    coord_var = ctk.StringVar(value=coordenadores[0])
    ctk.CTkLabel(tela_curso, text="Selecione o Coordenador").pack(pady=(10, 0))
    menu_coord = ctk.CTkOptionMenu(tela_curso, variable=coord_var, values=coordenadores)
    menu_coord.pack(padx=10, pady=10)

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

    btn_cadastrar = ctk.CTkButton(tela_curso, text="Cadastrar Curso", command=cadastrar_curso)
    btn_cadastrar.pack(pady=20)

    btn_voltar = ctk.CTkButton(tela_curso, text="Voltar", command=lambda: index(tela_curso))
    btn_voltar.pack(pady=10)

    tela_curso.mainloop()


def index(tela_ant=None):
    if tela_ant:
        try:
            tela_ant.destroy()
        except:
            pass

    index = ctk.CTk()
    index.geometry('500x500')

    criar_fundo_responsivo(index, "img.png")
    txt = ctk.CTkLabel(index, text='')
    txt.pack(padx=10, pady=45)
    btn_professor = ctk.CTkButton(index, text="professor", command=lambda: tela_logar_professor(index))
    btn_professor.pack(pady=30)
    btn_adm = ctk.CTkButton(index, text="administração", command=lambda: tela_adm(index))
    btn_adm.pack(pady=30)
    btn_aluno = ctk.CTkButton(index, text='aluno', command=lambda: tela_logar_aluno(index))
    btn_aluno.pack(pady=30)
    index.mainloop()


if __name__ == "__main__":
    index()
