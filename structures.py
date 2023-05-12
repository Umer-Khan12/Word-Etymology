# Data structure to store word information
class Word:
    def __init__(self, spelling, ipa, url, meaning):
        self.spelling = spelling
        self.ipa = ipa
        self.url = url
        self.meaning = meaning

    def __str__(self):
        return self.spelling + " " + self.ipa + "\nDefinition: " + self.meaning + "\nWiktionary link: " + self.url


# Linked list
class Node:
    def __init__(self, val, next_val=None):
        self.val = val
        self.next_val = next_val

    def __str__(self):
        return "Value = " + self.val + "\n\nNext = " + self.next_val

class LinkedList:
    def __init__(self, head=None):
        self.head = head

