## Singleton Design Pattern
import random

class theCards():
    __theInstance = None

    allCards = []

    @staticmethod
    def getInstance():
        ## Static access method
        if theCards.__theInstance == None:
            theCards()
        return theCards.__theInstance

    def __init__(self):
        """ Virtually private constructor. """
        if theCards.__theInstance != None:
            raise Exception("This class is a singleton!")
        else:
            theCards.__theInstance = self

    def reset(self):
        self.allCards = [
            "A", "A", "A", "A", ## Es
            2, 2, 2, 2,
            3, 3, 3, 3,
            4, 4, 4, 4,
            5, 5, 5, 5,
            6, 6, 6, 6,
            7, 7, 7, 7,
            8, 8, 8, 8,
            9, 9, 9, 9,
            10, 10, 10, 10,
            "J", "J", "J", "J", ## Knight
            "Q", "Q", "Q", "Q", ## Queen
            "K", "K", "K", "K"  ## King
        ]

    def getAllCards(self):
        return self.allCards

    def getCard(self):
        random.shuffle(self.allCards)
        cardToSend = self.allCards.pop(0)
        return cardToSend