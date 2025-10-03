import json
import os
import  hashlib
import bcrypt
class professor:
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
    
    def cadastro(self,profe_nome, profe_cpf, profe_contato,profe_diciplina,profe_senha):
        professor={'professor_nome':profe_nome,
                  'professor_cpf':profe_cpf,
                  'professor_contato':profe_contato,
                  'professor_diciplina':profe_diciplina,
                  'professor_senha':bcrypt.hashpw(profe_senha.encode(), bcrypt.gensalt()).decode(),
                  }
        self.professor_lista.append(professor)
        with open('arquivos/professor.json', 'w') as arquivo:
            json.dump(self.professor_lista,arquivo,indent=4)
      