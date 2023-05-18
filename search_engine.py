from dictionary_lookup.helper.loaddata import Data
from dictionary_lookup.helper.index import Engine
from sys import exit


index = Engine()

while True:
    try:
        search_term = input(">>")

        if search_term == "":
            continue
        print(index.search(search_term))

    except (KeyboardInterrupt, EOFError):
        exit(0)