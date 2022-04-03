import random
from nn import baby, make_and_verify_guess # :)
from tensorflow.keras.optimizers import Adam
import numpy as np
import util
from util import CARDS, CARDS_DICT, INV_CARDS_DICT, SUITS, SUITS_DICT, INV_SUITS_DICT


class BSGame:
    def __init__(self):
        self.deck = [(card, suit) for card in CARDS for suit in SUITS]
        self.__player1_cards = None
        self.__player2_cards = None
        self.claim_type = 0
        self.claim_card = None
        self.claim_quantity = None

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

    def play_bs(self, agent):
        claim = np.array([self.claim_type, self.claim_card, self.claim_quantity])
        agent, guess = make_and_verify_guess(self.__player1_cards,self.__player2_cards,claim,agent)

        return agent, guess

    def judge_bs(self):
        '''
        Judge if claim is right.
        '''
        number_of_claim_card = 0
        for card, suit in self.__player1_cards + self.__player2_cards:
            if self.claim_type == 1:
                if (card == self.claim_card) or (card == 2):
                    number_of_claim_card += 1
            else:
                if (suit == self.claim_card) or (card == 2):
                    number_of_claim_card += 1
            if self.claim_quantity == number_of_claim_card:
                return True
        return False

    def __str__(self):
        return cards_to_str(self.__player1_cards) + cards_to_str(self.__player2_cards)


def play_one_round(agent):
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
            input_claim_type = int(input("Card (1) or Suit(2): "))
        except ValueError:
            print("Invalid value.")
            continue
        else:
            if (input_claim_type == 1) or (input_claim_type == 2):
                new_game.claim_type = input_claim_type
                break
            else:
                print("Invalid value.")

    while True:
        inv_dict = INV_SUITS_DICT
        input_q = "Suit(HEART/CLUB/DIAMOND/SPADE): "
        if new_game.claim_type == 1:
            inv_dict = INV_CARDS_DICT
            input_q = "Card (A23456789JQK): "
        try:
            input_claim_card = input(input_q).upper()
            new_game.claim_card = inv_dict[input_claim_card]
        except KeyError:
            print("Invalid value.")
            continue
        else:
            break

    #ask for claim number
    while True:
        try:
            input_claim_quantity = int(input("Quantity of {}s (1-6): ".format(input_claim_card)))
        except ValueError:
            print("Invalid value.")
            continue
        else:
            if (input_claim_quantity > 6) or (input_claim_quantity <= 0):
                print("Invalid value.")
            else:
                new_game.claim_quantity = input_claim_quantity
                break

    #player 2 judges
    agent, player2_move = new_game.play_bs(agent)
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
