
import sys, os.path
sys.path.append(os.path.join(sys.path[0], "../.."))

from graphics2d import *

WIDTH = 1250
HEIGHT = 700

class UnoGameUI:

    NAMES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'spielverbot', 'umdrehen', '+2']
    CARDSIZE = (85, 128)
    CARDS = None

    # Defines the maximum space a hidden (computerplayer) hand will take up on screen
    AI_PLAYER_MAX_CARD_SPACE = WIDTH/3-20
    
    # Defines the positions of the played cards and the stack on screen
    PLAYED_CARDS_POSITION = (550, 250)
    STACK_POSITION = (700, 250)
    
    # Defines the screen locations of the player hands
    PLAYER_HAND_POSITIONS = [
        (WIDTH/2, 550), # spieler 0
        (WIDTH/6, 250), # spieler 1
        (WIDTH/2, 10), # spieler 2
        (5*WIDTH/6, 250) # spieler 3        
    ]

    def __init__(self, game_logic):
        #super().__init__(**kwargs)
        self.game_logic = game_logic
        if UnoGameUI.CARDS is None:
            UnoGameUI.CARDS = self._load_card_images()

    @classmethod
    def _load_card_images(cls):
        image = load_image("../../resources/UNO_cards_deck.png")
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

    def display_hidden_hand(self, player):
        """
        Displays the correct number of backfaces for a given player. Cards are squeezed together
        to fit into a given available space
        """
        hand_of_cards = self.game_logic.hand_von_spieler(player)
        ncards = hand_of_cards.wieviele()
        position = UnoGameUI.PLAYER_HAND_POSITIONS[player]
        offset = min(UnoGameUI.AI_PLAYER_MAX_CARD_SPACE / (ncards+1), UnoGameUI.CARDSIZE[0]/2)
        horizontal_space = offset*(ncards+1)
        card_image = UnoGameUI.CARDS["backface"]
        for i in range(ncards):
            draw_surface(card_image, (position[0]-horizontal_space/2+i*offset, position[1]))
        # we should display some text giving the full number of cards

    def display_open_hand(self, player):
        """
        Displays a hand of cards for the given player. Cards are halfway visile
        """
        hand_of_cards = self.game_logic.hand_von_spieler(player)
        ncards = hand_of_cards.wieviele()
        position = UnoGameUI.PLAYER_HAND_POSITIONS[player]
        ncards = hand_of_cards.wieviele()
        horizontal_space = UnoGameUI.CARDSIZE[0]/2*(ncards+1)
        for i, card in enumerate(hand_of_cards.liste_der_karten()):
            image = self.get_card_image(card)
            draw_surface(image, (position[0]-horizontal_space/2+i*UnoGameUI.CARDSIZE[0]/2, position[1]))

    def display_last_played_card(self):
        """
        Displays the card last played
        """
        card = self.game_logic.zuletzt_gespielte_karte()
        draw_surface(self.get_card_image(card),  UnoGameUI.PLAYED_CARDS_POSITION)

    def display_stack(self):
        """
        Displays a card backface which represents the stack of unused cards
        """
        draw_surface(UnoGameUI.CARDS["backface"], UnoGameUI.STACK_POSITION)

    def display_hand_background(self, player, color):
        """
        Displays a rectangular area behind a player's cards
        in a given color
        """
        rect = self.get_player_hand_bounding_rect(player)
        rect.inflate_ip(10, 10)
        draw_filled_rect((rect.x, rect.y), (rect.w, rect.h), color)
           
    
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

    def is_played_card_under_cursor(self, mouse_position):
        """Liefert True, wenn der Mauscursor über der letzten gespielten Karte liegt"""
        rect = Rect(UnoGameUI.PLAYED_CARDS_POSITION, UnoGameUI.CARDSIZE)
        return rect.collidepoint(mouse_position)

    def is_stack_under_cursor(self, mouse_position):
        """Liefert True, wenn der Mauscursor über dem Kartenstapel liegt"""
        rect = Rect(UnoGameUI.STACK_POSITION, UnoGameUI.CARDSIZE)
        return rect.collidepoint(mouse_position)

    def get_card_under_cursor(self, mouse_position):
        """
        Liefert die Karte, die sich unter dem Mauscursor befindet
        """
        if self.is_played_card_under_cursor(mouse_position):
            return self.game_logic.zuletzt_gespielte_karte()
        elif self.is_stack_under_cursor(mouse_position):
            return self.game_logic.stapel.zeige_oberste()
        player = self.get_player_hand_under_cursor(mouse_position)
        if player == -1:
            return None
        hand = self.game_logic.hand_von_spieler(player)
        ncards = hand.wieviele()
        if ncards == 0:
            return None
        if player == 0:
            offset = UnoGameUI.CARDSIZE[0]/2
        else:
            offset = min(UnoGameUI.AI_PLAYER_MAX_CARD_SPACE / (ncards+1), UnoGameUI.CARDSIZE[0]/2)
        horizontal_space = offset*(ncards+1)
        startx = UnoGameUI.PLAYER_HAND_POSITIONS[player][0]-horizontal_space/2
        idx = min(int((mouse_position[0] - startx) / offset), ncards-1)
        return hand.liste_der_karten()[idx]

