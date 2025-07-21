from neo4j import GraphDatabase
from config.settings import settings

# Initialize Neo4j driver
driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
)

class GraphStore:
    def __init__(self):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_triplet(self, subject, predicate, obj):
        with self.driver.session() as session:
            query = (
                "MERGE (s:Entity {name: $subject})\n"
                "MERGE (o:Entity {name: $object})\n"
                "MERGE (s)-[:RELATION {type: $predicate}]->(o)"
            )
            session.run(query, subject=subject, predicate=predicate, object=obj)

    def query_triplets(self, query_term):
        with self.driver.session() as session:
            query = (
                "MATCH (s:Entity)-[r:RELATION]->(o:Entity)\n"
                "WHERE s.name CONTAINS $term OR r.type CONTAINS $term OR o.name CONTAINS $term\n"
                "RETURN s.name AS subject, r.type AS predicate, o.name AS object"
            )
            result = session.run(query, term=query_term)
            return [f"({r['subject']} --{r['predicate']}--> {r['object']})" for r in result]

# For internal module usage
def query_triplets(cypher_query: str):
    with driver.session() as session:
        result = session.run(cypher_query)
        return [record.data() for record in result]

# === Example run (manual testing) ===
if __name__ == "__main__":
    gstore = GraphStore()
    print("Triplet Query Result:")
    triplets = gstore.query_triplets("Amazon")
    for t in triplets:
        print(t)
    gstore.close()
