
import sys, os.path
sys.path.append(os.path.join(sys.path[0], "../.."))

from graphics2d import *
from unospiel_logik import *
from uno_gameui import UnoGameUI

uno_game_ui = None
uno_game = None

time_passed = 0
card_under_cursor = None

WIDTH = 1250
HEIGHT = 700


def on_input(event):
    global card_under_cursor
    
    if event.type == MOUSEMOTION:        
        player = uno_game_ui.get_player_hand_under_cursor(event.pos)
        if player != -1:
            card_under_cursor = uno_game_ui.get_card_under_cursor(event.pos)
        elif uno_game_ui.is_played_card_under_cursor(event.pos):
            card_under_cursor = uno_game_ui.get_card_under_cursor(event.pos)
        elif uno_game_ui.is_stack_under_cursor(event.pos):
            card_under_cursor = uno_game_ui.get_card_under_cursor(event.pos)
        else:
            card_under_cursor = None
    
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        player = uno_game_ui.get_player_hand_under_cursor(event.pos)
        if uno_game.ist_am_zug(player):
            if player == 0:
                mache_spielerzug(player)
            else:
                mache_computerzug(player)



def on_draw():
    draw_filled_rect((0, 0), get_window_size(), BLACK)

    # zuletzt gespielte karte
    uno_game_ui.display_last_played_card()
    
    # kartenstapel zum aufnehmen
    uno_game_ui.display_stack()

    for nr in range(uno_game.anzahl_der_spieler()):
        if uno_game.ist_am_zug(nr):
            color = BLUE
        else:
            color = BLACK
        uno_game_ui.display_hand_background(nr, color)
        if nr == 0:            
            uno_game_ui.display_open_hand(nr)
        else:            
            uno_game_ui.display_hidden_hand(nr)

def on_update(deltat):
    global time_passed
    if not uno_game.ist_am_zug(0):
        time_passed += deltat
    if time_passed > 2000:
        # computerspieler spielen nach 2 Sekunden automatisch
        uno_game.mache_zug()
        time_passed = 0

def on_ready():
    global uno_game_ui, uno_game
    set_window_title("Demo 5 - UNO")
    uno_game = Spiel()
    uno_game.beginne_neues_spiel(4)
    uno_game_ui = UnoGameUI(uno_game)

def mache_spielerzug(spieler):
    """
    Sorgt dafür, dass die Karte gespielt wird, auf die der Spieler geklickt hat
    """    
    uno_game.mache_zug()
    
def mache_computerzug(spieler):
    """
    Sorgt dafür, dass der angegebene Computerspieler eine Karte spielt (oder,
    falls er nicht kann, aufnimmt
    """    
    uno_game.mache_zug()
    


go()
print(__file__)