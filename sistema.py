import json      # Para trabalhar com arquivos JSON (leitura e escrita de dados estruturados)
import os        # Para verificar e manipular caminhos e pastas do sistema operacional
import bcrypt    # Biblioteca para criptografar senhas de forma segura
from tkinter import messagebox 
import random

# Definição da classe 'professor'
class Professor:
    def __init__(self):
        """
        Construtor da classe professor.
        Essa função é executada sempre que um objeto da classe é criado.
        Aqui garantimos que o arquivo JSON que vai armazenar os professores exista,
        e carregamos os dados salvos (se existirem).
        """
        
        # Cria a pasta 'arquivos' caso ela não exista
        os.makedirs("arquivos", exist_ok=True) 
        
        # Verifica se o arquivo JSON já existe
        if os.path.exists('arquivos/professor.json'):
            # Se o arquivo existir, abrimos ele no modo leitura
            with open('arquivos/professor.json', 'r') as arquivo:
                try:
                    # Tentamos carregar os dados em formato JSON
                    self.professor_lista = json.load(arquivo)
                    
                    # Se o arquivo não contiver uma lista (pode estar corrompido), cria lista vazia
                    if not isinstance(self.professor_lista, list):
                        self.professor_lista = []
                
                # Caso o JSON esteja vazio ou mal formatado, criamos lista vazia
                except json.JSONDecodeError:
                    self.professor_lista = []
         
        else:
            # Se o arquivo não existir, iniciamos com uma lista vazia
            self.professor_lista = [] 
    

    def cadastro(self, profe_nome, profe_cpf, profe_contato, profe_diciplina, profe_senha):
        """
        Método responsável por cadastrar um novo professor no sistema.
        Recebe os dados do professor, organiza em um dicionário e salva no arquivo JSON.
        """
        adm = Adm()
        cpf_ve = adm.adm_ve(profe_cpf)
        
        if cpf_ve:
            # Cria um dicionário com os dados do professor
            professor = {
                'professor_nome': profe_nome,
                'professor_cpf': profe_cpf,
                'professor_contato': profe_contato,
                'professor_diciplina': profe_diciplina,
                
                # A senha é criptografada usando bcrypt para garantir segurança
                'professor_senha': bcrypt.hashpw(profe_senha.encode(), bcrypt.gensalt()).decode(),
            }
            
            # Adiciona o novo professor à lista já existente
            self.professor_lista.append(professor)
            
            # Abre o arquivo no modo escrita e salva toda a lista de professores
            with open('arquivos/professor.json', 'w') as arquivo:
                # json.dump salva no arquivo em formato JSON
                # indent=4 serve para deixar o arquivo legível (com espaçamento)
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
    