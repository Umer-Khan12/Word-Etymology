import unittest
import structures as struct

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



if __name__ == '__main__':
    unittest.main()
