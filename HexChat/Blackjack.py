import hexchat
import random

__module_name__ = 'Blackjack'
__module_version__ = '0.3.0'
__module_description__ = 'A Blackjack Bot Plugin'
__module_author__ = 'Vlek'
__module_website__ = 'https://github.com/Vlek/plugins/blob/master/HexChat/Blackjack.py'

_decks = 2
_blackjackstats = {}


def say(msg):
    """Says msg in chat within current context"""
    context = hexchat.get_context()
    context.command('say ' + msg)
    

class BlackjackStatistics:
    """Class used to house a single player's blackjack statistics"""
    def __init__(self, user):
        self.player = user
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.blackjacks = 0
        self.currenthand = None


class PokerGame:
    def __init__(self, user):
        self.suits = ['hearts', 'clubs', 'diamonds', 'spades']
        self.suitSymbols = {'hearts': "\xE2\x99\xA1", 'clubs': "\xE2\x99\xA7", 'diamonds': "\xE2\x99\xA2", 'spades': "\xE2\x99\xA4"}
        self.cardTypes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'king', 'queen', 'ace']
        self.cards = []

        for suit in self.suits:
            for cardType in self.cardTypes:
                self.cards.append([cardType, suit])

        self.player = user
        self.deck = self.cards * _decks
        self.playerHand = []
        self.houseHand = []

        #Draw some initial cards
        for i in range(2):
            self.draw()
            self.draw('house')

    def draw(self, person='player'):
        drawncard = random.choice(self.deck)
        self.deck.pop( self.deck.index( drawncard ) )
        if person == 'player':
            self.playerHand.append( drawncard )
        else:
            self.houseHand.append( drawncard )

    def hit(self):
        self.draw()
        if self.calchand() < 21:
            self.printhand('- Hit or Stand?')
        else:
            self.stand()

    def stand(self):
        #If player didn't bust or get blackjack, get the dealer some cards
        if not self.calchand('player') > 21 and not self.isblackjack():
            while self.calchand('player') > self.calchand('house') < 21 or self.calchand('house') < 17:
                #Must stand on soft 17!
                if not self.calchand('house') == 17:
                    self.draw('house')
                else:
                    break

        #Check if the player is in the stats dictionary:
        if self.player not in _blackjackstats:
            _blackjackstats[self.player] = BlackjackStatistics(self.player)

        #If house wins,
        if 22 > self.calchand('house') > self.calchand('player') or self.calchand('player') > 21 or not self.isblackjack() and self.isblackjack('house'):
            _blackjackstats[self.player].losses += 1
            self.printhand('- {} loses!'.format(self.player), False)
        #If it's a tie
        elif self.calchand('player') == self.calchand('house'):
            _blackjackstats[self.player].ties += 1
            self.printhand('- {} ties!'.format(self.player), False)
        #If the player wins
        else:
            _blackjackstats[self.player].wins += 1
            self.printhand('- {} wins!'.format(self.player), False)

        self.gameend()

    def hand(self):
        self.printhand('- Hit or Stand?')

    def printhand(self, message, hidehousehand=True):
        say('{}: {} ({}) House: {} {}'.format(self.player,
             ' '.join([self.printcard(card) for card in self.playerHand]),
             'Bust' if self.calchand() > 21 else 'Blackjack' if self.calchand() == 21 and len(self.playerHand) == 2 else self.calchand(),
             ' '.join([self.printcard(self.houseHand[0]), '?'] if hidehousehand else [self.printcard(card) for card in self.houseHand] + ['({})'.format('Bust' if self.calchand('house') > 21 else 'Blackjack' if self.calchand('house') == 21 and len(self.houseHand) == 2 else self.calchand('house'))]), message))

    def calchand(self, person='player'):
        handtotal = 0
        if person == 'player':
            hand = self.playerHand
        else:
            hand = self.houseHand

        aces = []
        for card in hand:
            #If it's a number card,
            if type(card[0]) == int:
                handtotal += card[0]
            #Gotta deal with aces last
            elif card[0] == 'ace':
                aces.append( card )
            #Else it's a face card
            else:
                handtotal += 10

            if handtotal > 21:
                return 22

        #Here's where we deal with aces
        for card in range(len(aces)):
            handtotal += 1 if handtotal > 10 or aces[card+1:] else 11

        return handtotal

    def issoft(self, person='player'):
        handtotal = 0
        if person == 'player':
            hand = self.playerHand
        else:
            hand = self.houseHand

        aces = []
        for card in hand:
            #If it's a number card,
            if type(card[0]) == int:
                handtotal += card[0]
            #Gotta deal with aces last
            elif card[0] == 'ace':
                aces.append( card )
            #Else it's a face card
            else:
                handtotal += 10

            if handtotal > 21:
                return False

        #If there's at least one ace and the sum of the number of aces
        #plus the amount of the hand before calculating the aces adds
        #up to less than 12, meaning it can take a face card, then it's soft,
        if aces and handtotal + len(aces) < 12:
            return True

        return False

    def isblackjack(self, person='player'):
        if person == 'player':
            hand = self.playerHand
        else:
            hand = self.houseHand
        return len(hand) == 2 and self.calchand(person) == 21

    def printcard(self, card):
        return '{}{}'.format(self.suitSymbols[card[1]], card[0] if type(card[0]) == int else card[0][0].title()) #self.suitSymbols[card[0]])

    def gameend(self):
        _blackjackstats[self.player].currenthand = 0

    def blackjackcheck(self):
        """This method is called after game creation to check whether to stop.
        It fixes the issue of not being able to properly remove the game from
        the current games list in the case of a blackjack. Also, it's possible
        to get a double payout if they stand afterwards."""
        #If they're lucky enough to draw 21 off the bat,
        if self.calchand() == 21:
            #End play right away,
            return self.stand()
        else:
            #Display hand
            return self.hand()


