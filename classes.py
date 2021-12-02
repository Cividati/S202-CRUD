from database import Graph as Gp

db = Gp('bolt://localhost:7687', 'neo4j', 'harryronyhermione')


class Aluno:
    def __init__(self, nome, casa):
        self.nome = nome
        self.casa = casa
        self.pontos = 0

        self.create()

    def create(self):
        
        # Criando aluno no banco de dados
        query = str(
            'CREATE (a:Aluno {nome: "'+self.nome+'", casa: "'+self.casa+'", pontos: "'+str(self.pontos)+'"})')
        result = db.execute_query(query) 
    
        # criando relacao de pertence a casa
        query = str("MATCH (a:Aluno), (c:Casa) "
        f"WHERE a.nome = '{self.nome}' AND c.nome = '{self.casa}' "
        "CREATE (a)-[r:Pertence]->(c) "
        "RETURN type(r)")
        result = db.execute_query(query)

    def read(self):
        query = str(
            f'MATCH (a:Aluno) WHERE a.nome = "{self.nome}" RETURN a')
        result = db.execute_query(query)
        self.nome = result[0]['a']['nome']
        self.pontos = int(result[0]['a']['pontos'])
        self.casa = result[0]['a']['casa']
        print(f'Nome: {self.nome}\nCasa: {self.casa}\nPontos: {self.pontos}\n')
        return

    def delete(self):
        query = str(
            f'MATCH (a:Aluno) WHERE a.nome = {self.nome} DETACH DELETE a')
        result = db.execute_query(query) 

    def addPontos(self, pontos):
        # busca qtd de pontos atuais
        query = str(
            f'MATCH (a:Aluno) WHERE a.nome = "{self.nome}" RETURN a.pontos')
        result = db.execute_query(query)
       
        # adiciona os pontos novos
        n_pontos = str(int(result[0]['a.pontos']) + pontos)
    
        # salva no db
        query = str(
            f'MATCH (a:Aluno) WHERE a.nome = "{self.nome}" SET a.pontos = "{n_pontos}"')
        result = db.execute_query(query)
        return 
    
    def rmPontos(self, pontos):
        # busca qtd de pontos atuais
        query = str(
            f'MATCH (a:Aluno) WHERE a.nome = "{self.nome}" RETURN a.pontos')
        result = db.execute_query(query)
       
        # adiciona os pontos novos
        n_pontos = str(int(result[0]['a.pontos']) - pontos)
    
        # salva no db
        query = str(
            f'MATCH (a:Aluno) WHERE a.nome = "{self.nome}" SET a.pontos = "{n_pontos}"')
        result = db.execute_query(query)
        return 

class Casa:
    def __init__(self, nome, pontos=0):
        self.nome = nome
        self.pontos = '0'

        self.create()

    def create(self):
        # Criando a casa
        query = str(
            'CREATE (c:Casa {nome: "'+self.nome+'", pontos: "'+self.pontos+'"})')
        result = db.execute_query(query)
        return 

    def updatePontos(self):
        self.pontos = 0 
        query = str(
            f'MATCH (a:Aluno) WHERE a.casa = "{self.nome}" RETURN a')
        result = db.execute_query(query)
        for r in result:
            self.pontos += int(r['a']['pontos'])

        # salva no db
        query = str(
            f'MATCH (c:Casa) WHERE c.nome = "{self.nome}" SET c.pontos = "{self.pontos}"')
        result = db.execute_query(query)
        return 

    def read(self):
        self.updatePontos()
        query = str(
            f'MATCH (c:Casa) WHERE c.nome = "{self.nome}" RETURN c')
        result = db.execute_query(query)
        self.nome = result[0]['c']['nome']
        #self.pontos = int(result[0]['c']['pontos'])
        
        query = str(
            f'MATCH (a:Aluno) WHERE a.casa = "{self.nome}" RETURN a')
        result = db.execute_query(query)
        self.alunos = len(result)

        print(f'Nome: {self.nome}\nPontos: {self.pontos}\nAlunos: {self.alunos}\n')
        return

    def delete(self):
        query = str(
            f'MATCH (c:Casa) WHERE c.nome = {self.nome} DETACH DELETE c')
        result = db.execute_query(query) 
        
        pass
