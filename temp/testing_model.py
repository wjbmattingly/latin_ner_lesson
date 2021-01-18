import spacy

def test_model(model, corpus):
    nlp = spacy.load(model)
    with open (corpus, "r", encoding="utf-8") as f:
        corpus = f.read()
    with open ("temp/ml_results.txt", "w", encoding="utf-8") as f:
        doc = nlp(corpus)
        for ent in doc.ents:
            f.write(f"{ent.text}, {ent.label_}\n")

test_model(r"models/latin_test", "data/berengar.txt")
