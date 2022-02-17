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

    # selection = input("Select result from list: ")
    selection = 9  # testing

    current_page = results[int(selection)].replace(" ","_")

    # user_selection = requests.get(page_url.format(current_page))

    return current_page


def wiki_plain(page):  # parse wiki_text from page
    parsed_text = wtp.parse(page.json()["parse"]["wikitext"])

    return parsed_text


def get_sections(page):
    print(page)
    section_url = "https://en.wikipedia.org/w/api.php?action=parse&page={}&prop=sections&format=json"
    print(section_url.format(page))
    sections = requests.get(section_url.format(page))

    with open("wiki_sections.json","w") as out_file:
        json.dump(sections.json(), out_file, indent=4)

    return sections


if __name__ == "__main__":
    # search_term = input("Enter your search term: ")
    search_term = "Spanish Inquisition"  # testing

    page_title = wiki_search(search_term, 10)
    print(page_title)
    wiki_page = requests.get(page_url.format(page_title))
    print(wiki_page)
    page_content = wiki_plain(wiki_page)
    print(page_content)
    wiki_sections = get_sections(page_title)
    print(wiki_sections.json())

    for x in wiki_sections.json()["parse"]["sections"]:
        print(x["anchor"])
