from pymongo import MongoClient

class Database:
    def __init__(self, uri="mongodb+srv://root:root@cluster0.cy8op.mongodb.net/", db_name="nome_do_banco"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()

class MotoristaDAO:
    def __init__(self, database):
        self.collection = database.get_collection("Motoristas")

    def create_motorista(self, motorista_data):
        result = self.collection.insert_one(motorista_data)
        return result.inserted_id

    def read_motorista(self, motorista_id):
        return self.collection.find_one({"_id": motorista_id})

    def update_motorista(self, motorista_id, update_data):
        self.collection.update_one({"_id": motorista_id}, {"$set": update_data})

    def delete_motorista(self, motorista_id):
        self.collection.delete_one({"_id": motorista_id})

class Passageiro:
    def __init__(self, nome, documento):
        self.nome = nome
        self.documento = documento

class Corrida:
    def __init__(self, nota, distancia, valor, passageiro):
        self.nota = nota
        self.distancia = distancia
        self.valor = valor
        self.passageiro = passageiro

class Motorista:
    def __init__(self, nota):
        self.nota = nota
        self.corridas = []
    
    def adicionar_corrida(self, corrida):
        self.corridas.append(corrida)     

class MotoristaCLI:
    def __init__(self, motorista_dao):
        self.motorista_dao = motorista_dao

    def menu(self):
        while True:
            print("1. Criar Motorista")
            print("2. Ler Motorista")
            print("3. Atualizar Motorista")
            print("4. Deletar Motorista")
            print("5. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.create_motorista()
            elif opcao == "2":
                self.read_motorista()
            elif opcao == "3":
                self.update_motorista()
            elif opcao == "4":
                self.delete_motorista()
            elif opcao == "5":
                break

    def create_motorista(self):
        nota = int(input("Digite a nota do motorista: "))
        motorista = Motorista(nota)

        while True:
            nome_passageiro = input("Digite o nome do passageiro: ")
            documento_passageiro = input("Digite o documento do passageiro: ")
            passageiro = Passageiro(nome_passageiro, documento_passageiro)

            nota_corrida = int(input("Digite a nota da corrida: "))
            distancia_corrida = float(input("Digite a distancia da corrida: "))
            valor_corrida = float(input("Digite o valor da corrida: "))
            corrida = Corrida(nota_corrida, distancia_corrida, valor_corrida, passageiro)

            motorista.adicionar_corrida(corrida)

            continuar = input("Deseja adicionar outra corrida? (s/n): ")
            if continuar.lower() != "s":
                break

        motorista_id = self.motorista_dao.create_motorista(motorista.__dict__)
        print(f"Motorista criado com ID: {motorista_id}")

    # Outros métodos para read, update e delete...
