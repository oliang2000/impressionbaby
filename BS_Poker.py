import random
import util
from util import CARDS, CARDS_DICT, INV_CARDS_DICT, SUITS, SUITS_DICT, INV_SUITS_DICT

class BSGame:
    def __init__(self):
        self.deck = [(card, suit) for card in CARDS for suit in SUITS]
        self.__player1_cards = None
        self.__player2_cards = None

    def draw_from_deck_wo_replacement(self, n_draw):
        newdeck = []
        for i in range(n_draw):
            index = random.randint(0, len(self.deck)-1)
            card = self.deck[index]
            self.deck.pop(index)
            newdeck.append(card)
        return newdeck

    def deal(self, n_draw):
        self.__player1_cards = self.draw_from_deck_wo_replacement(n_draw)
        self.__player2_cards = self.draw_from_deck_wo_replacement(n_draw)

    def get_player1_hands(self):
        return self.__player1_cards

    def get_player2_hands(self):
        return self.__player2_cards

    def play_bs(self, claim_card, claim_quantity, claim_type):
        '''
        Strategy for guessing True or False.
        '''
        if claim_type == 0:
            #if player 2 has the claimed card(s)
            n_player2_have = 0
            for card, suit in self.__player2_cards:
                if (card == claim_card) or (card == 2):
                    n_player2_have += 1
            if claim_quantity <= n_player2_have:
                return True
            #else guess by probability
            else:
                n_cards_needed = claim_quantity-n_player2_have
                possibility = 1
                i = 0
                while i < n_cards_needed:
                    possibility *= (8-n_player2_have-i)/(52-3-i)
                    i += 1
                if possibility > 0.1: 
                    return True

        elif claim_type == 1:
            #if player 2 has the claimed card(s)
            n_player2_have = 0
            for card, suit in self.__player2_cards:
                if (suit == claim_card) or (card == 2):
                    n_player2_have += 1
            if claim_quantity <= n_player2_have:
                return True
            #else guess by probability
            else:
                n_cards_needed = claim_quantity-n_player2_have
                possibility = 1
                i = 0
                while i < n_cards_needed:
                    possibility *= (16-n_player2_have-i)/(52-3-i)
                    i += 1
                if possibility > 0.1: 
                    return True
        
        return False ##


    def judge_bs(self, claim_card, claim_quantity, claim_type):
        '''
        Judge if claim is right.
        '''
        number_of_claim_card = 0
        for card, suit in self.__player1_cards + self.__player2_cards:
            if claim_type == 0:
                if (card == claim_card) or (card == 2):
                    number_of_claim_card += 1
            else:
                if (suit == claim_card) or (card == 2):
                    number_of_claim_card += 1
            if claim_quantity == number_of_claim_card:
                return True
        return False

    def __str__(self):
        return util.cards_to_str(self.__player1_cards) + util.cards_to_str(self.__player2_cards)


def play_one_round():
    '''
    One round of guessing.
    '''
    new_game = BSGame()
    new_game.deal(3)
    print("Your hand:")
    print(util.cards_to_str(new_game.get_player1_hands()))

    print('Enter your claim')
    #ask for claim card
    while True:
        try:
            claim_type = int(input("Card (0) or Suit(1): "))
        except ValueError:
            print("Invalid value.")
            continue
        else:
            if (claim_type == 0) or (claim_type == 1):
                break
            else:
                print("Invalid value.")

    while True:
        inv_dict = INV_SUITS_DICT
        input_q = "Suit(HEART/CLUB/DIAMOND/SPADE): "
        if claim_type == 0:
            inv_dict = INV_CARDS_DICT
            input_q = "Card (A23456789JQK): "
        try:
            claim_card_input = input(input_q).upper()
            claim_card = inv_dict[claim_card_input]
        except KeyError:
            print("Invalid value.")
            continue
        else:
            break

    #ask for claim number
    while True:
        try:
            claim_quantity = int(input("Quantity of {}s (1-6): ".format(claim_card_input)))
        except ValueError:
            print("Invalid value.")
            continue
        else:
            if (claim_quantity > 6) or (claim_quantity <= 0):
                print("Invalid value.")
            else:
                break

    #player 2 judges
    player2_move = new_game.play_bs(claim_card, claim_quantity, claim_type)
    print('\nPlayer 2 thinks its', str(player2_move))

    #show hands
    print('\nShow all cards:')
    print(new_game)

    #result
    result = new_game.judge_bs(claim_card, claim_quantity, claim_type)
    if result == player2_move:
        score1 = 0
        score2 = 6 - claim_quantity
        print('\nPlayer 2 wins {} points!'.format(score2))

    else:
        score1 = claim_quantity
        score2 = 0
        print('\nPlayer 1 wins {} points!'.format(score1))
    print('\n\n')

    return (score1, score2)

def main():
    print("\nLet's play BS Poker!\n")
    score_p1 = 0
    score_p2 = 0
    cont = 'Y'
    while cont.upper() == 'Y':
        score1, score2 = play_one_round()
        score_p1 += score1
        score_p2 += score2
        print('Player 1: {} points.'.format(score_p1))
        print('Player 2: {} points.'.format(score_p2))
        cont = input('Replay (Y/N)? ')
        print('\n\n')


if __name__ == "__main__":
    main()
