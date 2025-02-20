
import sys, os.path
sys.path.append(os.path.join(sys.path[0], "../.."))

from graphics2d import *
from unospiel_logik import *

uno_game_ui = None
uno_game = None

WIDTH = 1250
HEIGHT = 700


class UnoGameUI:

    NAMES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'spielverbot', 'umdrehen', '+2']
    CARDSIZE = (85, 128)
    CARDS = None

    AI_PLAYER_MAX_CARD_SPACE = WIDTH/3-20

    PLAYER_HAND_POSITIONS = [
        (WIDTH/2, 550), # spieler 0
        (WIDTH/6, 250), # spieler 1
        (5*WIDTH/6, 250), # spieler 2
        (WIDTH/2, 10) # spieler 3
    ]

    def __init__(self, game_logic):
        #super().__init__(**kwargs)
        self.game_logic = game_logic
        if UnoGameUI.CARDS is None:
            UnoGameUI.CARDS = self._load_card_images()

    @classmethod
    def _load_card_images(cls):
        image = load_image("resources/UNO_cards_deck.png")
        cardsize = UnoGameUI.CARDSIZE
        cards = {}
        for y, color in enumerate(['rot', 'gelb', 'grün', 'blau']):
            for x in range(13):
                r = Rect(x*cardsize[0], y*cardsize[1], cardsize[0], cardsize[1])
                name = UnoGameUI.NAMES[x] + "-" + color
                cards[name] = image.subsurface(r)
        cards["PC"] = image.subsurface(Rect(13*cardsize[0], 0, cardsize[0], cardsize[1]))
        cards["+4"] = image.subsurface(Rect(13*cardsize[0], 4*cardsize[1], cardsize[0], cardsize[1]))
        cards["backface"] = image.subsurface(Rect(0, 7*cardsize[1], cardsize[0], cardsize[1]))
        return cards

    def get_card_image(self, card):
        name = card.symbol + "-" + card.farbe
        return UnoGameUI.CARDS[name]

    def display_hidden_hand(self, hand_of_cards, position):
        ncards = hand_of_cards.wieviele()
        offset = min(UnoGameUI.AI_PLAYER_MAX_CARD_SPACE / (ncards+1), UnoGameUI.CARDSIZE[0]/2)
        horizontal_space = offset*(ncards+1)
        card_image = UnoGameUI.CARDS["backface"]
        for i in range(ncards):
            draw_surface(card_image, (position[0]-horizontal_space/2+i*offset, position[1]))
        # we should display some text giving the full number of cards

    def display_open_hand(self, hand_of_cards, position):
        ncards = hand_of_cards.wieviele()
        horizontal_space = UnoGameUI.CARDSIZE[0]/2*(ncards+1)
        for i, card in enumerate(hand_of_cards.liste_der_karten()):
            image = self.get_card_image(card)
            draw_surface(image, (position[0]-horizontal_space/2+i*UnoGameUI.CARDSIZE[0]/2, position[1]))

    def get_player_hand_bounding_rect(self, player):
        """
        Returns the bounding rectangle for the given player's visual cards display area
        """
        ncards = self.game_logic.hand_von_spieler(player).wieviele()
        if player == 0:
            horizontal_space = UnoGameUI.CARDSIZE[0]/2*(ncards+1)
        else:
            offset = min(UnoGameUI.AI_PLAYER_MAX_CARD_SPACE / (ncards+1), UnoGameUI.CARDSIZE[0]/2)
            horizontal_space = offset*(ncards+1)
        return Rect(UnoGameUI.PLAYER_HAND_POSITIONS[player][0]-horizontal_space/2,
                    UnoGameUI.PLAYER_HAND_POSITIONS[player][1],
                    horizontal_space,
                    UnoGameUI.CARDSIZE[1])


    def get_player_hand_under_cursor(self, mouse_position):
        """
        Returns the index of the player the mouse hovers over, or
        -1 if the mouse is not above a player hand
        """
        for i in range(4):
            rect = self.get_player_hand_bounding_rect(i)
            if rect.collidepoint(mouse_position):
                return i
        return -1

    def get_card_under_cursor(self, mouse_position):
        player = self.get_player_hand_under_cursor(mouse_position)
        if player == -1:
            return None
        hand = self.game_logic.hand_von_spieler(player)
        ncards = hand.wieviele()
        if player == 0:
            offset = UnoGameUI.CARDSIZE[0]/2
        else:
            offset = min(UnoGameUI.AI_PLAYER_MAX_CARD_SPACE / (ncards+1), UnoGameUI.CARDSIZE[0]/2)
        horizontal_space = offset*(ncards+1)
        startx = UnoGameUI.PLAYER_HAND_POSITIONS[player][0]-horizontal_space/2
        idx = min(int((mouse_position[0] - startx) / offset), ncards-1)
        return hand.liste_der_karten()[idx]



def on_input(event):
    if event.type == MOUSEMOTION:
        mouse_coords = event.pos
        player = uno_game_ui.get_player_hand_under_cursor(mouse_coords)
        if player != -1:
            print(uno_game_ui.get_card_under_cursor(mouse_coords))

def on_draw():

    draw_filled_rect((0, 0), get_window_size(), BLACK)

    # zuletzt gespielte karte
    oberste = uno_game.zuletzt_gespielte_karte()
    draw_surface(uno_game_ui.get_card_image(oberste),  (550, 250))

    # kartenstapel zum aufnehmen
    draw_surface(uno_game_ui.CARDS["backface"], (700, 250))

    for i in range(uno_game.anzahl_der_spieler()):
        karten = uno_game.hand_von_spieler(i)
        pos = uno_game_ui.PLAYER_HAND_POSITIONS[i]
        if i == 0:
            uno_game_ui.display_open_hand(karten, pos)
        else:
            uno_game_ui.display_hidden_hand(karten, pos)

def on_ready():
    global uno_game_ui, uno_game
    set_window_title("Demo 5 - UNO")
    uno_game = Spiel()
    uno_game.beginne_neues_spiel(4)
    uno_game_ui = UnoGameUI(uno_game)


go()