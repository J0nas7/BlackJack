import unittest
from BlackJack import printHand
from BlackJack import cardValue

class TestBlackJack(unittest.TestCase):
    def test_printHand(self):
        title = "Spiller"
        showNum = 1
        hand = [1,"J",3]
        result = printHand(title, showNum, hand)
        self.assertEqual(result, "Spiller\n1, J og 3\nI ALT: 14")

    def test_cardValue1(self):
        theCard = 10
        result = cardValue(theCard)
        self.assertEqual(result, 10)

    def test_cardValue2(self):
        theCard = 3
        result = cardValue(theCard)
        self.assertEqual(result, 3)

    def test_cardValue3(self):
        theCard = "Q"
        result = cardValue(theCard)
        self.assertEqual(result, 10)

    def test_cardValue4(self):
        theCard = 20
        result = cardValue(theCard)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()
