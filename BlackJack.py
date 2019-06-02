from random import randint
from Cards_Singleton import theCards
import clr
import subprocess

dealerCards = []
playerCards = []
playerCards2 = []
theBet = 0
saldo = 0

Cards = theCards().getInstance()
prefixMove = ""
badChoise = "Ugyldigt valg!"
insurance = False
split = False
automatic = False

def playerGame(restart = False): ## Starting the game from player perspective
    global theBet, dealerCards, playerCards, playerCards2, insurance, split
    if (restart): ## A game has been finished, and the player wants to start a new one, resetting the global variables
        Cards.reset()
        dealerCards = []
        playerCards = []
        playerCards2 = []
        insurance = False
        split = False
        print("\n\nDin saldo er nu på: "+str(saldo)) ## Current saldo continues

    print("Hvor meget vil du satse?:")
    theBet = input("(mellem 1-200kr) ") ## Player placing the bet

    try:
        betNum = int(theBet) ## Se if the bet is numeric
    except ValueError:
        ## Print error msg if not numeric and then start this function over again
        print("\n"+badChoise+" Dit sats skal være et tal.")
        playerGame()

    if (0 < betNum and betNum < 201): ## If bet is correctly places between 1-200
        print("\nDu satser "+theBet+"kr.")
        giveFirstCards()
    else:
        print("\nDu skal satse 1-200 kr.") ## Bet amount not allowed
        playerGame()

def dealerGame(restart = False): ## Starting the game from dealer perspective
    global theBet, dealerCards, playerCards, playerCards2, insurance, split
    if (restart): ## A game has been finished, and the dealer wants to start a new one, resetting the global variables
        Cards.reset()
        dealerCards = []
        playerCards = []
        playerCards2 = []
        insurance = False
        split = False
        print("\n\nSpillers saldo er nu på: "+str(saldo)) ## Current saldo continues

    ##print("Hvor meget vil du satse?:") NPC will place the bet
    if (0 < saldo and saldo < 201) :
        theBet = saldo
    elif (saldo < 0 and -201 < saldo) :
        theBet = saldo * -1
    elif (0 < saldo):
        theBet = 200
    else:
        theBet = 50

    try:
        betNum = int(theBet) ## Se if the bet is numeric
    except ValueError:
        ## Print error msg if not numeric and then start this function over again
        print("\n"+badChoise+" Spillers sats skal være et tal.")
        dealerGame()

    if (0 < betNum and betNum < 201): ## If bet is correctly places between 1-200
        print("\nSpiller satser "+str(theBet)+"kr.")
        giveFirstCards()
    else:
        print("\nSpiller skal satse 1-200 kr.") ## Bet amount not allowed
        dealerGame()

def giveFirstCards(): ## Player gets two cards, dealer gets one card
    for i in range(2):
        theCard = Cards.getCard()
        playerCards.append(theCard)
    for i in range(1):
        theCard = Cards.getCard()
        dealerCards.append(theCard)
    cardStatus() ## Make an overview of cards and points

def givePlayerCard(): ## One card to the player
    global automatic
    if (automatic == False): ## Player-mode where card is given automatic
        theCard = Cards.getCard()
        playerCards.append(theCard)
        if 0 < len(playerCards2):
            theCard = Cards.getCard()
            playerCards2.append(theCard)
    elif (automatic): ## Dealer-mode where card is given after dealer inputs "G" for Give
        dealerInput = input("Giv spilleren et kort mere (G): ")
        if (dealerInput == "G"):
            theCard = Cards.getCard()
            playerCards.append(theCard)
            if 0 < len(playerCards2):
                theCard = Cards.getCard()
                playerCards2.append(theCard)
        else:
            print(badChoise)
            givePlayerCard()
    cardStatus() ## Make an overview of cards and points

