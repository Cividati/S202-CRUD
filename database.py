from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging

class Graph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def clear(self):
        query = 'MATCH (n) DETACH DELETE n'
        data = []
        with self.driver.session() as session:
            results = session.run(query)
            for record in results:
                data.append(record)
            return data

    def close(self):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        data = []
        with self.driver.session() as session:
            results = session.run(query, parameters)
            for record in results:
                data.append(record)
            return data