def blackjack_hit(user, command):
    #Add them to the stats collection if they're not already there,
    if user not in _blackjackstats:
        _blackjackstats[user] = BlackjackStatistics(user)

    #Start a new game if necessary,
    #(After checking if they have enough gold)
    if not _blackjackstats[user].currenthand:

        _blackjackstats[user].currenthand = PokerGame(user)
        say(_blackjackstats[user].currenthand.blackjackcheck())
    else:
        say(_blackjackstats[user].currenthand.hit())


def blackjack_stand(user, command):
    #Add them to the stats collection if they're not already there,
    if user not in _blackjackstats:
        _blackjackstats[user] = BlackjackStatistics(user)

    if _blackjackstats[user].currenthand:
        say(_blackjackstats[user].currenthand.stand())
    else:
        say("You must start a game first by saying 'hit' before standing!")


def blackjack_scores(user, command):
    if user in _blackjackstats:
        #Wins: 38 (45.2%); Losses: 46 (54.8%); Blackjacks: 3; Total: 84 (+10 ties)
        totalplays = float(_blackjackstats[user].wins+_blackjackstats[user].losses+_blackjackstats[user].ties)
        say("{} - Wins: {} ({:.1f}%); Losses: {} ({:.1f}%); Ties: {} ({:.1f}%)".format(user.title(),
                                                              _blackjackstats[user].wins,
                                                              _blackjackstats[user].wins/totalplays*100,
                                                              _blackjackstats[user].losses,
                                                              _blackjackstats[user].losses/totalplays*100,
                                                              _blackjackstats[user].ties,
                                                              _blackjackstats[user].ties/totalplays*100))
    else:
        say("You must play first to have scores!")


def savestats(dt):
    pass
    #print('Saving Blackjack statistics')


def blackjack_dispatch(word, word_eol, userdata):
    try:
        a = word[1].split()
        {
            ".hit"  : blackjack_hit,
            ".stand"  : blackjack_stand,
            ".scores"  : blackjack_scores
        }[a[0].lower()](word[0], a[1:])
    except:
        pass
    return hexchat.EAT_NONE

hexchat.hook_print('Channel Msg Hilight', blackjack_dispatch)
hexchat.hook_print('Channel Message', blackjack_dispatch)
hexchat.hook_unload(savestats)

print('Starting Blackjack bot v{}'.format(__module_version__))


