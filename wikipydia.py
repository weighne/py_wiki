import requests
import re
import json
import wikitextparser as wtp

base_url = "https://en.wikipedia.org/w/api.php?action=query&titles={}&format=json"
page_url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&page={}&prop=wikitext&formatversion=2"
search_url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrnamespace=0&gsrlimit={}&gsrsearch='{}'"

# https://en.wikipedia.org/w/api.php?action=parse&format=json&page=Pet_door&prop=text&formatversion=2
test_url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&page=Pet_door&prop=wikitext&formatversion=2"

search = input("Whatchu want?\n")

page = requests.get(search_url.format(10, search))  # search for page based on input

with open("wiki_dump.json","w") as out_file:
    json.dump(page.json(), out_file, indent=4)

y=0
results = []
for x in page.json()["query"]["pages"]:  # list results and append to array for selection
    print(f"{y} -", page.json()["query"]["pages"][x]["title"])
    results.append(page.json()["query"]["pages"][x]["title"])
    y+=1

user_choice = input("Whitchu want?\n")

print(results[int(user_choice)])

page2 = requests.get(page_url.format(results[int(user_choice)].replace(" ","_")))  # get specific page
# page2 = requests.get(test_url)
print(type(page2))
# print(page.json())
with open("text_dump.json","w") as out_file2:
    json.dump(page2.json(), out_file2, indent=4)

parsed_text = wtp.parse(page2.json()["parse"]["wikitext"])  # parse wikitext so that it's actually readable
print(parsed_text)

with open("page_dump.txt","w") as out_file:
    out_file.write(str(parsed_text))
