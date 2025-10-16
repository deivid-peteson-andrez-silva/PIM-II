import json      
import os        
import bcrypt    


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
    

    def cadastro(self, profe_nome, profe_cpf, profe_contato, profe_curso, profe_senha):

        adm = Adm()
        cpf_ve = adm.adm_ve(profe_cpf)
        
        if cpf_ve:

            professor = {
                'professor_nome': profe_nome,
                'professor_cpf': profe_cpf,
                'professor_contato': profe_contato,
                'professor_diciplina': profe_curso,
                
 
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
            
    def alterar(self, logado_profe, novo_nome):
        for p in self.professor_lista:
            if p["professor_cpf"] == logado_profe["professor_cpf"]:
                p["professor_nome"] = novo_nome
                break

        with open('arquivos/professor.json', 'w', encoding='utf-8') as arquivo:
            json.dump(self.professor_lista, arquivo, indent=4, ensure_ascii=False)
                

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
    

    def cadastro(self, profe_nome, profe_cpf, profe_contato, profe_curso, profe_senha):

        adm = Adm()
        cpf_ve = adm.adm_ve(profe_cpf)
        
        if cpf_ve:

            professor = {
                'professor_nome': profe_nome,
                'professor_cpf': profe_cpf,
                'professor_contato': profe_contato,
                'professor_diciplina': profe_curso,
                
 
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
            
    def alterar(self, logado_profe, novo_nome):
        for p in self.professor_lista:
            if p["professor_cpf"] == logado_profe["professor_cpf"]:
                p["professor_nome"] = novo_nome
                break

        with open('arquivos/professor.json', 'w', encoding='utf-8') as arquivo:
            json.dump(self.professor_lista, arquivo, indent=4, ensure_ascii=False)
                
    def atividade(self, nome_profe, texto_digitado):
        for professor in self.professor_lista:
            if professor["professor_nome"] == nome_profe:
                if "atividades" not in professor:
                    professor["atividades"] = []
                professor["atividades"].append(texto_digitado)

                # Salva no adm.json no curso correspondente
                try:
                    with open("arquivos/adm.json", "r", encoding="utf-8") as arquivo:
                        dados_adm = json.load(arquivo)

                    for curso in dados_adm.get("curso_diciplina", []):
                        if curso["nome_curso"] == professor["professor_diciplina"]:
                            if "atividades" not in curso:
                                curso["atividades"] = []
                            # Adiciona a nova atividade
                            curso["atividades"].append({
                                "professor": nome_profe,
                                "texto": texto_digitado
                            })

                    with open("arquivos/adm.json", "w", encoding="utf-8") as arquivo:
                        json.dump(dados_adm, arquivo, indent=4, ensure_ascii=False)
                except Exception as e:
                    print("Erro ao salvar atividade no curso:", e)

                # Salva no professor.json
                with open("arquivos/professor.json", "w", encoding="utf-8") as arquivo:
                    json.dump(self.professor_lista, arquivo, indent=4, ensure_ascii=False)
                return 1
        return 0
    
    
    
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
            self.adm_dados = {"login_adm":"adm123","senha_adm":"adm123",'cpf_professor':[],"curso_diciplina":[]}
    def cadastrar_professor_cpf(self,nome_profe ,cpf_professor,coordenador=False):
        novo_profe = {
            "nome": nome_profe,
            "cpf": cpf_professor,
             "coordenador": coordenador
        }
        self.adm_dados['cpf_professor'].append(novo_profe)
 
        with open('arquivos/adm.json', 'w') as arquivo:
            json.dump(self.adm_dados,arquivo,indent=4)
      
      
    def cadastrar_curso(self,nome,profe_coordenador,carga_hora):
        novo_curso={
            'nome_curso':nome,
            'professor_coordenador':profe_coordenador,
            'curso_carga_hora':carga_hora
        }

        self.adm_dados['curso_diciplina'].append(novo_curso)
        with open('arquivos/adm.json', 'w') as arquivo:
            json.dump(self.adm_dados,arquivo,indent=4)       
    
    def listar_cursos(self):

        try:
            with open('arquivos/adm.json', 'r') as arquivo:
                dados = json.load(arquivo)
                return [curso['nome_curso'] for curso in dados.get('curso_diciplina', [])]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def listar_coordenadores(self):

        try:
            with open('arquivos/adm.json', 'r') as arquivo:
                dados = json.load(arquivo)
                return [prof['nome'] for prof in dados.get('cpf_professor', []) if prof.get('coordenador')]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    
    
    
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

    
    def cadastrar_aluno(self, nome, cpf, data_nascimento, endereco, telefone,senha,curso ):

        aluno = {
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento,
            'endereco': endereco,
            'telefone': telefone,
            'curso': curso,
            'senha': bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode(),
        }
        

        self.aluno_lista.append(aluno)

        with open('arquivos/alunos.json', 'w') as arquivo:

            json.dump(self.aluno_lista, arquivo, indent=4)
        
        return
    def logar_aluno(self, aluno_cpf, aluno_senha):
            """
        faz o login do alno meio obivio ne
            """
            aluno_encontrado = None
            cpf_login = aluno_cpf
            
            # Procura o aluno pelo CPF
            for aluno in self.aluno_lista:
                if aluno['cpf'] == cpf_login:
                    aluno_encontrado = aluno
                    break
            
            if not aluno_encontrado:
                return 1 
            else:
                # Verifica a senha
                if bcrypt.checkpw(aluno_senha.encode(), aluno_encontrado['senha'].encode()):
                    return aluno_encontrado  
                else:
                    return 2  
        
        
        
        
        
    def ver_atividades(self, nome_aluno):
        for aluno in self.aluno_lista:
            if aluno["nome"] == nome_aluno:
                curso = aluno["curso"]
                atividades_totais = []
                try:
                    with open("arquivos/adm.json", "r", encoding="utf-8") as arquivo:
                        dados_adm = json.load(arquivo)

                    for curso_dados in dados_adm.get("curso_diciplina", []):
                        if curso_dados["nome_curso"] == curso:
                            atividades_totais.extend(curso_dados.get("atividades", []))
                except Exception as e:
                    print("Erro ao carregar atividades:", e)
                return atividades_totais
        return []

    def enviar_resposta(self, nome_aluno, professor_nome, resposta):
        """
        Aluno envia uma resposta de atividade para o professor
        """
        for aluno in self.aluno_lista:
            if aluno["nome"] == nome_aluno:
                if "respostas" not in aluno:
                    aluno["respostas"] = []
                aluno["respostas"].append({
                    "professor": professor_nome,
                    "resposta": resposta
                })

                with open("arquivos/alunos.json", "w", encoding="utf-8") as arquivo:
                    json.dump(self.aluno_lista, arquivo, indent=4, ensure_ascii=False)
                return 1
        return 0

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
            self.adm_dados = {"login_adm":"adm123","senha_adm":"adm123",'cpf_professor':[],"curso_diciplina":[]}
    def cadastrar_professor_cpf(self,nome_profe ,cpf_professor,coordenador=False):
        novo_profe = {
            "nome": nome_profe,
            "cpf": cpf_professor,
             "coordenador": coordenador
        }
        self.adm_dados['cpf_professor'].append(novo_profe)
 
        with open('arquivos/adm.json', 'w') as arquivo:
            json.dump(self.adm_dados,arquivo,indent=4)
      
      
    def cadastrar_curso(self,nome,profe_coordenador,carga_hora):
        novo_curso={
            'nome_curso':nome,
            'professor_coordenador':profe_coordenador,
            'curso_carga_hora':carga_hora
        }

        self.adm_dados['curso_diciplina'].append(novo_curso)
        with open('arquivos/adm.json', 'w') as arquivo:
            json.dump(self.adm_dados,arquivo,indent=4)       
    
    def listar_cursos(self):

        try:
            with open('arquivos/adm.json', 'r') as arquivo:
                dados = json.load(arquivo)
                return [curso['nome_curso'] for curso in dados.get('curso_diciplina', [])]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def listar_coordenadores(self):

        try:
            with open('arquivos/adm.json', 'r') as arquivo:
                dados = json.load(arquivo)
                return [prof['nome'] for prof in dados.get('cpf_professor', []) if prof.get('coordenador')]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    
    
    
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

    
    def cadastrar_aluno(self, nome, cpf, data_nascimento, endereco, telefone,senha,curso ):

        aluno = {
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento,
            'endereco': endereco,
            'telefone': telefone,
            'curso': curso,
            'senha': bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode(),
        }
        

        self.aluno_lista.append(aluno)

        with open('arquivos/alunos.json', 'w') as arquivo:

            json.dump(self.aluno_lista, arquivo, indent=4)
        
        return
    def logar_aluno(self, aluno_cpf, aluno_senha):
            """
        faz o login do alno meio obivio ne
            """
            aluno_encontrado = None
            cpf_login = aluno_cpf
            
            # Procura o aluno pelo CPF
            for aluno in self.aluno_lista:
                if aluno['cpf'] == cpf_login:
                    aluno_encontrado = aluno
                    break
            
            if not aluno_encontrado:
                return 1 
            else:
                # Verifica a senha
                if bcrypt.checkpw(aluno_senha.encode(), aluno_encontrado['senha'].encode()):
                    return aluno_encontrado  
                else:
                    return 2  
        
    def ver_atividades(self, nome_aluno):
        for aluno in self.aluno_lista:
            if aluno["nome"] == nome_aluno:
                curso = aluno["curso"]
                atividades_totais = []
                try:
                    with open("arquivos/adm.json", "r", encoding="utf-8") as arquivo:
                        dados_adm = json.load(arquivo)

                    for curso_dados in dados_adm.get("curso_diciplina", []):
                        if curso_dados["nome_curso"] == curso:
                            atividades_totais.extend(curso_dados.get("atividades", []))
                except Exception as e:
                    print("Erro ao carregar atividades:", e)
                return atividades_totais
        return []

    def enviar_resposta(self, nome_aluno, professor_nome, resposta):
        """
        Aluno envia uma resposta de atividade para o professor
        """
        for aluno in self.aluno_lista:
            if aluno["nome"] == nome_aluno:
                if "respostas" not in aluno:
                    aluno["respostas"] = []
                aluno["respostas"].append({
                    "professor": professor_nome,
                    "resposta": resposta
                })

                with open("arquivos/alunos.json", "w", encoding="utf-8") as arquivo:
                    json.dump(self.aluno_lista, arquivo, indent=4, ensure_ascii=False)
                return 1
        return 0