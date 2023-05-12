# Data structure to store word information
class Word:
    def __init__(self, spelling, ipa, url, meaning):
        self.spelling = spelling
        self.ipa = ipa
        self.url = url
        self.meaning = meaning

    def __str__(self):
        return self.spelling + self.ipa + "\nDefinition: " + self.meaning + "\nWiktionary link: " + self.url

