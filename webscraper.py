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
        language_headers = languages_on_page(url)
        if language not in language_headers:
            return url + " (No section for " + language + ")"
        else:
            return url

    return "No Wiktionary page found."


def languages_on_page(url):
    """
    Returns a list of the language sections present on a Wiktionary page
    :param url: A Wiktionary url
    :return: A list of strings containing the names of languages that have sections on the Wiktionary page
    """
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")
    language_headers = []
    for section in soup.find_all("span", class_="mw-headline"):
        if section.parent.name == "h2":
            language_headers.append(section.text)
    return language_headers


def is_red_link(url):
    """
    Some wiktionary links don't have filled entries, this checks if there is an entry
    :param url: A Wiktionary url
    :return: True if there is no entry on the page, False otherwise
    """
    if url[-9:] == "redlink=1":
        return True
    else:
        return False


def get_wiki_ipa(url, language):
    """
    Returns the IPA pronunciation(s) of a given Wiktionary url and language
    :param url: A Wiktionary url
    :param language: Name of a language
    :return: IPA of that language's section on the Wiktionary url if it exists, "Not found." otherwise
    """
    pass

