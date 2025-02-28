from random import shuffle, sample

class Karte:
    """
    Repräsentiert eine UNO-Karte
    """
    def __init__(self, farbe, symbol):
        self.farbe = farbe
        self.symbol = symbol
        self.wurde_verwendet = False

    def ist_spielbar_auf(self, andere_karte):
        if self.farbe == andere_karte.farbe:
            return True
        if self.symbol == andere_karte.symbol:
            return True

        return False

    def ist_aktives_verbot(self):
        return self.ist_verbot() and not self.wurde_verwendet

    def ist_verbot(self):
        return self.symbol == "spielverbot"

    def ist_umdrehen(self):
        return self.symbol == "umdrehen"

    def ist_plus2(self):
        return self.symbol == "+2"

    def __repr__(self):
        return "Karte " + self.farbe + " " + self.symbol

class Stapel:
    """
    Repräsentiert den UNO-Spielstapel
    """
    def __init__(self, leer=False):
        if leer:
            self.karten = []
        else:
            self._erzeuge_spielkarten()
            self.mische_karten()


    def _erzeuge_spielkarten(self):
        self.karten = []

        for farbe in "rot", "grün", "gelb", "blau":
            for symbol in "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "umdrehen", "+2", "spielverbot":
                for i in range(2):
                    self.karten.append(Karte(farbe, symbol))

        # Wie ergänzen? Was fehlt noch?

    def ist_leer(self):
        return len(self.karten) == 0


    def mische_karten(self):
        shuffle(self.karten)

    def nimm_oberste(self):
        return self.karten.pop()

    def zeige_oberste(self):
        if self.ist_leer():
            return None
        else:
            return self.karten[-1]

    def lege_auf_stapel(self, karte):
        self.karten.append(karte)

class Hand:
    """
    Repräsentiert die Karten, die ein Spieler hält
    """
    def __init__(self):
        self.karten = []

    def __repr__(self):
        r = "Hand [ "
        for karte in self.karten:
            r = r + repr(karte) + " "
        return r + "]"

    def wieviele(self):
        return len(self.karten)

    def nimm(self, karte):
        self.karten.append(karte)

    def gib(self, karte):
        self.karten.remove(karte)

    def spielbare_karten_auf(self, oberste):
        spielbar = []
        for karte in self.karten:
            if karte.ist_spielbar_auf(oberste):
                spielbar.append(karte)
        return spielbar

    def liste_der_karten(self):
        return self.karten

class Spiel:
    """
    Repräsentiert ein vollständiges UNO-Spiel
    """
    def __init__(self):
        self.stapel = Stapel()
        self.spieler = []
        self.gespielt = Stapel(leer=True)
        # Niemand ist am Zug
        self.am_zug = -1
        self.richtung = 1


    def beginne_neues_spiel(self, anzahl_spieler):
        self.stapel = Stapel()
        self.spieler = []
        for i in range(anzahl_spieler):
            self.spieler.append(Hand())
        # Erster Spieler ist am Zug
        self.am_zug = 0
        self.richtung = 1
        # Verteile Karten an alle Spieler
        for spieler in self.spieler:
            for i in range(7):
                spieler.nimm(self.stapel.nimm_oberste())
        # Oberste Karte vom Stapel nehmen und ausspielen
        self.gespielt.lege_auf_stapel(self.stapel.nimm_oberste())

    def hand_von_spieler(self, n):
        return self.spieler[n]

    def anzahl_der_spieler(self):
        return len(self.spieler)

    def zuletzt_gespielte_karte(self):
        return self.gespielt.zeige_oberste()

    def karte_wird_gespielt(self, karte):
        self.gespielt.lege_auf_stapel(karte)

    def ist_am_zug(self, spieler):
        if spieler == -1:
            return False
        else:
            return spieler == self.am_zug
    
    def nimm_karte_auf(self):
        return self.stapel.nimm_oberste()
        
    
    def mache_zug(self):
        oberste = self.gespielt.zeige_oberste()
        hand = self.spieler[self.am_zug]

        if oberste.ist_verbot():
            if not oberste.wurde_verwendet:
                oberste.wurde_verwendet = True
                self.weiter_zur_nächsten_person()
                return

        if oberste.ist_plus2():
            if not oberste.wurde_verwendet:
                oberste.wurde_verwendet = True
                hand.nimm(self.stapel.nimm_oberste())
                hand.nimm(self.stapel.nimm_oberste())
                print("Spieler", self.am_zug, "nimmt 2 Karten auf.")
        for i in range(2):
            spielbare_karten = hand.spielbare_karten_auf(oberste)
            if len(spielbare_karten) > 0:
                gespielte_karte = sample(spielbare_karten, 1)[0]
                hand.gib(gespielte_karte)
                self.gespielt.lege_auf_stapel(gespielte_karte)
                if gespielte_karte.ist_umdrehen():
                    # wechselt von 1 auf -1 oder von -1 auf 1
                    self.richtung = 0 - self.richtung
                print("Spieler", self.am_zug, "spielt", gespielte_karte)
                break
            elif i == 0:
                hand.nimm(self.stapel.nimm_oberste())
                print("Spieler", self.am_zug, "nimmt Karte auf.")

        self.weiter_zur_nächsten_person()


    def weiter_zur_nächsten_person(self):
        self.am_zug = self.am_zug + self.richtung
        if self.am_zug >= len(self.spieler):
            self.am_zug = 0
        if self.am_zug < 0:
            self.am_zug = len(self.spieler)-1










