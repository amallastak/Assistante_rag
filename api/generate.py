import os
from google import genai
from api.search import search

# ⚠️ COLLE TA CLÉ GEMINI ICI ENTRE LES GUILLEMETS (ne la partage pas sur internet !)
API_KEY = ""

def generer_reponse(question):
    print(f"1. Recherche des articles pour : '{question}'...")
    articles = search(question, k=10)
    
    if not articles:
        return "Je ne trouve pas la réponse dans les textes indexés."

    contexte = ""
    for i, art in enumerate(articles, 1):
        contexte += f"--- Extrait {i} (BO n°{art['bo']} - {art['article']}) ---\n"
        contexte += f"{art['contenu']}\n\n"

    prompt = f"""Tu es un assistant juridique spécialisé dans le droit marocain.
Réponds à la question de l'utilisateur en te basant UNIQUEMENT sur les extraits fournis ci-dessous.
Si les extraits ne contiennent pas la réponse, réponds exactement : "Je ne trouve pas la réponse dans les textes indexés."
Cite tes sources sous la forme [BO n°X, Article Y].

Extraits :
{contexte}

Question : {question}
Réponse :"""

    print("2. Génération de la réponse par Gemini...")
    
    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        
        print("\n--- SOURCES TROUVÉES ---")
        for art in articles:
            print(f"- BO n°{art['bo']}, {art['article']} (Score: {art['score']})")
            
        return response.text
        
    except Exception as e:
        return f"Erreur avec Gemini : {e}"

if __name__ == "__main__":
    ma_question = "ما هي الرسوم الجمركية المطبقة على استيراد القمح اللين ومشتقاته؟"
    reponse = generer_reponse(ma_question)
    print("\n=== RÉPONSE DE L'ASSISTANT ===")
    print(reponse)