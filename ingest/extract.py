import fitz  # PyMuPDF
import os
import json
import re

RAW_DIR = "data/raw"
OUTPUT = "data/chunks.jsonl"

# Motif pour trouver les articles : "ARTICLE PREMIER", "ART. 12", "Article 3"
PATTERN_ARTICLE = re.compile(
    r"(ARTICLE\s+PREMIER|ART\.\s*\d+|Article\s+\d+)",
    re.IGNORECASE
)

def lire_pdf(chemin):
    doc = fitz.open(chemin)
    texte = ""
    for page in doc:
        texte += page.get_text()
    doc.close()
    return texte

def nettoyer(texte):
    lignes = texte.split("\n")
    lignes_propres = [l for l in lignes if len(l.strip()) > 3]
    return "\n".join(lignes_propres)

def decouper_par_article(texte, bo):
    positions = [(m.start(), m.group()) for m in PATTERN_ARTICLE.finditer(texte)]
    articles = []
    for i, (pos, titre) in enumerate(positions):
        fin = positions[i + 1][0] if i + 1 < len(positions) else len(texte)
        contenu = texte[pos:fin].strip()
        if len(contenu) > 50:  # Ignore les faux positifs trop courts
            articles.append({
                "bo": bo,
                "article": titre.strip(),
                "contenu": contenu
            })
    return articles

def main():
    # On prend TOUS les PDF du dossier data/raw
    fichiers = [f for f in os.listdir(RAW_DIR) if f.endswith(".pdf")]
    
    with open(OUTPUT, "w", encoding="utf-8") as out:
        total = 0
        for fichier in fichiers:
            chemin = os.path.join(RAW_DIR, fichier)
            # On extrait le numéro du BO depuis le nom (ex: BO_6818_Fr.pdf -> 6818)
            bo = fichier.split("_")[1] if "_" in fichier else "Inconnu"
            
            print(f"Traitement de {fichier}...")
            try:
                texte = nettoyer(lire_pdf(chemin))
                articles = decouper_par_article(texte, bo)
                print(f"   -> {len(articles)} articles trouvés.")
                for art in articles:
                    out.write(json.dumps(art, ensure_ascii=False) + "\n")
                total += len(articles)
            except Exception as e:
                print(f"   ❌ Erreur avec {fichier} : {e}")

        print(f"\n✅ Terminé ! Total : {total} articles écrits dans {OUTPUT}")

if __name__ == "__main__":
    main()