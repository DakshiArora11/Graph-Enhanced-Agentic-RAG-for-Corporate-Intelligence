from neo4j import GraphDatabase
from src.utils.logger import get_logger
from config.settings import settings
from src.storage.graph_store import query_triplets

logger = get_logger(__name__)

def query_neo4j(user_query: str) -> list:
    """Determine Cypher query based on rule and run it on Neo4j."""
    user_query_lower = user_query.lower()

    if "filed the report" in user_query_lower:
        cypher_query = """
        MATCH (s:Entity)-[r:RELATION]->(o:Entity)
        WHERE r.type CONTAINS 'file' AND o.name CONTAINS 'report'
        RETURN s.name AS subject, r.type AS predicate, o.name AS object
        """
    elif "sell" in user_query_lower or "sells" in user_query_lower or "products" in user_query_lower:
        cypher_query = """
        MATCH (s:Entity)-[r:RELATION]->(o:Entity)
        WHERE r.type CONTAINS 'sell' OR r.type CONTAINS 'product'
        RETURN s.name AS subject, r.type AS predicate, o.name AS object
        """
    else:
        cypher_query = """
        MATCH (s:Entity)-[r:RELATION]->(o:Entity)
        WHERE s.name CONTAINS $term OR o.name CONTAINS $term
        RETURN s.name AS subject, r.type AS predicate, o.name AS object
        """

    try:
        results = query_triplets(cypher_query.replace("$term", user_query_lower))
        logger.info(f"Graph query returned {len(results)} results.")
        return [f"({r['subject']} --{r['predicate']}--> {r['object']})" for r in results]
    except Exception as e:
        logger.error(f"Failed to execute Cypher query: {str(e)}")
        return ["[ERROR] Cypher execution failed."]