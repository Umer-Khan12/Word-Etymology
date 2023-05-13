import httplib2
from bs4 import BeautifulSoup
import requests


def get_wiki_url(word, language):
    """
    word and language are both string inputs
    :return: url (string) that links to the word in that language on wiktionary, "N/A" if page doesn't exist
    """

    # Replace spaces with underscores for words and languages that have them
    language_url = language.replace(" ", "_")
    word = word.replace(" ", "_")

    # Wiktionary url formats differ on if the word is a reconstruction or not
    # Reconstructed words start with '*' or belong to a 'Proto' language
    if word[0] == "*":
        url = "https://en.wiktionary.org/wiki/Reconstruction:" + language_url + "/" + word[1:]
    elif language[0:6] == "Proto-":
        url = "https://en.wiktionary.org/wiki/Reconstruction:" + language_url + "/" + word
    else:
        url = "https://en.wiktionary.org/wiki/" + word + "#" + language_url

    # Make sure the page exists
    h = httplib2.Http()
    resp = h.request(url, "HEAD")
    page_exists = False
    if int(resp[0]['status']) < 400:
        page_exists = True

    if page_exists:
        # It's possible that a wiktionary page exists but there's no section for the input language
        # So we should check the page first to make sure a section with that language exists
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, "lxml")
        language_headers = []
        for section in soup.find_all("span", class_="mw-headline"):
            if section.parent.name == "h2":
                language_headers.append(section.text)

        if language not in language_headers:
            return url + " (No section for " + language + ")"
        else:
            return url

    return "No Wiktionary page found."
