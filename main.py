from bs4 import BeautifulSoup, NavigableString, Comment
import requests


def between(cur, end):
    """
    Helper function to grab text between two html tags
    """
    while cur and cur != end:
        yield str(cur)
        cur = cur.next_element


html_text = requests.get("https://en.wiktionary.org/wiki/%D7%91%D7%AA#Hebrew").text
soup = BeautifulSoup(html_text, "lxml")

for section in soup.find_all("span", class_="mw-headline"):
    if section.parent.name == "h2" and section.text == "Hebrew":
        first_section_html = section.parent

new_html = ""

next_section_html = soup.find_all(text=lambda text:isinstance(text, Comment))[1]

for line in between(first_section_html.next_sibling, next_section_html):
    new_html += str(line)
