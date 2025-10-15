from sistema import Professor
professor = Professor()  
from tkinter import messagebox 
import customtkinter as ctk
from sistema import Adm
adm = Adm()
from sistema import Aluno
aluno = Aluno()
from PIL import Image



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

def tela_professor_1(logado_profe):
    
    tela_professor_1 =ctk.CTk()
    tela_professor_1.geometry('500x500')

    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 500)
    )
    fundo = ctk.CTkLabel(tela_professor_1 , image=img_fundo, text='')
    fundo.place(x=0, y=0)
    


    texto = ctk.CTkLabel(tela_professor_1, text=f"Professor {logado_profe}", font=("Arial", 10))  
    texto.pack(pady=50) 
    nome_al =ctk.CTkEntry(tela_professor_1, placeholder_text= 'nome')
    nome_al.pack(padx=10, pady=10)
    
    def alterar():
        
        nome = nome_al.get()
        logado_profe_al = logado_profe
        professor.alterar(logado_profe_al, nome)
    
    btn_logar_prof =ctk.CTkButton(tela_professor_1, text="alterar", command=alterar)
    btn_logar_prof.pack(pady=15)
    tela_index =ctk.CTkButton(tela_professor_1, text="index", command=lambda: index(tela_professor_1))
    tela_index.pack(pady=15)
    tela_professor_1.mainloop()

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
            tela_professor_1(logado_aluno)
            
    
    btn_logar_aluno =ctk.CTkButton(logar_aluno, text="logar", command=aluno_login)
    btn_logar_aluno.pack(pady=15)
    
    btn_aluno_cadastro = ctk.CTkButton(logar_aluno, text="cadastrar", command=lambda :tela_aluno_cadastro(logar_aluno))
    btn_aluno_cadastro.pack(pady=15)
    tela_index =ctk.CTkButton(logar_aluno, text="index", command=lambda: index(logar_aluno))
    tela_index.pack(pady=15)
    logar_aluno.mainloop()






def tela_aluno_1():
    


    index_aluno =ctk.CTk()
    index_aluno.geometry('500x500')

    img_fundo = ctk.CTkImage(
        light_image=Image.open('img.png'),
        dark_image=Image.open('img.png'),
        size=(500, 500)
    )
    fundo = ctk.CTkLabel(index_aluno , image=img_fundo, text='')
    fundo.place(x=0, y=0)
    



    index_aluno.mainloop()









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

    # 🔽 pega apenas coordenadores
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
index()