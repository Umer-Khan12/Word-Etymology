import httplib2

def get_wiki_url(word, language):
    """
    word and language are both string inputs
    :return: url (string) that links to the word in that language on wiktionary, "N/A" if page doesn't exist
    """

    # Wiktionary url formats differ on if the word is a reconstruction or not
    # Reconstructed words start with '*'
    if word[0] == "*":
        url = "https://en.wiktionary.org/wiki/Reconstruction:" + language + "/" + word[1:]
    else:
        url = "https://en.wiktionary.org/wiki/" + word + "#" + language

    # Make sure the page exists
    h = httplib2.Http()
    resp = h.request(url, "HEAD")
    if int(resp[0]['status']) < 400:
        return url
    else:
        return "N/A"

