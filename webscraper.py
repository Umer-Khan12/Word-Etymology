import httplib2
from bs4 import BeautifulSoup, Comment
import requests
import io


def get_wiki_url(word, language):
    """
    word and language are both string inputs
    :return: url (string) that links to the word in that language on wiktionary. If a page of that word
             exists then it returns a list [url, True/False] where the 2nd element is True if that word has
             a section in the input language. If a page with that word doesn't exist then it returns None.
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
            return [url, False]
        else:
            return [url, True]

    return None


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

    # Need to reformat the pronunciations so that the same ones arent repeated and there's one on each line
    pronunciations_unformatted = ""
    for li in pronunciation_ul_html.find_all("li"):
        pronunciations_unformatted += li.text + "\n"

    pronunciations_unformatted.rstrip()
    pronunciations_unrepeated = []
    for line in io.StringIO(pronunciations_unformatted):
        if line.rstrip() not in pronunciations_unrepeated:
            pronunciations_unrepeated.append(line.rstrip())

    # Remove some other repeated IPAs and irrelevant information
    pronunciations_formatted = []
    for line in pronunciations_unrepeated:
        if line[2:4] == "PR" and "IPA" not in line:
            continue
        elif line[0:5] == "Audio" and "IPA" not in line:
            continue
        elif line[0:6] == "Rhymes" and "IPA" not in line:
            continue
        elif line[0:9] == "Homophone" and "IPA" not in line:
            continue
        elif line[0:15] == "Syllabification" and "IPA" not in line:
            continue
        else:
            pronunciations_formatted.append(line.replace("(key)", ""))

    return "".join([x + "\n" for x in pronunciations_formatted]).rstrip()


def get_wiki_etymology(url, language):
    """
    Returns the etymology section on the Wiktionary url under the given language section
    :param url: A Wiktionary url
    :param language: Name of a language
    :return: Etymology of that language's section on the Wiktionary url if it exists, "Not found." otherwise
    """
    soup = return_section_soup(url, language)
    # If the language doesn't have a section on the Wiktionary page
    if soup is None:
        return "Not found."

    etymology_h3 = None
    for section in soup.find_all("span", class_="mw-headline"):
        if section.text == "Etymology" or section.text == "Etymology 1":
            etymology_h3 = section.parent
            break

    # If there's no etymology section
    if etymology_h3 is None:
        return "Not found."

    # The p tag for the etymology is 10 siblings over from the h3 tag
    etymology_p_html = etymology_h3
    for i in range(10):
        etymology_p_html = etymology_p_html.next_sibling

    return etymology_p_html.get_text().rstrip()


def get_wiki_definition(url, language):
    """
    Returns the definition entry of the Wiktionary url under the given language section
    :param url: A Wiktionary url
    :param language: Name of a language
    :return: Definition entry of that language's section on the Wiktionary url if it exists, "Not found." otherwise
    """
    soup = return_section_soup(url, language)
    # If the language doesn't have a section on the Wiktionary page
    if soup is None:
        return "Not found."

    # A list of possible id's that the input word's html tag could have
    possible_ids = ["Noun", "Verb", "Adjective", "Determiner", "Pronoun", "Conjunction", "Suffix", "Prefix", "Adverb",
                    "Numeral"]

    definition_tag = None
    for section in soup.find_all("span", class_="mw-headline"):
        if section.text in possible_ids:
            definition_tag = section.parent
            break

    # If there's no definition section
    if definition_tag is None:
        return "Not found."

    # Get the <p> text following the definition header
    definition_html = definition_tag
    for i in range(10):
        definition_html = definition_html.next_sibling

    output_text = ""
    output_text += definition_html.get_text().rstrip()

    # Get the <ol> text following the <p> tag
    while str(definition_html)[0:4] != "<ol>":
        definition_html = definition_html.next_sibling

    # Get the list entries
    definitions_unformatted = ""
    cur_num = 1
    for li in definition_html.find_all("li"):
        if li.parent.name == "ol":
            # Don't include the sentence examples or quotations or citations
            li_formatted = remove_inner_tags("<dl>", "</dl>", li)
            li_formatted = remove_inner_tags("<dd>", "</dd>", li_formatted)
            li_formatted = remove_inner_tags("<div class=\"citation-whole\">", "</div>", li_formatted)
            li_formatted = remove_inner_tags("<span class=\"cited-source\">", "</span>", li_formatted)
            li_formatted = remove_inner_tags("<ul style=\"display: block;\">", "</ul>", li_formatted)
            definitions_unformatted += str(cur_num) + ". " + remove_everything_after_period(li_formatted.text.rstrip()) + "\n"
            cur_num += 1

    definitions_unformatted.rstrip()
    definitions_unrepeated = []
    for line in io.StringIO(definitions_unformatted):
        if line.rstrip() not in definitions_unrepeated:
            definitions_unrepeated.append(line.rstrip())

    return output_text + "\n" + "".join(["    " + x + "\n" for x in definitions_unrepeated]).rstrip()


def between(cur, end):
    """
    Helper function to grab text between two html tags
    """
    while cur and cur != end:
        yield str(cur)
        cur = cur.next_element


def remove_inner_tags(tag_open, tag_close, html):
    """
    Helper function to remove tags (<foo>...</foo>) and their content from inner text of html.
    :param tag_close: closing form of the tag to be removed (a string written as </a>)
    :param html: The html that needs to be modified
    :param tag_open: opening form of the tag to be removed (a string written as <a>)
    :return: html without the tag and its contents
    """
    html_str = str(html).replace("\n", " ")
    new_html = ""

    # Loop over each letter in the string
    tag_encountered = False
    tag_deletion_length = 0
    cur_index = 0
    for letter in html_str:
        # Used to not include the closing part of the tag
        if tag_deletion_length != 0:
            tag_deletion_length -= 1
            cur_index += 1
            continue

        if letter == "<" and not tag_encountered:
            cur_tag = ""
            # Keep going until we figure out what the tag is
            for i in html_str[cur_index:]:
                if i != ">":
                    cur_tag += i
                elif i == ">":
                    cur_tag += i
                    break
            if cur_tag == tag_open:
                tag_encountered = True

        if letter == "<" and tag_encountered:
            # Need to check if its the closing tag
            cur_tag = ""
            for i in html_str[cur_index:]:
                if i != ">":
                    cur_tag += i
                elif i == ">":
                    cur_tag += i
                    break
            if cur_tag == tag_close:
                # If its the closing tag then we count how many more letters we need to skip to not include it
                tag_encountered = False
                tag_deletion_length = len(tag_close) - 1
                cur_index += 1
                continue

        # Add to the new_html string if we aren't at the tag yet or aren't deleting the rest of the tag
        if not tag_encountered:
            new_html += letter
        cur_index += 1

    return BeautifulSoup(new_html, "lxml")


def remove_everything_after_period(s):
    new_s = ""
    for i in s:
        new_s += i
        if i == ".":
            return new_s
    return new_s


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



print(get_wiki_pronunciation("https://en.wiktionary.org/wiki/name#English", "English"))
