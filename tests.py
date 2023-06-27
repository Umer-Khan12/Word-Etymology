import unittest
import structures as struct
import webscraper as ws

class TestStructures(unittest.TestCase):
    def test_word(self):
        result = struct.Word("red", "/ɹɛd/", "https://en.wiktionary.org/wiki/red", "Having red as its color.")
        self.assertEqual(str(result), "red /ɹɛd/\nDefinition: Having red as its color.\nWiktionary link: "
                                      "https://en.wiktionary.org/wiki/red")

    # Tests the Node class too
    def test_linkedlist(self):
        list1 = struct.LinkedList()
        self.assertEqual(list1.head, None)
        list1.head = struct.Node(0)
        self.assertEqual(list1.head.val, 0)
        self.assertEqual(list1.head.next_val, None)

        list2 = struct.LinkedList(struct.Node(1))
        self.assertEqual(list2.head.val, 1)
        node2 = struct.Node(2)
        node3 = struct.Node(3)
        node2.next_val = node3
        list2.head.next_val = node2
        # list2 = [1 | -]->[2 | -]->[3 |/]
        cur = list2.head
        list_string = ""
        while cur is not None:
            list_string += str(cur.val)
            cur = cur.next_val
        self.assertEqual(list_string, "123")


class TestWebscraper(unittest.TestCase):
    def test_get_wiki_url(self):
        # Test non-reconstructed word urls
        inputs_and_expected = {
            ("land", "English"): ["https://en.wiktionary.org/wiki/land#English", True],
            ("sjksjweqwqe", "English"): None,
            ("encampment", "Chinese"): ["https://en.wiktionary.org/wiki/encampment#Chinese", False],
            ("茶", "Chinese"): ["https://en.wiktionary.org/wiki/茶#Chinese", True],
            ("déjà vu", "English"): ["https://en.wiktionary.org/wiki/déjà_vu#English", True],
            ("خاکی", "Urdu"): ["https://en.wiktionary.org/wiki/خاکی#Urdu", True],
            ("茶", "German"): ["https://en.wiktionary.org/wiki/茶#German", False],
            ("heofon", "Old English"): ["https://en.wiktionary.org/wiki/heofon#Old_English", True]
        }
        for inputs, expected in inputs_and_expected.items():
            self.assertEqual(expected, ws.get_wiki_url(inputs[0], inputs[1]))

        # Test reconstructed word urls
        inputs_and_expected = {
            ("himinaz", "Proto-Germanic"):
                ["https://en.wiktionary.org/wiki/Reconstruction:Proto-Germanic/himinaz", True],
            ("*h₂enh₁-", "Proto-Indo-European"):
                ["https://en.wiktionary.org/wiki/Reconstruction:Proto-Indo-European/h₂enh₁-", True]
        }
        for inputs, expected in inputs_and_expected.items():
            self.assertEqual(expected, ws.get_wiki_url(inputs[0], inputs[1]))


    def test_is_red_link(self):
        self.assertEqual(ws.is_red_link("https://en.wiktionary.org/w/index.php?title=neeke&action=edit&redlink=1")
                         , True)
        self.assertEqual(ws.is_red_link("https://en.wiktionary.org/wiki/neck"), False)


    def test_languages_on_page(self):
        self.assertEqual(ws.languages_on_page("https://en.wiktionary.org/wiki/bath"),
                         ["English", "French", "Middle English", "Welsh", "Yola"])
        self.assertEqual(ws.languages_on_page("https://en.wiktionary.org/wiki/blatant"),
                         ["English"])


    def test_get_wiki_pronunciation(self):
        inputs_and_expected = {
            ("https://en.wiktionary.org/wiki/bath#English", "English"):
                "(Received Pronunciation, General South African) IPA: [bɑːθ]\n(North India) IPA: [bɑːt̪ʰ]\n"
                "(South India) IPA: [bɑːt̪]\n(General Australian, New Zealand) IPA: /bɐːθ/\n"
                "(US, Canada) IPA: [bæθ~bɛəθ~beəθ]\n(Northern England, Ireland) IPA: [baθ~bæθ]",
            ("https://en.wiktionary.org/wiki/bath#English", "qwerty"): "Not found.",
            ("https://en.wiktionary.org/wiki/bath#English", "Welsh"):
                "IPA: /baːθ/",
            ("https://en.wiktionary.org/wiki/%E0%A4%AC%E0%A5%81%E0%A4%A6%E0%A5%8D%E0%A4%A7#Sanskrit", "Sanskrit"):
                "(Vedic) IPA: /bud.dʱɐ́/, [bud̚.dʱɐ́]\n(Classical) IPA: /ˈbud̪.d̪ʱɐ/, [ˈbud̪̚.d̪ʱɐ]",
        }
        for inputs, expected in inputs_and_expected.items():
            self.assertEqual(expected, ws.get_wiki_pronunciation(inputs[0], inputs[1]))


    def test_get_wiki_etymology(self):
        inputs_and_expected = {
            ("https://en.wiktionary.org/wiki/bath#English", "English"):
                "From Middle English bath, baþ, from Old English bæþ (“bath”), from Proto-West Germanic *baþ, from "
                "Proto-Germanic *baþą (“bath”), from Proto-Indo-European *bʰeh₁- (“to warm”). Corresponding inherited "
                "verbs are beath and bathe.",
            ("https://en.wiktionary.org/wiki/bath#English", "qwerty"): "Not found.",
            ("https://en.wiktionary.org/wiki/bath#English", "Welsh"):
                "Probably from Proto-Celtic *batto-; according to the GPC, possibly related to Latin battuo "
                "(“I fight, pound, beat (up)”), though the semantics are far from certain.[1]",
            ("https://en.wiktionary.org/wiki/%E0%A4%AC%E0%A5%81%E0%A4%A6%E0%A5%8D%E0%A4%A7#Sanskrit", "Sanskrit"):
                "From Proto-Indo-Aryan *buddʰás, from Proto-Indo-Iranian *bʰudᶻdʰás, from Proto-Indo-European "
                "*bʰudʰtós (“awake, aware”). Cognate with Ancient Greek πυστός (pustós), Avestan 𐬠𐬎𐬯𐬙𐬀‎ (busta) "
                "and Russian будить (buditʹ, “to wake up”).",
        }
        for inputs, expected in inputs_and_expected.items():
            self.assertEqual(expected, ws.get_wiki_etymology(inputs[0], inputs[1]))


    def test_get_wiki_definition(self):
        inputs_and_expected = {
            ("https://en.wiktionary.org/wiki/Reconstruction:Proto-Hellenic/k%CA%B7%C3%A9twores", "Proto-Hellenic"):
                "*kʷétwores\n    four",
            ("https://en.wiktionary.org/wiki/bath#English", "qwerty"): "Not found.",
            ("https://en.wiktionary.org/wiki/%F0%90%8C%B2%F0%90%8D%82%F0%90%8C%B9%F0%90%8C%B8%F0%90%8D%83#Gothic",
             "Gothic"):
                "𐌲𐍂𐌹𐌸𐍃 • (griþs) f\n    rank, grade, standing",
            ("https://en.wiktionary.org/wiki/%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%A5%E0%A4%B8%E0%A5%8D#Sanskrit",
             "Sanskrit"):
                "प्रथस् • (práthas) n\n    width, extension",
        }
        for inputs, expected in inputs_and_expected.items():
            self.assertEqual(expected, ws.get_wiki_definition(inputs[0], inputs[1]))


if __name__ == '__main__':
    unittest.main()
