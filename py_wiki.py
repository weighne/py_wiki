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


def get_links(page):
    links = page.links
    formatted_links = [x.replace(' ','_').replace('\'','%27') for x in links]
    print("Page Links:\n")
    for x in range(len(formatted_links)):
        print(f"{x} - {formatted_links[x]}")
    print()
    #TODO: only spit out x number of links at a time and allow user to scroll through them manually
    nav = input("If you would link to visit a link, enter the corresponding number\nOtherwise, press \'q\' to exit...")
    if nav.lower() == 'q':
        print("bye")
    else:
        print(f"https://wikipedia.org/wiki/{formatted_links[int(nav)]}")


if __name__ == '__main__':
    selection = ""
    while selection.lower() != 'exit':
#        clear()
        search_results, selection = wiki_search()
    #   print(search_results, selection)

        if selection.lower() == 'q':
            wiki_search()
        elif selection.lower() == 'exit':
            break
        else:
#            clear()
    #       print(type(selection))
            print()
            wiki_page = wikipedia.page(search_results[int(selection)])
            print(wiki_page.title)

            summary = wikipedia.summary(search_results[int(selection)])
            print()
            print(summary)
            action = input("\nPress \'C\' to copy summary to clipboard\nPress \'L\' to view links\nPress any other key to continue...")
            if action.lower() == 'c':
                pclip.copy(summary)
            elif action.lower() == 'l':
                get_links(wiki_page)
            else:
                continue

# print(wikipedia.search(search_term))

