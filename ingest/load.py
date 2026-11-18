import json
import psycopg2
from collections import defaultdict

# Connexion à la base Docker
DB_CONFIG = {
    "dbname": "bo_db",
    "user": "amal",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def main():
    print("Connexion à la base de données...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return

    # 1. Lire tous les articles depuis le fichier JSONL
    print("Lecture de data/chunks.jsonl...")
    articles_par_bo = defaultdict(list)
    with open("data/chunks.jsonl", "r", encoding="utf-8") as f:
        for ligne in f:
            art = json.loads(ligne)
            articles_par_bo[art["bo"]].append(art)

    # 2. Insérer les documents et les articles
    total_inseres = 0
    for bo, articles in articles_par_bo.items():
        print(f"Insertion du BO {bo} ({len(articles)} articles)...")
        
        # On crée d'abord le document (le BO)
        cur.execute(
            "INSERT INTO documents (bo, date_pub) VALUES (%s, %s) RETURNING id;",
            (bo, "2020-01-01") # Date bidon pour l'instant
        )
        doc_id = cur.fetchone()[0]

        # On insère ensuite chaque article lié à ce BO
        for art in articles:
            cur.execute(
                "INSERT INTO chunks (doc_id, article, contenu) VALUES (%s, %s, %s);",
                (doc_id, art["article"], art["contenu"])
            )
            total_inseres += 1

    # On valide la transaction (on sauvegarde tout d'un coup)
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"\n✅ Terminé ! {total_inseres} articles insérés dans PostgreSQL.")

if __name__ == "__main__":
    main()