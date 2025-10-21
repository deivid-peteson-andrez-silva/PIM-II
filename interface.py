from sistema import Professor
professor = Professor()  
from tkinter import messagebox 
import customtkinter as ctk
from sistema import Adm
adm = Adm()
from sistema import Aluno
aluno = Aluno()
from PIL import Image
import json      



ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("dark-blue")
def tela_profe_cadastro(tela_ant):    
    tela_ant.destroy()
    cadastro = ctk.CTk()
    cadastro.geometry('500x550')

    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 550)
    )
    fundo = ctk.CTkLabel(cadastro, image=img_fundo, text='')
    fundo.place(x=0, y=0)
    
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
    logar_professor =ctk.CTk()
    logar_professor.geometry('500x500')

    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 500)
    )
    fundo = ctk.CTkLabel(logar_professor , image=img_fundo, text='')
    fundo.place(x=0, y=0)
    
    
    Log_cpf =ctk.CTkEntry(logar_professor, placeholder_text= 'cpf')
    Log_cpf.pack(padx=10, pady=10)
    log_senha =ctk.CTkEntry(logar_professor, placeholder_text= 'senha' , show='*')
    log_senha.pack(padx=10, pady=10)
    def profe_login():
        profe_senha = log_senha.get()
        profe_cpf = Log_cpf.get()


        if not ( profe_cpf and profe_senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
    
        logado_profe =   professor.logar(profe_cpf,profe_senha)
    
        if logado_profe == 1 :
            messagebox.showinfo('aaaaaa',f"Professor com cpf {profe_cpf} nao encontrado")

        elif logado_profe == 2:
            messagebox.showinfo('aaaaaaa',f" senha invalida")
        
        elif isinstance(logado_profe, dict):
            log_senha.delete(0, "end")
            Log_cpf.delete(0, "end")    
            logar_professor.destroy()
            tela_professor_1(logado_profe)
            
    
    btn_logar_prof =ctk.CTkButton(logar_professor, text="logar", command=profe_login)
    btn_logar_prof.pack(pady=15)
    
    btn_prof_cadastro = ctk.CTkButton(logar_professor, text="cadastrar", command=lambda :tela_profe_cadastro(logar_professor))
    btn_prof_cadastro.pack(pady=15)
    tela_index =ctk.CTkButton(logar_professor, text="index", command=lambda: index(logar_professor))
    tela_index.pack(pady=15)
    logar_professor.mainloop()


def tela_adm(tela_ant):
    tela_ant.destroy()
    tela_adm = ctk.CTk() 
    tela_adm.geometry('500x500')

    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 500)
    )
    fundo = ctk.CTkLabel(tela_adm , image=img_fundo, text='')
    fundo.place(x=0, y=0)
    
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

    btn_cadastrar_curso = ctk.CTkButton(tela_adm,text="Cadastrar Curso",command=lambda: tela_cadastrar_curso(tela_adm))
    btn_cadastrar_curso.pack(pady=10)

    tela_index = ctk.CTkButton(tela_adm, text="Voltar", command=lambda: index(tela_adm))
    tela_index.pack(pady=15)

    tela_adm.mainloop()
    
    