def dealerTakeCard(): ## One card to the dealer
    if (automatic == False): ## Player-mode where cards is taken automatic
        theCard = Cards.getCard()
        dealerCards.append(theCard)
        totalVal = 0
        for card in dealerCards:
            totalVal = totalVal + cardValue(card)
    elif (automatic): ## Dealer-mode where card is taken after dealer inputs "T" for Take
        curVal = 0
        for card in dealerCards:
            curVal = curVal + cardValue(card)
        print("Nu har du "+str(curVal))
        dealerInput = input("Tag kort indtil du opnår 17 (T): ")
        if (dealerInput == "T"):
            theCard = Cards.getCard()
            dealerCards.append(theCard)
            totalVal = 0
            for card in dealerCards:
                totalVal = totalVal + cardValue(card)
        else:
            print(badChoise)
            totalVal = curVal

    if (totalVal < 17): ## This function continues until dealer hits 17 points
        dealerTakeCard()
    else: ## After dealer hits 17 points, make an overview of cards and points
        cardStatus()

def printHand(title, showNum, hand): ## A template for showing which part (player or dealer) have which cards and points
    printText = title + "\n" ## Printing the title
    count = 1
    totalVal = 0
    for card in hand:
        printText = printText + str(card) ## Printing each card with comma separation
        if count+1 == len(hand):
            printText = printText + " og "
        elif count < len(hand):
            printText = printText + ", "

        try:
            theCardVal = cardValue(card) ## Numeric value of the card (J, Q, K = 10, Es = 1)
        except ValueError:
            print(clr.red("\n"+badChoise+" Alle kort skal være numeriske (Ugyldig = "+card+")"))
            theCardVal = 0
        totalVal += theCardVal
        count += 1
    return (printText+"\nI ALT: "+str(totalVal))
    """
        EXAMPLE:
        
        Spillers hånd:
        K, 6, 2
        I ALT: 18
    """

def cardStatus(): ## Make an overview of cards and points
    if (split): ## Show the overview when player has to hands
        playerHands = [playerCards, playerCards2]
        oneOrTwo = "ene";
        for hand in playerHands: ## Iterate over each player hand
            handTitle = "Spillers "+oneOrTwo+" hånd"
            oneOrTwo = "anden"
            showNum = 0
            theHand = hand
            print(printHand(handTitle, showNum, theHand)) ## Each hand is outputted through the printHand template
    else: ## Show the overview when player has one hand
        handTitle = "Spillers hånd"
        showNum = 0
        theHand = playerCards ## The player hand
        print(printHand(handTitle, showNum, theHand)) ## The hand is outputted through the printHand template

    handTitle = "Dealers hånd" ## Overview of the dealers hand
    showNum = 0
    theHand = dealerCards
    print(printHand(handTitle, showNum, theHand)) ## The dealers hand is outputted through the printHand template

    checkForWin() ## Validate if the player of dealer is capable of winning as the hands are now

def cardValue(theCard): ## Calculate card value (1-10 = 1-10; J, Q, K = 10)
    if (theCard == "J" or theCard == "Q" or theCard == "K"):
        theCard = 10
    elif (theCard == "A"):
        theCard = 1

    try:
        theCard = int(theCard) ## 1-10 including J, Q, K
    except ValueError:
        ## Error thrown is theCard is not either 1-10, J, Q og K
        print(clr.red("\n"+badChoise+" Kortet skal være et J, Q, K eller et tal ml. 1-10, for at kunne vurderes."))
        theCard = 0 ## Value is set to 0 for error handling

    if (0 < theCard and theCard < 11): ## If the card value is between 1-10, it'll be returned
        return theCard
    else: ## If the card value fails
        return False

