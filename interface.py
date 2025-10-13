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
    cadastro =ctk.CTk()
    cadastro.geometry('500x400')

    txt = ctk.CTkLabel(cadastro,text='insira seus dados')
    txt.pack(padx=10, pady=10 )
    nome =ctk.CTkEntry(cadastro, placeholder_text= 'nome')
    nome.pack(padx=10, pady=10)
    cpf =ctk.CTkEntry(cadastro, placeholder_text= 'cpf')
    cpf.pack(padx=10, pady=10)
    contato =ctk.CTkEntry(cadastro, placeholder_text= 'contato')
    contato.pack(padx=10, pady=10)
    diciplina =ctk.CTkEntry(cadastro, placeholder_text= 'diciplina')
    diciplina.pack(padx=10, pady=10)
    senha =ctk.CTkEntry(cadastro, placeholder_text= 'senha', show='*')
    senha.pack(padx=10, pady=10)

    def profe_cadastro():
        adm = Adm()
        profe_nome = nome.get()
        profe_cpf = cpf.get()
        profe_contato = contato.get()
        profe_diciplina = diciplina.get()
        #usar nome e cpf como "email"
        profe_senha =senha.get()
        if not (profe_nome and profe_cpf and profe_contato and profe_diciplina and profe_senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return        
        
        ve_profe =   professor.cadastro(profe_nome,profe_cpf,profe_contato,profe_diciplina,profe_senha)
       
        if ve_profe == 3:
            messagebox.showinfo('aaaaaaa',f" professor nao cadastrado por um  ADM")
        else: 
            messagebox.showinfo("Sucesso", f"Professor {profe_nome} cadastrado!")
            tela_logar_professor(cadastro)
       
        nome.delete(0, "end")
        cpf.delete(0, "end")
        contato.delete(0, "end")
        diciplina.delete(0, "end")
        senha.delete(0, "end")    
    
    btn_cadastrar =ctk.CTkButton(cadastro, text="Cadastrar", command=profe_cadastro)
    btn_cadastrar.pack(pady=15)
    tela_index =ctk.CTkButton(cadastro, text="index", command=lambda: index(cadastro))
    tela_index.pack(pady=15)
    cadastro.mainloop()

def tela_logar_professor(tela_ant):
    
    tela_ant.destroy()
    logar_professor =ctk.CTk()
    logar_professor.geometry('500x400')
    
    Log_cpf =ctk.CTkEntry(logar_professor, placeholder_text= 'cpf')
    Log_cpf.pack(padx=10, pady=10)
    log_senha =ctk.CTkEntry(logar_professor, placeholder_text= 'senha')
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
    tela_professor_1.geometry('900x400')
    
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
    tela_adm.geometry('500x400')


    nome =ctk.CTkEntry(tela_adm, placeholder_text= 'nome professor')
    nome.pack(padx=10, pady=10)
    cpf =ctk.CTkEntry(tela_adm, placeholder_text= 'cpf professor')
    cpf.pack(padx=10, pady=10)


    def cadastro_cpf_prof():
        nome_profe = nome.get()
        profe_cpf = cpf.get()
        
        adm.cadastrar_professor_cpf(nome_profe,profe_cpf)

    btn_cpf_prof =ctk.CTkButton(tela_adm, text="cpf", command=cadastro_cpf_prof)
    btn_cpf_prof.pack(pady=15)
    tela_index =ctk.CTkButton(tela_adm, text="index", command=lambda: index(tela_adm))
    tela_index.pack(pady=15)


    tela_adm.mainloop()


def tela_aluno_cadastro(tela_ant):
    tela_ant.destroy()    
    tela_aluno_ca = ctk.CTk() 
    tela_aluno_ca.geometry('500x400')
    

    txt = ctk.CTkLabel(tela_aluno_ca,text='insira seus dados')
    txt.pack(padx=10, pady=10 )
    nome =ctk.CTkEntry(tela_aluno_ca, placeholder_text= 'nome')
    nome.pack(padx=10, pady=10)
    nascimento =ctk.CTkEntry(tela_aluno_ca, placeholder_text= 'data_nascimento')
    nascimento.pack(padx=10, pady=10)
    cpf =ctk.CTkEntry(tela_aluno_ca, placeholder_text= 'cpf')
    cpf.pack(padx=10, pady=10)
    contato =ctk.CTkEntry(tela_aluno_ca, placeholder_text= 'telefone')
    contato.pack(padx=10, pady=10)
    endereco =ctk.CTkEntry(tela_aluno_ca, placeholder_text= 'endereco')
    endereco.pack(padx=10, pady=10)

    def aluno_cadastro():
        
        aluno_nome = nome.get()
        aluno_cpf = cpf.get()
        aluno_contato = contato.get()
        data_nascimento = nascimento.get()
        aluno_endereco = endereco.get()

        if not (aluno_nome and  aluno_cpf  and aluno_contato and data_nascimento):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        
        ve_aluno =   aluno.cadastrar_aluno(aluno_nome,aluno_cpf,data_nascimento,aluno_endereco,aluno_contato)
       
        if ve_aluno == 2 : 
            messagebox.showwarning("Atenção", " cadastrado")
        elif ve_aluno :
            messagebox.showinfo('aaaaaaa',f" aluno nao cadastrado por um")


       
   
    
    btn_cadastrar =ctk.CTkButton(tela_aluno_ca, text="Cadastrar", command=aluno_cadastro)
    btn_cadastrar.pack(pady=15)
    tela_index =ctk.CTkButton(tela_aluno_ca, text="index", command=lambda: index(tela_aluno_ca))
    tela_index.pack(pady=15)
    
    
    tela_aluno_ca.mainloop()

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
    btn_aluno = ctk.CTkButton(index,text='aluno', command=lambda: tela_aluno_cadastro(index) )
    btn_aluno.pack(pady=30)
    index.mainloop()
index()