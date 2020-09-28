import sys
import spacy
from lib import Error
from lib.automate import Automate
from lib.settings import SETTINGS


# Requirments:
# pip3 install spacy
# python -m spacy download en_core_web_sm
#
# Examples:
# Email: "Send email I am sick today. to niklas"
# Alarm: "Set alarm at 14:30 today"a
# Meeting: "Book meeting with Niklas for tomorow at 8:00 a clock"
def demo():
    while True:
        txt = sys.stdin.readline().strip()

        if len(txt) == 0:
            continue
        else:
            nlp(txt)
            break


def nlp(input):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(input)
    print("\n")
    print_tokens(doc)
    print("\n")
    run_demo(doc)


def print_tokens(doc):
    for t in doc:
        print(t.text, t.pos_)

    print("\n")

    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)


def tokens_to_string(tokens):
    text = list()
    for t in tokens:
        text.append(t.text)
    return " ".join(text)


# Get name
def get_name(tokens):
    rest = tokens.copy()
    for i in range(len(tokens)-1):
        if tokens[i].pos_ == "ADP" and tokens[i+1].pos_ == "PROPN":
            name = tokens[i+1]
            rest.remove(tokens[i])
            rest.remove(tokens[i+1])
            return (name, rest)

    return (None, None)


# Get Action
def get_action(tokens):
    rest = tokens.copy()
    for i in range(len(tokens)-1):
        if (tokens[i].pos_ == "VERB" or tokens[i].pos_ == "PROPN" or
                tokens[i].pos_ == "NOUN") and tokens[i+1].pos_ == "NOUN":
            action = tokens[i+1]
            rest.remove(tokens[i])
            rest.remove(tokens[i+1])
            return (action, rest)

    return (None, None)


# Get time
def get_time(doc):
    for ent in doc.ents:
        if ent.label_ == "TIME" or ent.label_ == "DATE":
            return ent

    return None


def run_demo(doc):
    email_contacts = {
        "viktor": "vikfro-6@student.ltu.se",
        "gustav": "gushan-6@student.ltu.se",
        "mark": "marhak-6@student.ltu.se",
        "niklas": "inaule-6@student.ltu.se",
        "alexander": "aleman-6@student.ltu.se",
        "hugo": "hugwan-6@student.ltu.se",
        "aron": "arowid-6@student.ltu.se",
    }
    tokens = list()
    for t in doc:
        tokens.append(t)
    (action, rest) = get_action(tokens)

    if action is None:
        print("Error")
        return
    else:
        if action.lemma_ == "email":
            (name, rest) = get_name(rest)
            if name is None:
                print("Error")
                return
            contact = email_contacts.get(name.text.lower())
            automate = Automate()
            try:
                response = automate.run(
                    "skicka",
                    [contact],
                    None,
                    tokens_to_string(rest),
                    "John Doe",
                )
                print(response)
            except Error as err:
                print(err)

        elif action.lemma_ == "alarm":
            time = get_time(doc)
            if time is None:
                print("Error")
                return
            print("Alarm")
            print("Alarm set at time \"{}\".".format(time))
        elif action.lemma_ == "meeting":
            (name, rest) = get_name(rest)
            if name is None:
                print("Error")
                return
            time = get_time(doc)
            if time is None:
                print("Error")
                return
            print("Meeting")
            print("Meeting set with \"{0}\" at time \"{1}\".".format(name.text,
                                                                     time))


if __name__ == '__main__':
    demo()
