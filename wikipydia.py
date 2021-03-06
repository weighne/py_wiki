import requests
import re
import json
import wikitextparser as wtp
import random

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
    # selection = random.randint(1,9)  # testing

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


def sections_choice(sections,z):
    '''
    Sections are indexed in order of appearance on the page, so we list the section titles, but just use the user's input (1, 2, 3, etc.) to call the specific section
    This feels very silly, but seems to work pretty well... so I'm gonna leave it alone.
    '''
    section_url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&page={}&prop=wikitext&formatversion=2&section={}"
    y = 1
    for x in sections.json()["parse"]["sections"]:
        print(f"{y} -", x["anchor"])
        y+=1

    # user_choice = input("Select section from list: ")
    # user_choice = random.randint(1,len(sections.json()["parse"]["sections"]))  # testing
    user_choice = 30

    formatted_url = section_url.format(sections.json()["parse"]["title"].replace(" ","_"),user_choice)
    section_get = requests.get(formatted_url)
    # with open(f"section_dump-{z}.json","w") as out_file:
    #     json.dump(section_get.json(), out_file, indent=4)
    # print(formatted_url)
    return section_get.json()

# eveything between <> regex: (?<=<).*(?=>)
# This just grabs one: <(.*)\/>
# grabs <ref name = > garbage: <(ref.*?)>
def parse_text(section):
    special_chars = ['\n','<ref>','</ref>','{{','}}','[[',']]','','','','']
    ref_string = "<ref>(.*?)</ref>"  # regex for reference string
    # TODO: use regex to find unwanted ref strings and remove them from the plain text
    # TODO: use regex to find special strings [[]] / {{}} and then handle them accordingly
    plain_text = []
    skip=0

    garbage_text = re.split('([^a-zA-Z0-9\s])', section)
    #clean up the easy stuff in the garbage text (null characters and trailing whitespace)
    garbage_text = [x for x in garbage_text if x.strip()]

    less_garbage_text = []  # array for the good stuff
    prev_char = ''  # variable for tracking what we're working with
    for x in range(len(garbage_text)):
        # print(prev_char)
        if x == 0:  # not much to compare the first character against, so we make note of it, and move on
            prev_char = garbage_text[x]
            less_garbage_text.append(garbage_text[x])
            continue
        else:
            prev_char = garbage_text[x-1]  # now we have a real previous character to work with

            if garbage_text[x] == prev_char:  # if the current and previous character match...
                curr_char = garbage_text[x]
                if len(less_garbage_text) >= 1:
                    less_garbage_text.pop(len(less_garbage_text)-1)  # remove any garbage from the clean array

                less_garbage_text.append(f"{prev_char}{curr_char}")  # append nice combined string to new array
            else:  # if there is no match...
                less_garbage_text.append(garbage_text[x])  # dump the current character into the new array
                continue  # keep moving

    print("This is supposed to be garbage")
    print()
    print(garbage_text)
    print()
    print()
    print("This is supposed to be less garbage")
    print()
    print(less_garbage_text)
    print()
    print()
    with open("less_garbage.txt","w") as outfile:
        for x in less_garbage_text:
            outfile.write(x)

    x = 0
    skip=0
    temp=[]
    # slightly_less_garbage_text =[]
    regex_pattern = r'<ref(\S*?)[^>]*>.*?</\1ref>|<.*?/>'
    slightly_less_garbage_text = re.sub(regex_pattern, '', ''.join(less_garbage_text), count=0)

    # This shit down here vvv does that ^^^ but waaaaaay worse... I'm holding on to it to remind myself that I should be using regex more

    # while x <= len(less_garbage_text):
    #     try:
    #         print(x)
    #         if "{{" in less_garbage_text[x]:
    #             skip=1
    #             while skip==1:
    #                 if "}}" in less_garbage_text[x]:
    #                     temp.append(less_garbage_text[x])
    #                     #less_garbage_text.pop(x)
    #                     x+=1
    #                     skip=0
    #                 else:
    #                     temp.append(less_garbage_text[x])
    #                     #less_garbage_text.pop(x)
    #                     x+=1
    #             # Do some stuff...
    #         elif "ref" in less_garbage_text[x] and less_garbage_text[x+1] == ">":
    #             slightly_less_garbage_text.pop(x-1)
    #             skip=1
    #             while skip==1:
    #                 if "ref" in less_garbage_text[x] and less_garbage_text[x-1] == "/":
    #                     temp.append(less_garbage_text[x])
    #                     temp.append(less_garbage_text[x+1])
    #                     #less_garbage_text.pop(x)
    #                     x+=2
    #                     skip=0
    #                 else:
    #                     temp.append(less_garbage_text[x])
    #                     #less_garbage_text.pop(x)
    #                     x+=1
    #         elif "ref name" in less_garbage_text[x] and less_garbage_text[x-1] == "<":
    #             skip=1
    #             while skip==1:
    #                 if less_garbage_text[x] == ">":
    #                     temp.append(less_garbage_text[x])
    #                     #less_garbage_text.pop(x)
    #                     x+=1
    #                     skip=0
    #                 else:
    #                     temp.append(less_garbage_text[x])
    #                     #less_garbage_text.pop(x)
    #                     x+=1
    #
    #         else:
    #             slightly_less_garbage_text.append(less_garbage_text[x])
    #             x+=1
    #     except IndexError:
    #         break
    # print(temp)
    print(''.join(less_garbage_text))
    print()
    print(''.join(slightly_less_garbage_text))



    for x in re.split('([^a-zA-Z0-9\s])', section):
        if x in special_chars:
            if x == "<ref>":
                skip=1
            elif x == "</ref>":
                skip=0
            elif x == "{{convert":
                print("do math")
            else:
                continue
        elif x not in special_chars and skip != 1:
            plain_text.append(x)
    # print(plain_text)


if __name__ == "__main__":
    # search_term = input("Enter your search term: ")
    z=0
    while z!=1:
        search_term = "Bees"  # testing

        page_title = wiki_search(search_term, 10)
        # print(page_title)
        wiki_page = requests.get(page_url.format(page_title))
        # print(wiki_page)
        page_content = wiki_plain(wiki_page)
        # print(page_content)
        wiki_sections = get_sections(page_title)
        # print(wiki_sections.json())
        print(sections_choice(wiki_sections,z))
        parse_text(sections_choice(wiki_sections,z)["parse"]["wikitext"])
        z+=1
