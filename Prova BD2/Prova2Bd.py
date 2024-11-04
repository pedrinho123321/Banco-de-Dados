
from neo4j import GraphDatabase

class Database:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

class TeacherCRUD:
    def __init__(self, database):
        self.db = database

    def create(self, name, ano_nasc, cpf):
        query = "CREATE (:Teacher {name: $name, ano_nasc: $ano_nasc, cpf: $cpf})"
        self.db.query(query, {"name": name, "ano_nasc": ano_nasc, "cpf": cpf})

    def read(self, name):
        query = "MATCH (t:Teacher {name: $name}) RETURN t"
        result = self.db.query(query, {"name": name})
        return result

    def delete(self, name):
        query = "MATCH (t:Teacher {name: $name}) DETACH DELETE t"
        self.db.query(query, {"name": name})

    def update(self, name, newCpf):
        query = "MATCH (t:Teacher {name: $name}) SET t.cpf = $newCpf RETURN t"
        self.db.query(query, {"name": name, "newCpf": newCpf})

# Funções de consulta
def questao_01(database):
    # 1. Retornar ano_nasc e CPF do professor Renzo
    query_1 = "MATCH (t:Teacher {name: 'Renzo'}) RETURN t.ano_nasc, t.cpf"
    result_1 = database.query(query_1)
    print("Ano de nascimento e CPF do Renzo:", result_1)

    # 2. Retornar nome e cpf dos professores cujo nome começa com 'M'
    query_2 = "MATCH (t:Teacher) WHERE t.name STARTS WITH 'M' RETURN t.name, t.cpf"
    result_2 = database.query(query_2)
    print("Professores com nome começando com 'M':", result_2)

    # 3. Retornar os nomes de todas as cidades
    query_3 = "MATCH (c:City) RETURN c.name"
    result_3 = database.query(query_3)
    print("Nomes das cidades:", result_3)

    # 4. Retornar nome, endereço e número das escolas com número entre 150 e 550
    query_4 = "MATCH (s:School) WHERE s.number >= 150 AND s.number <= 550 RETURN s.name, s.address, s.number"
    result_4 = database.query(query_4)
    print("Escolas com número entre 150 e 550:", result_4)

def questao_02(database):
    # 1. Ano de nascimento do professor mais jovem e mais velho
    query_1 = "MATCH (t:Teacher) RETURN max(t.ano_nasc) AS MaisNovo, min(t.ano_nasc) AS MaisVelho"
    result_1 = database.query(query_1)
    print("Professor mais jovem e mais velho:", result_1)

    # 2. Média aritmética da população de todas as cidades
    query_2 = "MATCH (c:City) RETURN avg(c.population) AS MediaPopulacao"
    result_2 = database.query(query_2)
    print("Média da população das cidades:", result_2)

    # 3. Cidade com CEP '37540-000' e substituir 'a' por 'A'
    query_3 = "MATCH (c:City {cep: '37540-000'}) RETURN replace(c.name, 'a', 'A') AS NomeModificado"
    result_3 = database.query(query_3)
    print("Cidade com CEP '37540-000' com 'a' trocado por 'A':", result_3)

    # 4. Retornar um caractere iniciando da 3ª letra do nome dos professores
    query_4 = "MATCH (t:Teacher) RETURN substring(t.name, 2) AS NomeSubstr"
    result_4 = database.query(query_4)
    print("Substrings dos nomes dos professores:", result_4)

def main():
    db = Database("bolt://localhost:7687", "neo4j", "password")
    teacher_crud = TeacherCRUD(db)

    # Executando as questões
    print("\nQuestão 01:")
    questao_01(db)

    print("\nQuestão 02:")
    questao_02(db)

    while True:
        print("\nMenu CLI:")
        print("1. Criar Teacher")
        print("2. Ler Teacher")
        print("3. Atualizar Teacher")
        print("4. Deletar Teacher")
        print("5. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            name = input("Nome: ")
            ano_nasc = int(input("Ano de Nascimento: "))
            cpf = input("CPF: ")
            teacher_crud.create(name, ano_nasc, cpf)

        elif choice == "2":
            name = input("Nome: ")
            result = teacher_crud.read(name)
            print(result)

        elif choice == "3":
            name = input("Nome: ")
            new_cpf = input("Novo CPF: ")
            teacher_crud.update(name, new_cpf)

        elif choice == "4":
            name = input("Nome: ")
            teacher_crud.delete(name)

        elif choice == "5":
            break

        else:
            print("Opção inválida, tente novamente.")

    db.close()

if __name__ == "__main__":
    main()
