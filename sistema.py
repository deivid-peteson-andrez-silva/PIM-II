
import json
import os
import socket

SERVER_IP = "192.168.1.201"  # ajuste conforme o IP da máquina do servidor
SERVER_PORT = 5000


def enviar_servidor(tipo, dados):
    """Envia dados ao servidor."""
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
    """Recebe dados do servidor."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        s.send(json.dumps({"tipo": tipo}).encode())
        chunks = []
        while True:
            part = s.recv(4096)
            if not part:
                break
            chunks.append(part)
        data = b"".join(chunks)

        return json.loads(data)
    except Exception as e:
        print("Erro no recebimento:", e)
        return None
    finally:
        s.close()



# CLASSE PROFESSOR


class Professor:
    def __init__(self):
        self.professor_lista = receber_servidor("get_professor") or []

    def cadastro(self, nome, cpf, contato, curso, senha):
        adm = Adm()
        if not adm.adm_ve(cpf):
            return 3  

        professor = {
            "professor_nome": nome,
            "professor_cpf": cpf,
            "professor_contato": contato,
            "professor_diciplina": curso,
            "professor_senha": senha,

        }

        self.professor_lista.append(professor)
        enviar_servidor("professor", self.professor_lista)
        return 1

    def logar(self, cpf, senha):
        if cpf == "adm123" and senha == "adm123":
            return 3  

        for professor in self.professor_lista:
            if professor["professor_cpf"] == cpf:
                if senha == professor["professor_senha"]:

                    return professor
                else:
                    return 2  
        return 1  

    def alterar(self, prof_logado, novo_nome):
        for prof in self.professor_lista:
            if prof["professor_cpf"] == prof_logado["professor_cpf"]:
                prof["professor_nome"] = novo_nome
                break
        enviar_servidor("professor", self.professor_lista)

    def atividade(self, nome_profe, texto_digitado):
        """Professor cria uma atividade"""
        for professor in self.professor_lista:
            if professor["professor_nome"] == nome_profe:
                professor.setdefault("atividades", []).append(texto_digitado)
                enviar_servidor("professor", self.professor_lista)

    
                adm_dados = receber_servidor("get_adm") or {}
                for curso in adm_dados.get("curso_diciplina", []):
                    if curso.get("nome_curso") == professor["professor_diciplina"]:
                        curso.setdefault("atividades", []).append({
                            "professor": nome_profe,
                            "texto": texto_digitado
                        })
                enviar_servidor("adm", adm_dados)
                return 1
        return 0

    def salvar_notas(self, nome_prof, respostas):
        """Salva notas corrigidas de alunos."""
        alunos = receber_servidor("get_aluno") or []
        for aluno in alunos:
            for r in aluno.get("respostas", []):
                if r.get("professor") == nome_prof:
                    r["nota"] = respostas.get(r["atividade"], 0)
        enviar_servidor("aluno", alunos)



# CLASSE ALUNO


class Aluno:
    def __init__(self):
        self.aluno_lista = receber_servidor("get_aluno") or []

    def cadastrar_aluno(self, nome, cpf, data_nasc, endereco, telefone, senha, curso):
        aluno = {
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": data_nasc,
            "endereco": endereco,
            "telefone": telefone,
            "curso": curso,
            "senha": senha,

        }
        self.aluno_lista.append(aluno)
        enviar_servidor("aluno", self.aluno_lista)

    def logar_aluno(self, cpf, senha):
        for aluno in self.aluno_lista:
            if aluno["cpf"] == cpf:
                if senha == aluno["senha"]:
                    return aluno
                else:
                    return 2
        return 1

    def ver_atividades(self, nome_aluno):
        atividades_disponiveis = []
        alunos = receber_servidor("get_aluno") or []
        professores = receber_servidor("get_professor") or []

        aluno_atual = next((a for a in alunos if a["nome"] == nome_aluno), None)
        if not aluno_atual:
            return []

        respostas = aluno_atual.get("respostas", [])

        for prof in professores:
            nome_prof = prof.get("professor_nome")
            for atividade in prof.get("atividades", []):
                ja_respondeu = any(
                    r.get("atividade") == atividade and r.get("professor") == nome_prof
                    for r in respostas
                )
                if not ja_respondeu:
                    atividades_disponiveis.append({
                        "professor": nome_prof,
                        "texto": atividade
                    })
        return atividades_disponiveis

    def enviar_resposta(self, nome_aluno, professor, resposta, atividade):
        alunos = receber_servidor("get_aluno") or []
        for a in alunos:
            if a["nome"] == nome_aluno:
                a.setdefault("respostas", [])
                if not any(r["atividade"] == atividade and r["professor"] == professor for r in a["respostas"]):
                    a["respostas"].append({
                        "professor": professor,
                        "atividade": atividade,
                        "resposta": resposta
                    })
        enviar_servidor("aluno", alunos)

    def calcular_media(self, nome_aluno):
        alunos = receber_servidor("get_aluno") or []
        medias = {}
        for a in alunos:
            if a["nome"] == nome_aluno:
                for r in a.get("respostas", []):
                    prof = r["professor"]
                    nota = r.get("nota", 0)
                    medias.setdefault(prof, []).append(nota)
        for prof in medias:
            notas = medias[prof]
            medias[prof] = sum(notas) / len(notas) if notas else 0
        return medias



# CLASSE ADM


class Adm:
    def __init__(self):
        self.adm_dados = receber_servidor("get_adm") 

    def cadastrar_professor_cpf(self, nome, cpf, coordenador=False):
        novo_profe = {
            "nome": nome,
            "cpf": cpf,
            "coordenador": coordenador
        }
        self.adm_dados["cpf_professor"].append(novo_profe)
        enviar_servidor("adm", self.adm_dados)

    def cadastrar_curso(self, nome, coordenador, carga_hora):
        novo_curso = {
            "nome_curso": nome,
            "professor_coordenador": coordenador,
            "curso_carga_hora": carga_hora
        }
        self.adm_dados["curso_diciplina"].append(novo_curso)
        enviar_servidor("adm", self.adm_dados)

    def listar_cursos(self):
        return [c["nome_curso"] for c in self.adm_dados.get("curso_diciplina", [])]

    def listar_coordenadores(self):
        return [p["nome"] for p in self.adm_dados.get("cpf_professor", []) if p.get("coordenador")]

    def adm_ve(self, cpf):
        return any(p["cpf"] == cpf for p in self.adm_dados.get("cpf_professor", []))
