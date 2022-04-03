CARDS = list(range(1, 14)) 
CARDS_DICT = {1:'A', 2:'2', 3:'3', 4:'4', 5:'5', 6: '6', 7: '7', 8: '8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K'}
INV_CARDS_DICT = {v: k for k, v in CARDS_DICT.items()}

SUITS = list(range(3)) 
SUITS_DICT = {0: 'HEART', 1: 'CLUB', 2:'DIAMOND', 3:'SPADE'}
INV_SUITS_DICT = {v: k for k, v in SUITS_DICT.items()}

def cards_to_str(cards):
    '''
    String of cards in tuple
    '''
    s = ''
    for card, suit in cards:
        s += '{} of {}'.format(CARDS_DICT[card], SUITS_DICT[suit]) + '\n'
    return s