import random
from nn import baby, make_and_verify_guess # :)
from tensorflow.keras.optimizers import Adam
import numpy as np


cards = list(range(1, 14))
cards_dict = {1:'A', 2:'2', 3:'3', 4:'4', 5:'5', 6: '6', 7: '7', 8: '8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K'}
inv_cards_dict = {v: k for k, v in cards_dict.items()}

suits = list(range(3))
suits_dict = {0: 'HEART', 1: 'CLUB', 2:'DIAMOND', 3:'SPADE'}
inv_suits_dict = {v: k for k, v in suits_dict.items()}


def cards_to_str(cards):
    '''
    String of cards in tuple
    '''
    s = ''
    for card, suit in cards:
        s += '{} of {}'.format(cards_dict[card], suits_dict[suit]) + '\n'
    return s


class Cards:
    def __init__(self, n_draw):
        self.deck = [(card, suit) for card in cards for suit in suits]
        self.n_draw = n_draw
        self.__player1_cards = None
        self.__player2_cards = None


    def draw_from_deck_wo_replacement(self):
        newdeck = []
        for i in range(self.n_draw):
            index = random.randint(0, len(self.deck)-1)
            card = self.deck[index]
            self.deck.pop(index)
            newdeck.append(card)
        return newdeck

    def deal(self):
        self.__player1_cards = self.draw_from_deck_wo_replacement()
        self.__player2_cards = self.draw_from_deck_wo_replacement()

    def show_player1_hands(self):
        print(cards_to_str(self.__player1_cards))

    def play_bs(self, claim_card, claim_quantity, claim_type, agent):
        claim = np.array([claim_type, claim_card,claim_quantity])
        agent, guess = make_and_verify_guess(self.__player1_cards,self.__player2_cards,claim,agent)

        return agent, guess

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
        return cards_to_str(self.__player1_cards) + cards_to_str(self.__player2_cards)


def play_one_round(agent):
    '''
    One round of guessing.
    '''
    new_cards = Cards(3)
    new_cards.deal()
    print("Your hand:")
    new_cards.show_player1_hands()

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
        inv_dict = inv_suits_dict
        input_q = "Suit(HEART/CLUB/DIAMOND/SPADE): "
        if claim_type == 0:
            inv_dict = inv_cards_dict
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
    agent, player2_move = new_cards.play_bs(claim_card, claim_quantity, claim_type, agent)
    print('\nPlayer 2 thinks its', str(player2_move))

    #show hands
    print('\nShow all cards:')
    print(new_cards)

    #result
    result = new_cards.judge_bs(claim_card, claim_quantity, claim_type)
    if result == player2_move:
        score1 = 0
        score2 = 6 - claim_quantity
        print('\nPlayer 2 wins {} points!'.format(score2))

    else:
        score1 = claim_quantity
        score2 = 0
        print('\nPlayer 1 wins {} points!'.format(score1))
    print('\n\n')

    return agent, (score1, score2)

def main():
    print("\nLet's play BS Poker!\n")
    score_p1 = 0
    score_p2 = 0
    cont = 'Y'
    # build and compile
    baby_object = baby()
    model = baby_object.build_model()
    agent = baby_object.build_agent()
    agent.compile(Adam(lr=1e-3), metrics=['mae']) #mean absolute error

    while cont.upper() == 'Y':
        agent, score1, score2 = play_one_round(agent)
        score_p1 += score1
        score_p2 += score2
        print('Player 1: {} points.'.format(score_p1))
        print('Player 2: {} points.'.format(score_p2))
        cont = input('Replay (Y/N)? ')
        print('\n\n')


if __name__ == "__main__":
    main()
