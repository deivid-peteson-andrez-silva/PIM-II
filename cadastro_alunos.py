import json      # Para trabalhar com arquivos JSON (armazenamento e leitura dos dados)
import os        # Para manipular diretórios e verificar se arquivos/pastas existem


# Definição da classe 'Aluno'
class Aluno:
    def __init__(self):
        """
        Construtor da classe Aluno.
        É executado automaticamente quando criamos um objeto da classe.
        Serve para garantir que o arquivo JSON e a pasta existam,
        além de carregar os dados dos alunos já cadastrados.
        """
        
        # Cria uma pasta chamada 'arquivos' se ela ainda não existir
        os.makedirs("arquivos", exist_ok=True)
        
        # Verifica se o arquivo 'alunos.json' já existe
        if os.path.exists('arquivos/alunos.json'):
            # Abre o arquivo no modo leitura
            with open('arquivos/alunos.json', 'r') as arquivo:
                try:
                    # Tenta carregar os dados em formato JSON
                    self.aluno_lista = json.load(arquivo)
                    
                    # Se o arquivo não for uma lista (pode ter sido corrompido), cria lista vazia
                    if not isinstance(self.aluno_lista, list):
                        self.aluno_lista = []
                
                # Caso o arquivo esteja vazio ou com erro de formatação
                except json.JSONDecodeError:
                    self.aluno_lista = []
        else:
            # Se o arquivo não existir, cria uma lista vazia
            self.aluno_lista = []

    
    def cadastrar_aluno(self, nome, cpf, data_nascimento, endereco, telefone):
        """
        Método responsável por cadastrar um novo aluno no sistema.
        Recebe os dados como parâmetros e adiciona no arquivo JSON.
        """
        
        # Cria um dicionário (estrutura tipo JSON) com as informações do aluno
        aluno = {
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento,
            'endereco': endereco,
            'telefone': telefone
        }
        
        # Adiciona o novo aluno na lista atual de alunos
        self.aluno_lista.append(aluno)
        
        # Abre o arquivo no modo escrita para salvar os dados atualizados
        with open('arquivos/alunos.json', 'w') as arquivo:
            # json.dump salva os dados no arquivo
            # indent=4 serve para deixar o JSON bem formatado (legível)
            json.dump(self.aluno_lista, arquivo, indent=4)
        
        print(f"✅ Aluno '{nome}' cadastrado com sucesso!")


# Exemplo de uso do sistema
if __name__ == "__main__":
    sistema = Aluno()  # Cria o objeto da classe
    
    while True:
        print("\n===== SISTEMA DE CADASTRO DE ALUNOS =====")
        print("1 - Cadastrar novo aluno")
        print("2 - Listar alunos cadastrados")
        print("3 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nome = input("Nome completo: ")
            cpf = input("CPF: ")
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
            endereco = input("Endereço: ")
            telefone = input("Telefone: ")
            
            sistema.cadastrar_aluno(nome, cpf, data_nascimento, endereco, telefone)
        
        elif opcao == "2":
            print("\n=== Lista de Alunos Cadastrados ===")
            for aluno in sistema.aluno_lista:
                print(f"Nome: {aluno['nome']}")
                print(f"CPF: {aluno['cpf']}")
                print(f"Data de Nascimento: {aluno['data_nascimento']}")
                print(f"Endereço: {aluno['endereco']}")
                print(f"Telefone: {aluno['telefone']}")
                print("--------------------------")
        
        elif opcao == "3":
            print("Saindo do sistema... 👋")
            break
        
        else:
            print("❌ Opção inválida! Tente novamente.")
