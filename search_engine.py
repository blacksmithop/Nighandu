from dictionary_lookup.helper.loaddata import Data
from dictionary_lookup.helper.index import Index
from sys import exit


df = Data().load()

index = Index()

index.index_document(df=df)

while True:
    try:
        search_term = input(">>")

        if search_term == "":
            continue
        print(index.search(search_term))

    except (KeyboardInterrupt, EOFError):
        exit(0)