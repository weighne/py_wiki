import wikipedia
from os import system, name
import pyperclip as pclip


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def wiki_search():
    selection = ""
    while selection.lower() != 'q':
        search_term = input("Enter your search term: ").strip()
        search_results = wikipedia.search(search_term)

        for x in range(len(search_results)):
            print(f"{x} - {search_results[x]}")

        selection = input("\nSelect an article (\'q\' to search again or \'exit\' to exit): ").strip()

        if selection.lower() == 'q':
            clear()
            continue
        elif selection.lower() == 'exit':
            clear()
            break
        else:
            clear()
            wiki_page = wikipedia.page(search_results[int(selection)])
            print(wiki_page.title)
            for x in range(len(wiki_page.sections)):
                print(f"{x} - {wiki_page.sections[x]}")

            print("What section of the page would you like to view?\nEnter \'S\' for summary\n")
            section_choice = input("Input: ")

            if section_choice.lower() == 's':
                wiki_output = wikipedia.summary(search_results[int(selection)])
                print(wiki_output)
            else:
                try:
                    wiki_output = wiki_page.section(wiki_page.sections[int(section_choice)].replace(" ","_"))
                    print(wiki_output)
                except:
                    print("Something went way wrong!\n")

            #print(summary)
            action = input("\nPress \'C\' to copy to clipboard\nPress \'L\' to view links\nPress any other key to continue...\nInput: ")

            if action.lower() == 'c':
                pclip.copy(wiki_output)
            elif action.lower() == 'l':
                get_links(wiki_page)
            else:
                continue

        return search_results, selection


def get_links(page):
    links = page.links
    formatted_links = [x.replace(' ','_').replace('\'','%27') for x in links]
    print("Page Links:\n")
    for x in range(len(formatted_links)):
        if x%10 != 0 or x == 0:
            print(f"{x} - {formatted_links[x]}")
        elif x%10 == 0 and x != 0:
            print(f"{x} - {formatted_links[x]}")
            cont = input("\nPress \'q\' to stop...\nPress any other key to continue...\n")
            if cont.lower() == 'q':
                break
            else:
                continue
        else:
            print(x)

    print()
    #TODO: only spit out x number of links at a time and allow user to scroll through them manually
    nav = input("If you would link to visit a link, enter the corresponding number\nOtherwise, press \'q\' to exit...\nInput: ")
    if nav.lower() == 'q':
        print("bye")
    else:
        print(f"https://wikipedia.org/wiki/{formatted_links[int(nav)]}")


if __name__ == '__main__':
    while True:
        print("Welcome to py_wiki!\nChoose from one of the functions below...\n")
        print("0 - Search\n1 - Visit Link\n2 - Exit")
        function = input("Input: ")
        if function == 0:  # search
            clear()
            wiki_search()
        elif function == 1:  # link
            clear()
            print("This function hasn\'t been built yet, Chris is very hopeful for what it might do in the future...")
        elif function == 2:
            print("Goodbye!")
            break

        search_results, selection = wiki_search()
    #   print(search_results, selection)



# print(wikipedia.search(search_term))
