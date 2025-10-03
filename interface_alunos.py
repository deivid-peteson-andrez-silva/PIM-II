from sistema import professor
professor = professor()  



profe_nome = input('nome')

profe_cpf = input('cpf')

profe_contato = input('contato')

profe_diciplina = input('diciplina')
#usar nome e cpf como "email"
profe_senha = input('senha')

professor.cadastro(profe_nome,profe_cpf,profe_contato,profe_diciplina,profe_senha)