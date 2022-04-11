##3: update play scene
# click 1 or 2 changes the claim type and screen display

import pyxel
from BS_Poker import BSGame
from textwrap import wrap
import util
from util import CARDS, CARDS_DICT, INV_CARDS_DICT, SUITS, SUITS_DICT, INV_SUITS_DICT
from nn import Baby, make_and_verify_guess # :)

SCREEN_W = 150
SCREEN_L = 200

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_RULES = 3


SUIT_POSITIONS = {0: (32, 16), 1:(40, 16), 2:(32, 24), 3:(40, 24)} #0: 'HEART', 1: 'CLUB', 2:'DIAMOND', 3:'SPADE'

MARGIN = 15


RULES = "2 players: You and Baby. Each player draws 3 cards from the deck. \
You guess what's in the 6 cards. Baby claims it is true or false. \
If Baby judges correctly, it wins. If not you win."
RULES = wrap(RULES, 34)

#util
def print_paragraph(par, start_y, n):
    '''
    Prints paragraph line by line on screen

    par(list): paragraph to be printed
    start_y(int): start y position of text
    n(1-13): color of text 
    '''
    for line in par:
        pyxel.text(10, start_y, line, n) 
        start_y += 10
    return start_y


class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_L, title = "Impression Baby") 
        self.round = 1
        self.status = 0 #0: player win, 1:player lost ##3
        self.player1_score = 0 #you
        self.player2_score = 0 #baby
        self.scene = SCENE_TITLE #for switching scenes
        self.bsgame = BSGame()
        self.bsgame.deal(3)
        #click
        pyxel.mouse(True)
        #import title page image
        pyxel.load("assets/poker_vectors.pyxres")
        pyxel.run(self.update, self.draw)
        #initialize agent
        baby_object = Baby()
        model = baby_object.build_model()
        agent = baby_object.build_agent()
        agent.compile(Adam(lr=1e-3), metrics=['mae']) #mean absolute error

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()
        elif self.scene == SCENE_RULES:
            self.update_rules_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
        if pyxel.btnp(pyxel.KEY_R):
            self.scene = SCENE_RULES

    def update_play_scene(self):
        #claim type
        #once cliamed, can't change
        if not self.bsgame.claim_type:
            if pyxel.btnp(pyxel.KEY_1):
                self.bsgame.claim_type = 1
            if pyxel.btnp(pyxel.KEY_2):
                self.bsgame.claim_type = 2

        #claiming cards
        if self.bsgame.claim_type and (not self.bsgame.claim_card):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.bsgame.claim_type == 1:
                    if (pyxel.mouse_y > 100) & (pyxel.mouse_y < 110) & (pyxel.mouse_x > MARGIN) & (pyxel.mouse_x < (MARGIN + 130)) :
                        self.bsgame.claim_card = int((pyxel.mouse_x - MARGIN)/10) + 1 ###
                if self.bsgame.claim_type == 2:
                    if (pyxel.mouse_y > 100) & (pyxel.mouse_y < 110) & (pyxel.mouse_x > MARGIN) & (pyxel.mouse_x < (MARGIN + 40)):
                        self.bsgame.claim_card = int((pyxel.mouse_x - MARGIN)/10) + 1 ###

        #claim quantity
        if self.bsgame.claim_card:
            if pyxel.btnp(pyxel.KEY_1):
                self.bsgame.claim_quantity = 1
            if pyxel.btnp(pyxel.KEY_2):
                self.bsgame.claim_quantity = 2
            if pyxel.btnp(pyxel.KEY_3):
                self.bsgame.claim_quantity = 3
            if pyxel.btnp(pyxel.KEY_4):
                self.bsgame.claim_quantity = 4
            if pyxel.btnp(pyxel.KEY_5):
                self.bsgame.claim_quantity = 5
            if pyxel.btnp(pyxel.KEY_6):
                self.bsgame.claim_quantity = 6

        ##3

    def update_gameover_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
            self.cards = Cards(3)
            self.round += 1


    def update_rules_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY


    def draw(self):
        pyxel.cls(0)
        
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        elif self.scene == SCENE_RULES:
            self.draw_rules_scene()


    def draw_cards(self, x, y, player_n):
        '''
        Draws the 3 cards of player 1 or 2 on screen
        '''
        if player_n == 1:
            hand = self.bsgame.get_player1_hands()
        elif player_n == 2:
            hand = self.bsgame.get_player2_hands()

        for p_card in hand:
            suit_coords = SUIT_POSITIONS[p_card[1]]
            card_val = (CARDS_DICT[p_card[0]])
            pyxel.blt(x, y, 0, 16, 16, 16, 16)
            pyxel.blt(x + 3, y + 2, 0, suit_coords[0], suit_coords[1], 6, 6) #card suit 
            #card number
            i = 2
            if card_val == '10':
                i = 0
            pyxel.text(x + 8 + i, y + 8, card_val, 7) 
            x += 20


    def draw_buttons(self, y, d):
        if self.bsgame.claim_type == 1:
            for i, n in enumerate(CARDS_DICT.values()):
                pyxel.blt(MARGIN + i*d, y, 0, 4, 20, 8, 8) #button
                pyxel.text(MARGIN + i*d + 2, y+1, n, 7) #button
        elif self.bsgame.claim_type == 2:
            for k, v in SUIT_POSITIONS.items():
                pyxel.blt(MARGIN + k*d, y, 0, 4, 20, 8, 8) #button
                pyxel.blt(MARGIN + k*d + 1, y + 1, 0, v[0], v[1], 6, 6) #button


    def draw_title_scene(self):
        pyxel.text(45, 30, "Impression Baby", pyxel.frame_count % 16)
        #graphics
        pyxel.blt(35, 40, 0, 0, 0, 80, 16)
        #text
        pyxel.text(40, 90, "- play (enter) -", 13) ##2
        pyxel.text(40, 100, "- rules (R) -", 13) ##2
        pyxel.text(40, 110, "- quit (Q) -", 13) ##2


    def draw_play_scene(self):

        pyxel.text(60, 4, f"ROUND {self.round}", 13) 
        pyxel.text(SCREEN_W-15, 4, '{}:{}'.format(self.player1_score, self.player2_score), 13) ##1
        pyxel.text(MARGIN, 30, "Your hand:", 7) 
        pyxel.text(MARGIN, 40, util.cards_to_str(self.bsgame.get_player1_hands()), 3) 

        self.draw_cards(80, 40, player_n = 1)

        pyxel.text(MARGIN, 70, "Enter your claim", 7) 
        pyxel.text(MARGIN, 80, "Card (1) or Suit(2): ", 13) ##2
        #claim type
        if self.bsgame.claim_type == 1:
            pyxel.text(MARGIN, 90, "Choose card: ", 13) 
            self.draw_buttons(100, 10)
        elif self.bsgame.claim_type == 2:
            pyxel.text(MARGIN, 90, "Choose suit: ", 13)
            self.draw_buttons(100, 10)
        #claim card
        if self.bsgame.claim_card:
            if self.bsgame.claim_type == 1:
                pyxel.text(MARGIN, 115, "Claimed card:", 13) 
                pyxel.text(MARGIN + 70, 115, CARDS_DICT[self.bsgame.claim_card], 3)
            if self.bsgame.claim_type == 2:
                pyxel.text(MARGIN, 115, "Claimed card:", 13)
                pyxel.text(MARGIN + 60, 115, SUITS_DICT[self.bsgame.claim_card], 3)
            pyxel.text(MARGIN, 125, "Claim quantity (1-6):", 13)
            if self.bsgame.claim_quantity:
                pyxel.text(MARGIN + 90, 125, str(self.bsgame.claim_quantity), 3) ###


    def draw_gameover_scene(self):
        pyxel.text(50, 66, "GAME OVER", 8) 
        txt = "YOU WON!"
        if self.status == 1:
            txt = "YOU LOST!"
        pyxel.text(50, 76, txt, 8) 
        pyxel.text(31, 126, "- Press return to replay -", 13)
        self.round += 1 ##1

    def draw_rules_scene(self):
        pyxel.text(54, 20, "* RULES *", 7) 
        end_y = print_paragraph(RULES, 30, 7)
        pyxel.text(43, end_y + 20, "- press enter -", 13) 


App()



