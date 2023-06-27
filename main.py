# In-console IO loop for the Wiktionary webscraper\

import webscraper as ws


print("Wiktionary Webscraper\nTo exit the program at any point type exit()\n")

while True:
    word = input("----------------------------------------------------------------------------\nEnter a word: ")
    while word == "":
        print("No word entered.")
        word = input("Enter a word: ")
    if word == "exit()":
        break

    language = input("Enter the language the word belongs to: ")
    while language == "":
        print("No language entered.")
        language = input("Enter the langauge the word belongs to: ")
    if language == "exit()":
        break

    # Fix formatting for word and language
    word = word.lower()
    language = language.title()

    url_tuple = ws.get_wiki_url(word, language)
    if url_tuple is None:
        print("\nA Wiktionary URL doesn't exist for this word (in any language).")
    elif url_tuple[1] is False:
        print("\nA Wiktionary URL exists for this word but not in this language.")
        print("The languages for this word on Wiktionary are: ")
        print("    " + ", ".join(ws.languages_on_page(url_tuple[0])))
    else:
        url = url_tuple[0]
        print("Definition:\n" + ws.get_wiki_definition(url, language) + "\n")
        print("Pronunciation:\n" + ws.get_wiki_pronunciation(url, language) + "\n")
        print("Etymology:\n" + ws.get_wiki_etymology(url, language))
