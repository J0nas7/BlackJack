# BlackJack.py
Contains the game itself.

Starts with choosing to play as Player or as Dealer

Player should choose an amount 1-200 as a bet

Playing as Dealer will make the game auto choosing a bet and figuring out which moves to take
(The player becomes a kind of NPC)

The game is made with rules found online

After each move is finished, a function will check if we have a winner and/or a looser.

When a round has finished, it is possible to continue or stop playing

# test_BlackJack.py
Tests two functions

The printHand() function that makes a template of the current hand(s) of Player and Dealer along with their points

The cardValue() function that validates what value to give a card. 2-10 = 2-10; A = 1; J, Q, K = 10

# Cards_Singleton.py
This class holds the card deck in a Singleton class.

This asure os that the game can not have multiple decks to choose cards from.

The Singleton instance makes sure that we can only have one instance of the class,
which is called from a public function that returns the one and only instance of the Cards Singleton class.

The Singleton Class has a constructor if "the instance" has been set, if not, will set it. If it is set, it throws and error telling it's a Singleton.

There is a list of possible cards in the class. This list is shuffled everytime we want to pick a card.

Don't think normal casinos shuffles the card deck everytime. But this is easily done in a program, and makes a higher rate of random cards.
