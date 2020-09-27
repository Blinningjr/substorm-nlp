import sys
from nlp import demo


def commands(arr):
    if arr[0] == "input" or arr[0] == "i":
        # TODO: send arr[1] to automation
        demo.nlp(' '.join(arr[1:]))
        arr.clear()

    elif arr[0] == "exit" or arr[0] == "e":
        sys.exit()

    elif arr[0] == "help" or arr[0] == "h":
        prompt()
    else:
        print(f"{arr[0]} is not a command, see help or h for help")


def prompt():
    f = open("helpPrompt.txt", "r")
    print(f.read())
