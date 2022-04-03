##1: update rounds
##2: other pages

import pyxel

SCREEN_L = 150
SCREEN_W = 200

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_RULES = 3

class App:
    def __init__(self):
        pyxel.init(SCREEN_L, SCREEN_W, title = "Impression Baby") 
        self.round = 1
        self.scene = SCENE_TITLE #for switching scenes
        #import title page image
        pyxel.load("assets/baby.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.scene == SCENE_TITLE:
            self.update_title_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
        if pyxel.btnp(pyxel.KEY_R):
            self.scene = SCENE_RULES

    def draw(self):
        pyxel.cls(0)
        pyxel.text(60, 4, f"ROUND {self.round}", 13) ##1
        
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()

    def draw_title_scene(self):
        pyxel.text(45, 30, "Impression Baby", pyxel.frame_count % 16)
        pyxel.blt(35, 40, 0, 0, 0, 64, 16)#blt(x, y, img, u, v, w, h, [colkey])
        pyxel.blt(96, 40, 0, 0, 16, 16, 16)
        pyxel.text(40, 90, "- play (enter) -", 13) ##2
        pyxel.text(40, 100, "- rules (R) -", 13) ##2
        pyxel.text(40, 110, "- quit (Q) -", 13) ##2


App()