import psycopg2
from sentence_transformers import SentenceTransformer
import time

DB_CONFIG = {
    "dbname": "bo_db",
    "user": "amal",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

# On charge le modèle d'IA (la première fois, ça le télécharge)
print("Chargement du modèle d'IA (patientez...)")
model = SentenceTransformer('intfloat/multilingual-e5-base')

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # On récupère les articles qui n'ont pas encore d'embedding
    print("Recherche des articles à traiter...")
    cur.execute("SELECT id, contenu FROM chunks WHERE embedding IS NULL;")
    articles = cur.fetchall()
    
    total = len(articles)
    print(f"Il y a {total} articles à transformer en vecteurs.")

    if total == 0:
        print("Tous les articles ont déjà des vecteurs !")
        return

    # On traite par lots de 32 pour ne pas saturer la mémoire
    batch_size = 32
    start_time = time.time()

    for i in range(0, total, batch_size):
        batch = articles[i:i+batch_size]
        ids = [row[0] for row in batch]
        
        # IMPORTANT : Le modèle e5 exige le préfixe "passage: " pour les textes
        textes = ["passage: " + row[1] for row in batch]

        # L'IA calcule les vecteurs
        vecteurs = model.encode(textes)
        
        # On enregistre dans PostgreSQL
        for j, art_id in enumerate(ids):
            # On convertit le vecteur en format lisible par pgvector
            vec_str = "[" + ",".join(map(str, vecteurs[j])) + "]"
            cur.execute(
                "UPDATE chunks SET embedding = %s WHERE id = %s;",
                (vec_str, art_id)
            )
        
        conn.commit()
        progress = min(i + batch_size, total)
        print(f"Traitement : {progress}/{total} articles transformés...")

    end_time = time.time()
    print(f"\n✅ Terminé en {int(end_time - start_time)} secondes !")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()