def tela_aluno_cadastro(tela_ant):
    tela_ant.destroy()    
    tela_aluno_ca = ctk.CTk() 
    tela_aluno_ca.geometry('500x550')
    
    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 550)
    )
    fundo = ctk.CTkLabel(tela_aluno_ca , image=img_fundo, text='')
    fundo.place(x=0, y=0)
    
    txt = ctk.CTkLabel(tela_aluno_ca,text='Insira seus dados')
    txt.pack(padx=10, pady=10 )

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

    # 🔽 Lista de cursos disponíveis
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
        
        # Salva o curso escolhido junto com os dados do aluno
        aluno.cadastrar_aluno(aluno_nome, aluno_cpf, data_nascimento, aluno_endereco, aluno_contato, aluno_senha, aluno_curso)
        messagebox.showinfo("Sucesso", f"Aluno '{aluno_nome}' cadastrado no curso '{aluno_curso}'!")

        # Limpa os campos
        nome.delete(0, "end")
        cpf.delete(0, "end")
        contato.delete(0, "end")
        nascimento.delete(0, "end")
        endereco.delete(0, "end")
        senha.delete(0, "end")
        curso_var.set(cursos[0])

    btn_cadastrar = ctk.CTkButton(tela_aluno_ca, text="Cadastrar", command=aluno_cadastro)
    btn_cadastrar.pack(pady=15)

    tela_index = ctk.CTkButton(tela_aluno_ca, text="Index", command=lambda: index(tela_aluno_ca))
    tela_index.pack(pady=15)
    
    tela_aluno_ca.mainloop()

def tela_logar_aluno(tela_ant):



    tela_ant.destroy()
    logar_aluno =ctk.CTk()
    logar_aluno.geometry('500x500')

    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 500)
    )
    fundo = ctk.CTkLabel(logar_aluno , image=img_fundo, text='')
    fundo.place(x=0, y=0)
    
    
    Log_cpf =ctk.CTkEntry(logar_aluno, placeholder_text= 'cpf')
    Log_cpf.pack(padx=10, pady=10)
    log_senha =ctk.CTkEntry(logar_aluno, placeholder_text= 'senha' , show='*')
    log_senha.pack(padx=10, pady=10)
    def aluno_login():
        aluno_senha = log_senha.get()
        aluno_cpf = Log_cpf.get()


        if not ( aluno_cpf and aluno_senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
    
        logado_aluno =   aluno.logar_aluno(aluno_cpf,aluno_senha)
    
        if logado_aluno == 1 :
            messagebox.showinfo('aaaaaa',f"Professor com cpf {aluno_cpf} nao encontrado")

        elif logado_aluno == 2:
            messagebox.showinfo('aaaaaaa',f" senha invalida")
        
        elif isinstance(logado_aluno, dict):
            log_senha.delete(0, "end")
            Log_cpf.delete(0, "end")    
            logar_aluno.destroy()
            tela_aluno_1(logado_aluno)
            
    
    btn_logar_aluno =ctk.CTkButton(logar_aluno, text="logar", command=aluno_login)
    btn_logar_aluno.pack(pady=15)
    
    btn_aluno_cadastro = ctk.CTkButton(logar_aluno, text="cadastrar", command=lambda :tela_aluno_cadastro(logar_aluno))
    btn_aluno_cadastro.pack(pady=15)
    tela_index =ctk.CTkButton(logar_aluno, text="index", command=lambda: index(logar_aluno))
    tela_index.pack(pady=15)
    logar_aluno.mainloop()



def tela_cadastrar_curso(tela_ant):
    tela_ant.destroy()
    tela_curso = ctk.CTk()
    tela_curso.geometry('500x500')

    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 500)
    )
    fundo = ctk.CTkLabel(tela_curso, image=img_fundo, text='')
    fundo.place(x=0, y=0)

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

#tela_cadastrar_curso()

def index(tela_ant=None):
    if tela_ant:
        tela_ant.destroy()    
    

    index =ctk.CTk()
    index.geometry('500x500')

    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 500)
    )
    fundo = ctk.CTkLabel(index , image=img_fundo, text='')
    fundo.place(x=0, y=0)
    
    txt = ctk.CTkLabel(index , text='')
    txt.pack(padx=10, pady=45 )
    btn_professor  =ctk.CTkButton(index, text="professor", command=lambda: tela_logar_professor(index))
    btn_professor.pack(pady=30)
    btn_adm  =ctk.CTkButton(index, text="administração", command=lambda: tela_adm(index))
    btn_adm.pack(pady=30)
    btn_aluno = ctk.CTkButton(index,text='aluno', command=lambda: tela_logar_aluno(index) )
    btn_aluno.pack(pady=30)
    index.mainloop()

