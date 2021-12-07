import wikipedia


def wiki_search():
    search_term = input("Enter your search term: ").strip()
    search_results = wikipedia.search(search_term)

    for x in range(len(search_results)):
        print(f"{x} - {search_results[x]}")

    selection = input("\nSelect an article (\'q\' to search again): ").strip()

    return search_results, selection


if __name__ == '__main__':
    search_results, selection = wiki_search()
#    print(search_results, selection)

    if selection == 'q' or selection == 'Q':
        wiki_search()
    else:
#        print(type(selection))
        print()
        print(wikipedia.summary(search_results[int(selection)]))

# print(wikipedia.search(search_term))

