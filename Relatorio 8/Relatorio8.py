
from neo4j import GraphDatabase

class GameManager:

    def __init__(self, uri, user, password):
        # Inicializa a conexão com o banco de dados
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Fecha a conexão com o banco de dados
        self.driver.close()

    # Cria um jogador
    def create_player(self, player_id, name):
        with self.driver.session() as session:
            session.run(
                "CREATE (p:Player {id: $player_id, name: $name})",
                player_id=player_id, name=name
            )
    
    # Atualiza o nome de um jogador
    def update_player(self, player_id, new_name):
        with self.driver.session() as session:
            session.run(
                "MATCH (p:Player {id: $player_id}) "
                "SET p.name = $new_name",
                player_id=player_id, new_name=new_name
            )

    # Exclui um jogador
    def delete_player(self, player_id):
        with self.driver.session() as session:
            session.run(
                "MATCH (p:Player {id: $player_id}) "
                "DETACH DELETE p",
                player_id=player_id
            )
    
    # Recupera a lista de jogadores
    def get_players(self):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Player) RETURN p.id AS id, p.name AS name")
            return [{"id": record["id"], "name": record["name"]} for record in result]

    # Cria uma partida entre dois ou mais jogadores e registra o resultado
    def create_match(self, match_id, player_ids, result):
        with self.driver.session() as session:
            session.run(
                "CREATE (m:Match {id: $match_id, result: $result})",
                match_id=match_id, result=result
            )
            for player_id in player_ids:
                session.run(
                    "MATCH (p:Player {id: $player_id}), (m:Match {id: $match_id}) "
                    "CREATE (p)-[:PLAYED]->(m)",
                    player_id=player_id, match_id=match_id
                )

    # Atualiza o resultado de uma partida
    def update_match_result(self, match_id, new_result):
        with self.driver.session() as session:
            session.run(
                "MATCH (m:Match {id: $match_id}) "
                "SET m.result = $new_result",
                match_id=match_id, new_result=new_result
            )

    # Exclui uma partida
    def delete_match(self, match_id):
        with self.driver.session() as session:
            session.run(
                "MATCH (m:Match {id: $match_id}) "
                "DETACH DELETE m",
                match_id=match_id
            )

    # Recupera informações de uma partida específica
    def get_match(self, match_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (m:Match {id: $match_id}) "
                "RETURN m.id AS id, m.result AS result",
                match_id=match_id
            )
            record = result.single()
            if record:
                return {"id": record["id"], "result": record["result"]}
            else:
                return None
    
    # Recupera o histórico de partidas de um jogador
    def get_player_matches(self, player_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Player {id: $player_id})-[:PLAYED]->(m:Match) "
                "RETURN m.id AS match_id, m.result AS result",
                player_id=player_id
            )
            return [{"match_id": record["match_id"], "result": record["result"]} for record in result]


# Exemplo de uso
if __name__ == "__main__":
    # Conexão com o Neo4j
    game_manager = GameManager("bolt://localhost:7687", "neo4j", "password")

    # Criar jogadores
    game_manager.create_player("1", "Jogador 1")
    game_manager.create_player("2", "Jogador 2")

    # Criar uma partida entre Jogador 1 e Jogador 2 com resultado
    game_manager.create_match("m1", ["1", "2"], "Jogador 1 venceu")

    # Obter lista de jogadores
    players = game_manager.get_players()
    print(players)

    # Obter informações de uma partida específica
    match = game_manager.get_match("m1")
    print(match)

    # Obter histórico de partidas de um jogador
    player_matches = game_manager.get_player_matches("1")
    print(player_matches)

    # Fechar a conexão com o banco de dados
    game_manager.close()
