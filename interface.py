from sistema import professor
professor = professor()  
from tkinter import messagebox 
import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("dark-blue")


def tela_profe_cadastro():
    
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
    senha =ctk.CTkEntry(cadastro, placeholder_text= 'senha')
    senha.pack(padx=10, pady=10)

    def profe_cadastro():
        profe_nome = nome.get()
        profe_cpf = cpf.get()
        profe_contato = contato.get()
        profe_diciplina = diciplina.get()
        #usar nome e cpf como "email"
        profe_senha =senha.get()
        if not (profe_nome and profe_cpf and profe_contato and profe_diciplina and profe_senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        
        professor.cadastro(profe_nome,profe_cpf,profe_contato,profe_diciplina,profe_senha)
        messagebox.showinfo("Sucesso", f"Professor {profe_nome} cadastrado!")
       
        nome.delete(0, "end")
        cpf.delete(0, "end")
        contato.delete(0, "end")
        diciplina.delete(0, "end")
        senha.delete(0, "end")    
    
    btn_cadastrar =ctk.CTkButton(cadastro, text="Cadastrar", command=profe_cadastro)
    btn_cadastrar.pack(pady=15)

    cadastro.mainloop()




tela_profe_cadastro()