def checkForWin(): ## After making an overview of hands, we will check if one is capable of winning
    if split: ## If the player has splitted and plays with two hands
        playerHands = [playerCards, playerCards2]
        totalPlayerVal = []
        totalPlayerVal.append(0)
        totalPlayerVal.append(0)
        totalDealerVal = 0
        theHandIndex = 0
        for hand in playerHands: ## Iterate over each player hand
            for card in hand:
                totalPlayerVal[theHandIndex] = totalPlayerVal[theHandIndex] + cardValue(card)
            theHandIndex += 1
        for card in dealerCards: ## Iterate over the dealers hand
            totalDealerVal = totalDealerVal + cardValue(card)

        print("\n"+str(totalPlayerVal[0])+" "+str(totalPlayerVal[1])+" "+str(totalDealerVal)) ## For debugging purpose, better overview
        if (totalPlayerVal[0] == 21 or totalPlayerVal[1] == 21): ## If the player has BlackJack
            print("Black Jack") ## Debugging to see winning case
            if (totalPlayerVal[0] < totalDealerVal or totalPlayerVal[1] < totalDealerVal): ## If the dealer has higher score than one of the player hands, the player only win with the Black Jack hand
                twoWin = False
                print("F")
            else: ## If both player hands are higher than the dealer hand. Player will DoubleWin
                twoWin = True
                print("T")
            playAgain(21, totalDealerVal, True, twoWin) ## Finish the game with a winner

        elif (21 < totalDealerVal): ## If the dealer hits more than 21 and loses
            print("Dealer loses") ## Debugging to see winning case
            playAgain(20, 22, True) ## Finish the game with a winner

        elif (totalPlayerVal[0] > 21 or totalPlayerVal[1] > 21): ## If the player hits more than 21 and loses
            print("More than 21") ## Debugging to see winning case
            playAgain(22, totalDealerVal, False) ## Finish the game with a winner

        elif (totalPlayerVal[0] > totalDealerVal and totalPlayerVal[1] > totalDealerVal and 17 <= totalDealerVal): ## If the player wins DoubleWin but none of them is BlackJack
            print("Double win not Black jack ") ## Debugging to see winning case
            playAgain(20, totalDealerVal, True, True) ## Finish the game with a winner

        elif (totalPlayerVal[0] < totalDealerVal and totalPlayerVal[1] < totalDealerVal and 17 <= totalDealerVal): ## If the dealer wins over both player hands
            print("Dealer wins") ## Debugging to see winning case
            playAgain(0, totalDealerVal, False) ## Finish the game with a winner

        elif ((totalPlayerVal[0] > totalDealerVal or totalPlayerVal[1] > totalDealerVal) and 17 <= totalDealerVal): ## If the player wins, but no DoubleWin and no BlackJack
            print("One hand win") ## Debugging to see winning case
            playAgain(20, totalDealerVal, True, False) ## Finish the game with a winner

        else: ## If nobody can win or lose yet, the game will continue asking for a move
            chooseNextMove()

    else: ## If the player has one playing hand
        totalPlayerVal = 0
        totalDealerVal = 0
        ## Iterate over player and dealer hand
        for card in playerCards:
            totalPlayerVal = totalPlayerVal + cardValue(card)
        for card in dealerCards:
            totalDealerVal = totalDealerVal + cardValue(card)

        if (totalPlayerVal == 21): ## If player has BlackJack
            playAgain(totalPlayerVal, totalDealerVal, True)     ## Finish the game with player as winner
        elif (totalPlayerVal > 21): ## If player hits more than 21
            playAgain(totalPlayerVal, totalDealerVal, False)    ## Finish the game with dealer as winner
        elif (totalDealerVal > 21): ## If dealer hits more than 21
            playAgain(totalPlayerVal, totalDealerVal, True)     ## Finish the game with player as winner
        elif (17 <= totalDealerVal and totalPlayerVal < totalDealerVal): ## Dealer wins over player
            playAgain(totalPlayerVal, totalDealerVal, False)    ## Finish the game with dealer as winner
        elif (17 <= totalDealerVal and totalPlayerVal > totalDealerVal): ## Player wins over dealer
            playAgain(totalPlayerVal, totalDealerVal, True)     ## Finish the game with player as winner
        elif (17 <= totalDealerVal and 17 <= totalPlayerVal and totalDealerVal == totalPlayerVal): ## Same points player wins
            playAgain(totalPlayerVal, totalDealerVal, True)     ## Finish the game with player as winner
        else: ## If nobody can win or lose yet, the game will continue asking for a move
            if 2 == len(playerCards): ## First move in the game, after player has gotten two cards and dealer has gotten one card
                chooseFirstMove()
            else: ## Next move in the game
                chooseNextMove()

