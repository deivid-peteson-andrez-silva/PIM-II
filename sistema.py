import json      
import os        
import bcrypt    
from tkinter import messagebox 
import random


class Professor:
    def __init__(self):
        
        os.makedirs("arquivos", exist_ok=True) 
        
 
        if os.path.exists('arquivos/professor.json'):

            with open('arquivos/professor.json', 'r') as arquivo:
                try:

                    self.professor_lista = json.load(arquivo)

                    if not isinstance(self.professor_lista, list):
                        self.professor_lista = []
                
                except json.JSONDecodeError:
                    self.professor_lista = []
         
        else:
            self.professor_lista = [] 
    

    def cadastro(self, profe_nome, profe_cpf, profe_contato, profe_diciplina, profe_senha):

        adm = Adm()
        cpf_ve = adm.adm_ve(profe_cpf)
        
        if cpf_ve:

            professor = {
                'professor_nome': profe_nome,
                'professor_cpf': profe_cpf,
                'professor_contato': profe_contato,
                'professor_diciplina': profe_diciplina,
                
 
                'professor_senha': bcrypt.hashpw(profe_senha.encode(), bcrypt.gensalt()).decode(),
            }
            

            self.professor_lista.append(professor)
            
            with open('arquivos/professor.json', 'w') as arquivo:

                json.dump(self.professor_lista, arquivo, indent=4)

        else:
            return 3
    def logar(self, profe_cpf, profe_senha):
        cpf_v = None
        prof_logar = profe_cpf
        for professor in self.professor_lista:
            if professor['professor_cpf'] == prof_logar:
                cpf_v = professor
                break
        
        if not cpf_v:
            return 1
        else:
            if bcrypt.checkpw(profe_senha.encode(), cpf_v['professor_senha'].encode()):
                return professor
            else:
                return 2 
            
    def alterar(self,logado_profe,alteracao):
        
        novo_nome = alteracao
        logado_profe['professor_nome'] = novo_nome
        with open('arquivos/professor.json', 'w') as arquivo:
            json.dump(self.professor_lista, arquivo, indent=4)

class Adm :
    def __init__(self):
        os.makedirs("arquivos", exist_ok=True) 
        if os.path.exists('arquivos/adm.json'):
            with open('arquivos/adm.json', 'r') as arquivo:
                try:
                    self.adm_dados = json.load(arquivo)
                    if not isinstance(self.adm_dados, dict):
                            cpf_profe = None
                            self.adm_dados = {"login_adm":"adm123","senha_adm":"adm123",'cpf_professor':[]}
                except json.JSONDecodeError:
                    self.adm_dados = {"login_adm":"adm123","senha_adm":"adm123","cpf_professor":[]}
        else:
            self.adm_dados = {"login_adm":"adm123","senha_adm":"adm123",'cpf_professor':[]}
    def cadastrar_professor_cpf(self,nome_profe ,cpf_professor):
        novo_profe = {
            "nome": nome_profe,
            "cpf": cpf_professor
        }
        self.adm_dados['cpf_professor'].append(novo_profe)
 
        with open('arquivos/adm.json', 'w') as arquivo:
            json.dump(self.adm_dados,arquivo,indent=4)
      
    def adm_ve(self,profe_cpf):
        for prof in self.adm_dados["cpf_professor"]:
            if prof["cpf"] == profe_cpf:
                return True
        
        
        return False
    

class Aluno:
    def __init__(self):

        os.makedirs("arquivos", exist_ok=True)
        

        if os.path.exists('arquivos/alunos.json'):
    
            with open('arquivos/alunos.json', 'r') as arquivo:
                try:
                    self.aluno_lista = json.load(arquivo)

                    if not isinstance(self.aluno_lista, list):
                        self.aluno_lista = []

                except json.JSONDecodeError:
                    self.aluno_lista = []
        else:

            self.aluno_lista = []

    
    def cadastrar_aluno(self, nome, cpf, data_nascimento, endereco, telefone,):

        aluno = {
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento,
            'endereco': endereco,
            'telefone': telefone
        }
        

        self.aluno_lista.append(aluno)

        with open('arquivos/alunos.json', 'w') as arquivo:

            json.dump(self.aluno_lista, arquivo, indent=4)
        
        return
