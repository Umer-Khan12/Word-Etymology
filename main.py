from bs4 import BeautifulSoup, NavigableString
import requests


def between(cur, end):
    """
    Helper function to grab text between two html tags
    """
    while cur and cur != end:
        yield str(cur)
        cur = cur.next_element


html_text = requests.get("https://en.wiktionary.org/wiki/pool").text
soup = BeautifulSoup(html_text, "lxml")

first_section = "English"
next_section = "Dutch"

for section in soup.find_all("span", class_="mw-headline"):
    if section.parent.name == "h2" and section.text == first_section:
        first_section_html = section.parent
for section in soup.find_all("span", class_="mw-headline"):
    if section.parent.name == "h2" and section.text == next_section:
        next_section_html = section.parent

new_html = ""
for c in between(first_section_html.next_sibling, next_section_html):
    new_html += str(c)

new_soup = BeautifulSoup(new_html, "lxml")

for line in new_soup.find_all("span", class_="IPA"):
    print(line)

