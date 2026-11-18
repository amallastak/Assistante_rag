import psycopg2
from sentence_transformers import SentenceTransformer

DB_CONFIG = {
    "dbname": "bo_db",
    "user": "amal",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

print("Chargement du modèle de recherche...")
model = SentenceTransformer('intfloat/multilingual-e5-base')

def search(question, k=10):
    question_vecteur = model.encode("query: " + question)
    vec_str = "[" + ",".join(map(str, question_vecteur)) + "]"

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = """
        SELECT c.article, c.contenu, d.bo, MAX(1 - (c.embedding <=> %s::vector)) AS score
        FROM chunks c
        JOIN documents d ON c.doc_id = d.id
        GROUP BY c.article, c.contenu, d.bo
        ORDER BY score DESC
        LIMIT %s;
    """
    
    cur.execute(query, (vec_str, k))
    resultats = cur.fetchall()
    
    cur.close()
    conn.close()

    articles_trouves = []
    for row in resultats:
        articles_trouves.append({
            "bo": row[2],
            "article": row[0],
            "contenu": row[1],
            "score": round(row[3], 4)
        })
    
    return articles_trouves