import requests

URL_ANTONYMS = "https://antonymonline.ru/antonyms.json?word="
URL_SYNONYMS = "https://synonymonline.ru/assets/json/synonyms.json"
filename = "templates.cfg"
templates = {}

def read_template(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return generate_template(f.readlines())


def write_to_template(filename, key, value):
    global templates
    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n"+key + "," + value)
    templates = read_template(filename)


def generate_template(lines):
    dict = {}
    for line in lines:
        stripped = line.strip()
        if "," not in line: continue
        key_value_pair = stripped.split(",")
        key = key_value_pair[0].strip()
        value = key_value_pair[1].strip()
        dict[key] = value
        dict[value] = key

    return dict


templates = read_template(filename)


def get_antonym_for_word(word):
    if word in templates.keys():
        return templates[word]
    return requests.get(URL_ANTONYMS + word).json()["antonyms"]


def get_synonym_for_word(word):
    payload = {"word": word}
    return requests.post(URL_SYNONYMS, data=payload).json()["synonyms"]


def demotivate_sentence(words):
    negative = []
    for word in words:
        try:
            negative.append(try_find_antonyms_and_synonyms(word))
        except Exception as e:
            raise Exception("Unable to find antonyms or synonyms for " + word)
    return " ".join(negative)


def try_find_antonyms_and_synonyms(word):
    try:
        return get_antonym_for_word(word)[0]
    except Exception as e:
        print("Trying to find synonym for " + word)
        return get_synonym_for_word(word)[0]