def playAgain(playerTotal = 0, dealerTotal = 0, won = True, DoubleWin = False): ## Finish the game with a winner and a looser
    global saldo, theBet, automatic

    if (won): ## If the player won
        if (playerTotal == dealerTotal): ## Player and dealer has same score
            print(clr.italic.yellow("=== Push! I ender på samme værdi. Spiller får indsatsen retur."))
            saldo = (int(saldo)) ## Saldo remains unchanced, no actual winner
        else:
            if (automatic == False): ## Player win from player-perspective
                print(clr.bold.green("\n=== Tillykke! Du har vundet runden! :-D ==="))
            else: ## Player win from dealer-perspective
                print(clr.bold.red("\n=== Desværre! Du har tabt runden! :-( ==="))

            if (DoubleWin): ## If player has DoubleWin
                print(clr.bold.green("Spiller vinder på begge hænder! Dobbelt op på dobbelt op!"))
                saldo = (int(saldo) + int(theBet) + (int(theBet)*2)) ## Double of the winning amount (which is already twofold)
            else: ## Player wins the bet twofold
                saldo = (int(saldo) + int(theBet) + int(theBet))
    else: ## If the dealer won
        if (automatic == True): ## Dealer win from dealer-perspective
            print(clr.bold.green("\n=== Tillykke! Du har vundet runden! :-D ==="))
        else: ## Dealer win from player-perspective
            print(clr.bold.red("\n=== Desværre! Du har tabt runden! :-( ==="))

        if (insurance): ## If the player has bought insurance, the bet will be returned
            print(clr.italic.red("Men der er købt forsikring! Indskud kommer derfor retur."))
            saldo = (int(saldo) + int(theBet))
        else: ## Without insurance, the player loses the bet
            saldo = (int(saldo) - int(theBet))

    print(clr.yellow("Spillersaldo: "+str(saldo))) ## Current saldo in game
    playAgain = input("Spil igen? (Y/N): ") ## Play again? (Y/N)
    if (playAgain == "Y"):
        ## subprocess.run(["clear"])
        if (automatic):
            dealerGame(True) ## Play again dealer perspective
        else:
            playerGame(True) ## Play again player perspective

def chooseFirstMove(): ## Description of the different possible moves, will be shown first time
    global automatic
    if (automatic == False):
        print("\nMuligheder:")
        print("(H) HIT: Du får et kort mere. Vær opmærksom på, at du kan få så mange kort du ønsker, men husk: Får du over 21, så har du tabt.")
        print("(ST) STAND: Du får ikke flere kort og det er nu dealerens tur.")
        print("(D) DOUBLE: Du fordobler indsatsen i spillet, og  får ET kort mere. Så er det dealerens tur.")
        print("(SP) SPLIT: Du splitter dine to kort op og opnår derved to separate spil")
        print("(I) INSURANCE: Hvis dealeren har et es, kan du forsikre dig mod at dealeren får Black Jack. Forsikring koster halvdelen af dit indskud. Hvis du har forsikret og dealeren får Black Jack, får du dit indskud tilbage. Det koster altså halvdelen af dit oprindelige indskud.")
        print("(R) RETIRE/SURRENDER: Giver dig mulighed for at opgive din korthånd, hvis du mener dine chancer for at vinde er dårlige. Det koster halvdelen af dit indskud.")

    makeAMove()

def chooseNextMove(): ## Short presentation of the different possible moves
    if (automatic == False):
        print("\nMuligheder: (H) HIT (SP) SPLIT (ST) STAND (D) DOUBLE (R) RETIRE/SURRENDER (I) INSURANCE")
        print("Brug for forklaringer? (HELP) HJÆLP")

    makeAMove()

