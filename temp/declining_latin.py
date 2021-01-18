import json
import glob


def load_data(file):
    with open (file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

first = ["a", "am", "e", "ae"]
sec = ["us", "um", "e", "i", "o"]
third = ["em", "is", "i", "e"]

first_plurals = ["ae", "as", "arum", "is"]
sec_plurals = ["i", "os", "orum", "is"]
third_plurals = ["es", "ibus", "es"]

def third_rules(name):
    forms = [name]
    if name[-1] == "s":
        new = name[0:-1]+"t"
    elif name[-1] == "o":
        new = name+"n"
    elif name[-2:] == "es":
        new = name[0:-2]
    else:
        new=name
    for form in third:
        forms.append (new+form)
    for form in sec:
        forms.append (new+form)
    return (forms)

def declinsion(name):
    if name[-1] == "a":
        declinsion=1
    elif name[-2:] == "us":
        declinsion=2
    else:
        declinsion=3
    return (declinsion)

def decline_all(file):
    with open (file, "r", encoding="utf-8") as f:
        names = json.load(f)
    all = []
    for word in names:
        forms = []
        dec = declinsion(word)
        if dec == 1:
            for form in first:
                new = word[:-1]+form
                forms.append(new)
        elif dec == 2:
            for form in sec:
                new = word[:-2]+form
                forms.append(new)
        elif dec == 3:
            new = third_rules(word)
            for form in new:
                forms.append(form)
        for form in forms:
            all.append(form)
    return (all)

def decline_plurals(file):
    final = []
    words = load_data(file)
    for word in words:
        if word[-2:] == "ae":
            root = word[:-2]
            for ending in first_plurals:
                final.append (root+ending)
        elif word[-1:] == "i":
            root = word[:-1]
            for ending in sec_plurals:
                final.append (root+ending)
        elif word[-2:] == "es":
            root = word[:-2]
            for ending in third_plurals:
                final.append (root+ending)
        else:
            pass
    return (final)

places = decline_all("data/places.json")
places = list(set(places))
places.sort()
write_data("data/places_declined.json", places)

groups_declined = decline_plurals("data/groups.json")
write_data("data/groups_declined.json", groups_declined)

cognomina = decline_all("data/cognomina.json")
nomina = decline_all("data/nomina.json")
praenomina = decline_all("data/praenomina_nonabs.json")
praenomina_abs = load_data("data/praenomina_abs.json")

all = cognomina+nomina+praenomina+praenomina_abs
all = list(set(all))
all.sort()
write_data("data/all_names_declined.json", all)
