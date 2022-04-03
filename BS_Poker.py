import random


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
    def __init__(self):
        self.deck = [(card, suit) for card in cards for suit in suits]
        self.__player1_cards = None
        self.__player2_cards = None

    def draw_from_deck_wo_replacement(self, n):
        newdeck = []
        for i in range(n):
            index = random.randint(0, len(self.deck)-1)
            card = self.deck[index]
            self.deck.pop(index)
            newdeck.append(card)
        return newdeck

    def deal(self, n):
        self.__player1_cards = self.draw_from_deck_wo_replacement(n)
        self.__player2_cards = self.draw_from_deck_wo_replacement(n)

    def show_player1_hands(self):
        print(cards_to_str(self.__player1_cards))

    def play_bs(self, claim_card, claim_quantity):
        '''
        Strategy for guessing True or False.
        '''
        # n_i_have = 
        # possibility = 
        if claim_quantity > 2:
            return False
        else:
            return True


    def judge_bs(self, claim_card, claim_quantity):
        '''
        Judge if claim is right.
        '''
        number_of_claim_card = 0
        for card, suit in self.__player1_cards + self.__player2_cards:
            if (card == claim_card) or (card == 2):
                number_of_claim_card += 1
                if claim_quantity == number_of_claim_card:
                    return True
        return False

    def __str__(self):
        return cards_to_str(self.__player1_cards) + cards_to_str(self.__player2_cards)


def main():
    print("\nLet's play BS Poker!\n")
    new_cards = Cards()
    new_cards.deal(3)
    print("Your hand:")
    new_cards.show_player1_hands()

    #multi-round
    # while True:
    #     bs = input('Guess hand (0) or bullshit (1)?')
    #     if bs:
    #         break
    #     else:
    #         claim_card = input("Enter your claim (A23456789JQK):")
    #         claim_quantity = input("Quantity of {}s (1-6):".format(claim_card))

    #single round
    print('Enter your claim')
    #ask for claim card
    while True:
        try:
            claim_card = inv_cards_dict[input("Card (A23456789JQK): ").upper()]
        except KeyError:
            print("Invalid value.")
            continue
        else:
            break
    #ask for claim number
    while True:
        try:
            claim_quantity = int(input("Quantity of {}s (1-6): ".format(claim_card)))
        except ValueError:
            print("Invalid value.")
            continue
        else:
            if (claim_quantity > 6) or (claim_quantity <= 0):
                print("Invalid value.")
            else:
                break

    #player 2 judges
    player2_move = new_cards.play_bs(claim_card, claim_quantity)
    print('\nPlayer 2 thinks its', str(player2_move))

    #show hands
    print('\nShow all cards:')
    print(new_cards)

    #result
    result = new_cards.judge_bs(claim_card, claim_quantity)
    if result == player2_move:
        print('\nPlayer 2 wins {} points!'.format(7 - claim_quantity))
    else:
        print('\nPlayer 1 wins {} points!'.format(claim_quantity))
    print('\n\n')



if __name__ == "__main__":
    main()