def tela_aluno_1(logado_aluno):
    tela = ctk.CTk()
    tela.geometry("700x500")
    tela.title(f"Aluno {logado_aluno['nome']}")

    lbl = ctk.CTkLabel(tela, text=f"Bem-vindo(a), {logado_aluno['nome']}", font=("Arial", 16))
    lbl.pack(pady=10)

    atividades = aluno.ver_atividades(logado_aluno["nome"])

    if not atividades:
        ctk.CTkLabel(tela, text="Nenhuma atividade disponível.").pack(pady=20)
    else:
        for atv in atividades:
            frame = ctk.CTkFrame(tela)
            frame.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"Professor: {atv['professor']}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame, text=f"Atividade:\n{atv['texto']}", wraplength=600, justify="left").pack(anchor="w", padx=20)

            resposta_box = ctk.CTkTextbox(frame, width=600, height=80)
            resposta_box.pack(padx=10, pady=5)

            def enviar_resposta(atv_prof=atv["professor"], box=resposta_box):
                resposta = box.get("1.0", "end").strip()
                if resposta:
                    aluno.enviar_resposta(logado_aluno["nome"], atv_prof, resposta)
                    messagebox.showinfo("Sucesso", "Resposta enviada com sucesso!")
                    tela.destroy()
                    tela_aluno_1(logado_aluno)
                else:
                    messagebox.showwarning("Erro", "Digite uma resposta antes de enviar.")

            btn_enviar = ctk.CTkButton(frame, text="Enviar Resposta", command=enviar_resposta)
            btn_enviar.pack(pady=5)

    tela.mainloop()

def tela_ver_notas(tela_ant, logado_aluno):
    tela_ant.destroy()
    tela = ctk.CTk()
    tela.geometry("700x500")
    tela.title("Minhas Notas")

    ctk.CTkLabel(tela, text=f"Notas de {logado_aluno['nome']}", font=("Arial", 16)).pack(pady=15)

    try:
        with open("arquivos/alunos.json", "r", encoding="utf-8") as arq:
            alunos = json.load(arq)
    except:
        alunos = []

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




def tela_professor_1(logado_profe):
    tela = ctk.CTk()
    tela.geometry("700x500")
    tela.title(f"Professor {logado_profe['professor_nome']}")

    lbl = ctk.CTkLabel(tela, text=f"Bem-vindo(a), {logado_profe['professor_nome']}", font=("Arial", 16))
    lbl.pack(pady=20)

    # Botão para enviar nova atividade
    btn_atividade = ctk.CTkButton(tela, text="Criar nova atividade",
                                  command=lambda: tela_atividade_prof(tela, logado_profe))
    btn_atividade.pack(pady=10)

    # Botão para atribuir nota

    btn_nota = ctk.CTkButton(tela, text="Atribuir nota",
                         command=lambda: tela_atribuir_nota(tela, logado_profe))
    btn_nota.pack(pady=10)


    # Botão para corrigir respostas de alunos
    btn_corrigir = ctk.CTkButton(tela, text="Corrigir respostas",
                                 command=lambda: tela_corrigir(tela, logado_profe))
    btn_corrigir.pack(pady=10)

    tela.mainloop()



# tela altera
def tela_prof_altera(tela_ant,logado_profe):
   # tela_ant.after(100, tela_ant.destroy)
    tela_alterar_prof =ctk.CTk()
    tela_alterar_prof.geometry('500x500')


    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 500)
    )
    fundo = ctk.CTkLabel(tela_alterar_prof , image=img_fundo, text='')
    fundo.place(x=0, y=0)

    texto = ctk.CTkLabel(tela_alterar_prof, text=f"Professor {logado_profe['professor_nome']}", font=("Arial", 10))
    texto.pack(pady=50) 
    nome_al =ctk.CTkEntry(tela_alterar_prof, placeholder_text= 'nome')
    nome_al.pack(padx=10, pady=10)
    
    def alterar():
        novo_nome = nome_al.get()
        if novo_nome.strip():
            professor.alterar(logado_profe, novo_nome)
            messagebox.showinfo("Sucesso", f"Nome alterado para {novo_nome}")
            texto.configure(text=f"Professor {novo_nome}")  # Atualiza o label
            nome_al.delete(0, "end")

    tela_alterar_prof.mainloop()
    
    
