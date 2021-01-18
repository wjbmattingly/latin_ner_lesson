import spacy
from spacy.pipeline import EntityRuler
import json
import glob


def load_data(file):
    with open (file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

#Gernating rules
def generate_ruler(patterns, name):
    nlp = spacy.blank("en")
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)
    nlp.to_disk(f"models/{name}_ent_ruler")

def create_training_data(file, type):
    data = load_data(file)
    patterns = []
    for item in data:
        pattern = {
                    "label": type,
                    "pattern": item
                    }
        patterns.append(pattern)
    return (patterns)

def test_ent_ruler(ruler, corpus):
    nlp = spacy.load(ruler)
    with open (corpus, "r", encoding="utf-8") as f:
        corpus = f.read()
    with open ("temp/results.txt", "w", encoding="utf-8") as f:
        doc = nlp(corpus)
        for ent in doc.ents:
            f.write(f"{ent.text}, {ent.label_}\n")

def create_training_set(corpus, ent_ruler_model, output_file, prodigy=False):
    nlp=spacy.load(ent_ruler_model)
    TRAIN_DATA = []
    with open (corpus, "r", encoding="utf-8") as f:
        data = f.read()
        segments = data.split("\n")
        for segment in segments:
            segment = segment.strip()
            doc = nlp(segment)
            entities = []
            for ent in doc.ents:
                if prodigy==True:
                    entities.append({"start":ent.start_char, "end": ent.end_char,  "label": ent.label_, "text": ent.text})
                    pass
                else:
                    entities.append((ent.start_char, ent.end_char, ent.label_))
            if len(entities) > 0:
                if prodigy==True:
                    TRAIN_DATA.append({"text": segment, "spans": entities})
                else:
                    TRAIN_DATA.append([segment, {"entities": entities}])
    print (len(TRAIN_DATA))
    with open (output_file, "w", encoding="utf-8") as f:
        json.dump(TRAIN_DATA, f, indent=4)



person_patterns = create_training_data("data/all_names_declined.json", "PERSON")
groups_patterns = create_training_data("data/groups_declined.json", "GROUP")
places_patterns = create_training_data("data/places_declined.json", "LOCATION")


all_patterns = person_patterns+groups_patterns+places_patterns

generate_ruler(all_patterns, "latin_loc_per_group")
test_ent_ruler("models/latin_loc_per_group_ent_ruler", "data/corpus.txt")

create_training_set("data/corpus.txt", "models/latin_loc_per_group_ent_ruler", "training_data/training_set_prodigy.json", prodigy=True)
