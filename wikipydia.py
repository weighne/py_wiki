import requests
import re
import json

base_url = "https://en.wikipedia.org/w/api.php?action=query&titles={}"
search_url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrnamespace=0&gsrlimit={}&gsrsearch='{}'"

search = input("Whatchu want?\n")

page = requests.get(search_url.format(10, search))

with open("wiki_dump.json","w") as out_file:
    json.dump(page.json(), out_file, indent=4)

for x in page.json()["query"]["pages"]:
    print(page.json()["query"]["pages"][x]["title"])

user_choice = input("Whatchu want?")
