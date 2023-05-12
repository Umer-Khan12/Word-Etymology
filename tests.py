import unittest as ut
import webscraper as ws

class TestWebscraper(ut.TestCase):
    def test_word(self):
        result = ws.Word("red", "/ɹɛd/", "https://en.wiktionary.org/wiki/red", "Having red as its color.")
        self.assertEqual(str(result), "red /ɹɛd/\nDefinition: Having red as its color.\nWiktionary link: "
                                      "https://en.wiktionary.org/wiki/red")


if __name__ == '__main__':
    ut.main()
