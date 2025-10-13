import json          
import bcrypt   
import socket
from tkinter import messagebox 


SERVER_IP = "192.168.1.201"  # ex: "192.168.0.100"
SERVER_PORT = 5000

def enviar_servidor(tipo, dados):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        payload = {"tipo": tipo, "dados": dados}
        s.send(json.dumps(payload).encode())
        s.recv(1024)
    except Exception as e:
        print("Erro no envio:", e)
    finally:
        s.close()

def receber_servidor(tipo):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        s.send(json.dumps({"tipo": tipo}).encode())
        data = s.recv(4096)
        return json.loads(data)
    except Exception as e:
        print("Erro no recebimento:", e)
        return None
    finally:
        s.close()
        
        
class Professor:
    def __init__(self):

        self.professor_lista = receber_servidor("get_professor") or []
 

    def cadastro(self, profe_nome, profe_cpf, profe_contato, profe_diciplina, profe_senha):

        adm = Adm()
        cpf_ve = adm.adm_ve(profe_cpf)
        
        if not adm.adm_ve(profe_cpf):
            return 3

        professor = {
            'professor_nome': profe_nome,
            'professor_cpf': profe_cpf,
            'professor_contato': profe_contato,
            'professor_diciplina': profe_diciplina,
            'professor_senha': bcrypt.hashpw(profe_senha.encode(), bcrypt.gensalt()).decode(),
        }

        self.professor_lista.append(professor)
        enviar_servidor("professor",self.professor_lista)

    def logar(self, profe_cpf, profe_senha):
        
        if profe_cpf == "adm123" and profe_senha == 'adm123':
            return 3
        
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
        enviar_servidor('Professor',self.professor_lista)

class Adm :
    def __init__(self):
        self.adm_dados = receber_servidor("get_adm") or {"login_adm":"adm123","senha_adm":"adm123",'cpf_professor':[]}

    def cadastrar_professor_cpf(self,nome_profe ,cpf_professor):
        novo_profe = {
            "nome": nome_profe,
            "cpf": cpf_professor
        }
        self.adm_dados['cpf_professor'].append(novo_profe)
        enviar_servidor("adm", self.adm_dados)

    def adm_ve(self,profe_cpf):
    
        return any(prof.get("cpf") == profe_cpf for prof in self.adm_dados.get("cpf_professor", []))