def makeAMove(test = ""): ## Next move in the game
    global saldo, theBet, prefixMove, insurance, split, automatic
    title = "Du" ## Title from player-perspective
    if (automatic == False): ## If we play as player, we choose the move
        if (prefixMove == ""): ## Player choose move
            print(clr.yellow("\nHvad vil du gøre nu?:"))
            theMove = input(" ")
            subprocess.run(["clear"])
        else: ## If a previous move has prefixed this move
            theMove = prefixMove
    elif (automatic and theBet > 0): ## If we play as dealer
        title = "Spiller" ## Title from dealer-perspective
        if (prefixMove == ""): # An Intelligent function will choose next player-move
            theMove = player_intelligence()
        else: ## If a previous move has prefixed this move
            theMove = prefixMove
    else:
        theMove = test

    ## SEE DESCRIPTIONS IN THE chooseFirstMove() FUNCTION
    if (theMove == "H"):
        givePlayerCard()
    elif(theMove == "ST"):
        dealerTakeCard()
        prefixMove = "ST"
    elif(theMove == "D"):
        theBet = (int(theBet) * int(2)) ## The given bet will be doubled
        print(title+" får et kort mere og fordobler indsatsen til: "+str(theBet))
        prefixMove = "ST"
        givePlayerCard()
    elif(theMove == "R"):
        saldo = (int(saldo) - int(theBet)/2) ## Player gives up, loses half of the bet
        print(title+" giver op! Det koster halvdelen af satset. Trækkes fra saldoen.")
        playAgain(0,0,False)
    elif(theMove == "I"):
        print("\n"+title+" køber forsikring mod at tabe, nuværende saldo: "+str(saldo))
        saldo = (int(saldo) - (int(theBet)/2)) ## Player buys insurance from losing, costing half the bet, but insures to get the bet back
        print("Det koster halvdelen af satset ("+str(theBet)+"), saldo: "+str(saldo))
        insurance = True
        chooseNextMove()
    elif(theMove == "SP"): ## Player will split two first given cards
        if 2 == len(playerCards):
            if (playerCards[0] == playerCards[1]): ## Split can only happen with identical cards
                playerCards2.append(playerCards.pop(0))
                split = True
                cardStatus() ## Overview of hands and points
            else:
                print(badChoise+" "+title+" skal have to ens kort på hånden.")
                chooseNextMove()
        else:
            print(badChoise+" "+title+" må kun have to kort på hånden, når "+title+" splitter")
            chooseNextMove()
    elif(theMove == "HELP"):
        chooseFirstMove()
    else: ## Invalid Move
        print(badChoise+" Det træk findes ikke.")
        chooseNextMove()

def player_intelligence(): ## Function that tries to figure out smartest move for player, playing from dealer-perspective
    global saldo, theBet, prefixMove, insurance, split, automatic, dealerCards, playerCards, playerCards2

    ## Iterate over possible hands
    playerTotal = 0
    for num in playerCards:
        playerTotal = playerTotal + cardValue(num)
    playerTotal2 = 0
    for num in playerCards2:
        playerTotal2 = playerTotal2 + cardValue(num)

    dealerFirstCard = cardValue(dealerCards[0])
    if (len(playerCards) == 2 and playerCards[0] == playerCards[1] and split == False): ## Split if possible
        split = True
        return "SP"
    elif (len(dealerCards) == 1 and dealerFirstCard > 8 and insurance == False): ## Buy insurance if dealer has a high start card (9 or 10 points)
        return "I"
    elif (split): ## If player has two playing hands
        if (playerTotal < 16 and playerTotal2 < 16): ## Hit new cards if both hands are under 16 points
            return "H"
        else:
            return "ST" ## Stay and let dealer pick cards, if both hands are over 16
    elif (playerTotal < 16): ## If the one playing hand is under 16 points
        if (len(dealerCards) == 1 and dealerFirstCard < 6): ## And if the dealer has under 6 points
            return "D" ## Double the bet and take a card
        else:
            return "H" ## If dealer has over 5 points, just take a card
    else:
        return "ST" ## Player is happy with the position now, and dealer takes card until reaching 17+ points

def startGame(): ## Very start of game
    global automatic
    chooseSide = input("Vil du være spiller (S) eller dealer (D)?: ") ## Choose to play as Player og as Dealer
    if chooseSide == "S":
        playerGame()
    elif chooseSide == "D":
        automatic = True
        dealerGame()
    else:
        print(badChoise)
        startGame()

if __name__ == '__main__':
    startGame()