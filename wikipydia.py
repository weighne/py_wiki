import requests
import re
import json
import wikitextparser as wtp

base_url = "https://en.wikipedia.org/w/api.php?action=query&titles={}&format=json"
page_url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&page={}&prop=wikitext&formatversion=2"
search_url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrnamespace=0&gsrlimit={}&gsrsearch='{}'"


def wiki_search(term, limit=10):  # take user search term and return list of possible results, then take user input to get specific page
    search_url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrnamespace=0&gsrlimit={}&gsrsearch='{}'"
    page_url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&page={}&prop=wikitext&formatversion=2"
    search = requests.get(search_url.format(int(limit), term))

    y=0
    results = []
    for x in search.json()["query"]["pages"]:  # list results and append to array for selection
        print(f"{y} -", search.json()["query"]["pages"][x]["title"])
        results.append(search.json()["query"]["pages"][x]["title"])
        y+=1

    selection = input("Select result from list: ")

    user_selection = requests.get(page_url.format(results[int(selection)].replace(" ","_")))

    return user_selection


def wiki_plain(page):  # parse wiki_text from page
    parsed_text = wtp.parse(page.json()["parse"]["wikitext"])

    return parsed_text


def get_sections(page):
    print("uhhhhh....")
    # TODO: Gotta look for section headers and then collect all the text between the two section headers.


if __name__ == "__main__":
    search_term = input("Enter your search term: ")

    wiki_page = wiki_search(search_term, 10)
    page_content = wiki_plain(wiki_page)
