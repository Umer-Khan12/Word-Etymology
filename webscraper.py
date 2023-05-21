import httplib2
from bs4 import BeautifulSoup, Comment
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


def get_wiki_pronunciation(url, language):
    """
    Returns the pronunciation section of a given Wiktionary url and language
    :param url: A Wiktionary url
    :param language: Name of a language
    :return: Pronunciation of that language's section on the Wiktionary url if it exists, "Not found." otherwise
    """
    soup = return_section_soup(url, language)
    # If the language doesn't have a section on the Wiktionary page
    if soup is None:
        return "Not found."

    pronunciation_h3 = None
    for section in soup.find_all("span", class_="mw-headline"):
        if section.text == "Pronunciation":
            pronunciation_h3 = section.parent
            break

    # If there's no pronunciation section
    if pronunciation_h3 is None:
        return "Not found."

    # The ul tag for the pronunciation list is 10 siblings over from the h3 tag
    pronunciation_ul_html = pronunciation_h3
    for i in range(10):
        pronunciation_ul_html = pronunciation_ul_html.next_sibling

    for li in pronunciation_ul_html.find_all("li"):
        print(li.text)



def get_wiki_etymology(url, language):
    """
    Returns the etymology section on the Wiktionary url under the given language section
    :param url: A Wiktionary url
    :param language: Name of a language
    :return: Etymology of that language's section on the Wiktionary url if it exists, "Not found." otherwise
    """
    pass


def between(cur, end):
    """
    Helper function to grab text between two html tags
    """
    while cur and cur != end:
        yield str(cur)
        cur = cur.next_element


def return_section_soup(url, language):
    """
    Given a Wiktionary url and a language, returns that language's section's html in Beautiful Soup format
    :param url: A Wiktionary url
    :param language: Name of a language
    :return: Beautiful Soup format html code of that language's section on the url if it exists, None
             if that section doesn't exist on the page.
    """
    sections = languages_on_page(url)

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")

    if language not in sections:
        return None

    # Needs to be handled differently if the input language is the last section on the page
    if sections.index(language) == len(sections) - 1:
        # Every wiktionary page follows its last language section with a cache usage comment
        first_section = language
        cache_comment = soup.find_all(text=lambda text:isinstance(text, Comment))[1]

        # Find the h2 tag that has first_section in its child's span's id
        for section in soup.find_all("span", class_="mw-headline"):
            if section.parent.name == "h2" and section.text == first_section:
                first_section_html = section.parent

        new_html = ""
        for line in between(first_section_html.next_sibling, cache_comment):
            new_html += str(line)

        return BeautifulSoup(new_html, "lxml")
    else:
        # Grab the current language's heading and the heading of the language section after it
        first_section = language
        next_section = sections[sections.index(language) + 1]

        # Find the h2 tags that have first_section and next_section in their child's span's ids
        for section in soup.find_all("span", class_="mw-headline"):
            if section.parent.name == "h2" and section.text == first_section:
                first_section_html = section.parent
        for section in soup.find_all("span", class_="mw-headline"):
            if section.parent.name == "h2" and section.text == next_section:
                next_section_html = section.parent

        new_html = ""
        for line in between(first_section_html.next_sibling, next_section_html):
            new_html += str(line)

        return BeautifulSoup(new_html, "lxml")


get_wiki_pronunciation("https://en.wiktionary.org/wiki/bath", "English")
