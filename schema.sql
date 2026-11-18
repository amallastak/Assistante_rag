-- Active l'extension pour les vecteurs (déjà fait, mais on s'assure)
CREATE EXTENSION IF NOT EXISTS vector;

-- Table pour stocker les métadonnées des Bulletins Officiels
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    bo TEXT,
    date_pub DATE
);

-- Table pour stocker les articles (chunks)
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    doc_id INT REFERENCES documents(id),
    article TEXT,
    contenu TEXT,
    -- Recherche par mots-clés (pour plus tard)
    tsv TSVECTOR GENERATED ALWAYS AS (to_tsvector('french', contenu)) STORED,
    -- Emplacements pour les vecteurs (768 dimensions pour notre modèle)
    embedding VECTOR(768)
);

-- Crée un index pour accélérer la recherche par mots-clés
CREATE INDEX ON chunks USING gin(tsv);

-- Crée un index pour accélérer la recherche par sens (vecteurs)
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);