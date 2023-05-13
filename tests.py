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
            ("land", "English"): "https://en.wiktionary.org/wiki/land#English",
            ("sjksjweqwqe", "English"): "No Wiktionary page found.",
            ("encampment", "Chinese"): "https://en.wiktionary.org/wiki/encampment#Chinese (No section for Chinese)",
            ("茶", "Chinese"): "https://en.wiktionary.org/wiki/茶#Chinese",
            ("déjà vu", "English"): "https://en.wiktionary.org/wiki/déjà_vu#English",
            ("خاکی", "Urdu"): "https://en.wiktionary.org/wiki/خاکی#Urdu",
            ("茶", "German"): "https://en.wiktionary.org/wiki/茶#German (No section for German)",
            ("heofon", "Old English"): "https://en.wiktionary.org/wiki/heofon#Old_English"
        }
        for inputs, expected in inputs_and_expected.items():
            self.assertEqual(expected, ws.get_wiki_url(inputs[0], inputs[1]))

        # Test reconstructed word urls
        inputs_and_expected = {
            ("himinaz", "Proto-Germanic"): "https://en.wiktionary.org/wiki/Reconstruction:Proto-Germanic/himinaz",
            ("*h₂enh₁-", "Proto-Indo-European"):
                "https://en.wiktionary.org/wiki/Reconstruction:Proto-Indo-European/h₂enh₁-"
        }
        for inputs, expected in inputs_and_expected.items():
            self.assertEqual(expected, ws.get_wiki_url(inputs[0], inputs[1]))


if __name__ == '__main__':
    unittest.main()
