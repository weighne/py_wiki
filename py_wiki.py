import wikipedia
from os import system, name
import pyperclip as pclip


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def wiki_search():
    search_term = input("Enter your search term: ").strip()
    search_results = wikipedia.search(search_term)

    for x in range(len(search_results)):
        print(f"{x} - {search_results[x]}")

    selection = input("\nSelect an article (\'q\' to search again or \'exit\' to exit): ").strip()

    return search_results, selection


if __name__ == '__main__':
    selection = ""
    while selection.lower() != 'exit':
        search_results, selection = wiki_search()
    #   print(search_results, selection)

        if selection.lower() == 'q':
            wiki_search()
        elif selection.lower() == 'exit':
            break
        else:
    #       print(type(selection))
            print()
            summary = wikipedia.summary(search_results[int(selection)])
            print(summary)
            action = input("Press \'C\' to copy summary to clipboard\n Press any other key to continue...")
            if action.lower() == 'c':
                pclip.copy(summary)
            else:
                continue

# print(wikipedia.search(search_term))