def tela_atividade_prof(tela_ant, logado_profe):
    tela_ant.destroy()
    tela = ctk.CTk()
    tela.geometry("600x500")
    tela.title("Nova Atividade")

    lbl = ctk.CTkLabel(tela, text="Digite o enunciado da atividade:", font=("Arial", 14))
    lbl.pack(pady=10)

    chat = ctk.CTkTextbox(tela, width=500, height=250)
    chat.pack(pady=10)

    def salvar_atividade():
        texto = chat.get("1.0", "end").strip()
        if texto:
            professor.atividade(logado_profe["professor_nome"], texto)
            messagebox.showinfo("Sucesso", "Atividade cadastrada!")
            tela_professor_1(logado_profe)
            tela.destroy()
        else:
            messagebox.showwarning("Erro", "O campo não pode estar vazio.")

    btn_salvar = ctk.CTkButton(tela, text="Salvar atividade", command=salvar_atividade)
    btn_salvar.pack(pady=20)

    btn_voltar = ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(logado_profe)])
    btn_voltar.pack()

    tela.mainloop()
        
        
def tela_corrigir(tela_ant, logado_profe):
    from sistema import Aluno
    aluno = Aluno()

    tela_ant.destroy()
    tela = ctk.CTk()
    tela.geometry("700x500")
    tela.title("Respostas dos alunos")

    lbl = ctk.CTkLabel(tela, text="Respostas enviadas pelos alunos", font=("Arial", 14))
    lbl.pack(pady=10)

    # Mostra todas as respostas que mencionam o professor logado
    respostas = []
    for al in aluno.aluno_lista:
        for r in al.get("respostas", []):
            if r["professor"] == logado_profe["professor_nome"]:
                respostas.append((al["nome"], r["resposta"]))

    if not respostas:
        ctk.CTkLabel(tela, text="Nenhuma resposta recebida ainda.").pack(pady=20)
    else:
        for nome, resp in respostas:
            frame = ctk.CTkFrame(tela)
            frame.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"Aluno: {nome}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame, text=f"Resposta: {resp}", wraplength=600, justify="left").pack(anchor="w", padx=20)

    btn_voltar = ctk.CTkButton(tela, text="Voltar", command=lambda: [tela.destroy(), tela_professor_1(logado_profe)])
    btn_voltar.pack(pady=20)

    tela.mainloop()

def tela_atribuir_nota(tela_ant, logado_profe):
    tela_ant.destroy()
    tela = ctk.CTk()
    tela.geometry("700x500")
    tela.title("Atribuir Nota")

    ctk.CTkLabel(tela, text="Atribuir Nota a um Aluno", font=("Arial", 16)).pack(pady=15)

    nome_aluno = ctk.CTkEntry(tela, placeholder_text="Nome do Aluno")
    nome_aluno.pack(pady=10)

    atividade = ctk.CTkEntry(tela, placeholder_text="Nome ou texto da atividade")
    atividade.pack(pady=10)

    nota = ctk.CTkEntry(tela, placeholder_text="Nota (0 - 10)")
    nota.pack(pady=10)

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

        resultado = professor.atribuir_nota(
            logado_profe["professor_nome"],
            nome_a,
            atividade_t,
            nota_num
        )

        if resultado == 0:
            messagebox.showerror("Erro", "Arquivo de alunos não encontrado.")
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


#tela_professor_1('dsfdfdf')
index()