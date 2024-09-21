from random import randint
from Model.Constantes import *
from Model.Joueur import *
from Model.Plateau import *


def __construirePion(color: int) -> dict:
    print("Fonction construirePion manquante !")
    return None

def __construireJoueur(color: int) -> dict:
    print("Fonction construireJoueur manquante !")
    return None


def __construirePlateau() -> dict:
    print("Fonction construirePlateau manquante !")
    return None


def __setPlateauJoueur(j: dict, p: dict) -> None:
    print("Fonction setPlateauJoueur manquante !")
    return None


def __initialiserIAJoueur(j: dict, extended: bool) -> None:
    print("Fonction initialiserIAJoueur manquante !")
    return None


def __getPlacerPionJoueur(j: dict) -> callable:
    print("Fonction getPlacerPionJoueur manquante !")
    return None


def __getCouleurJoueur(j: dict) -> int:
    print("Fonction getCouleurJoueur manquante  !")
    return const.JAUNE


def __getPionJoueur(j: dict) -> dict:
    print("Fonction getPionJoueur manquante !")
    return None


def __placerPionPlateau(plateau: dict, pion: dict, column: int) -> int:
    print("Fonction placerPionPlateau manquante !")
    return const.NB_LINES - 1


def __getPionsGagnantsPlateau(p: dict) -> list:
    print("Fonction getPionsGagnantsPlateau manquante !")
    return None


def __getCouleurPion(pion: dict) -> int:
    print("Fonction getCouleurPion manquante !")
    return const.JAUNE


def __isRempliPlateau(plateau: dict) -> bool:
    print("Fonction isRempliPlateau manquante !")
    return False


def __getIdPion(pion: dict) -> int:
    print("Fonction getIdPion manquante ! ** RISQUE DE PLANTAGE !!! **")
    return 0

def __setIdPion(pion: dict, id: int) -> None:
    print("Fonction setIdPion manquante ! ** RISQUE DE PLANTAGE !!! **")
    return None

def __placerPionLignePlateau(p: dict, pion: dict, line: int, left: bool) -> tuple:
    print("Fonction placerPionLignePlateau manquante ! ** RISQUE DE PLANTAGE !!! **")
    return [], None

def __isPatPlateau(p: list, histo: dict) -> bool:
    print("Fonction isPatPlateau manquante !")
    return False


def __setModeEtenduJoueur(j: dict, mode: bool) -> None:
    print("Fonction setModeEtenduJoueur manquante ! ** POSE PROBLEME SI VOUS ACTIVEZ LE MODE ETENDU !!! **")
    return None



def load_function(name: str) -> callable:
    if name in globals():
        return globals()[name]
    name = '__' + name
    if name not in globals():
        print(f"Implementation Error : {name} not defined")
        raise ModuleNotFoundError(name)
    return globals()[name]


class Controller:

    def __init__(self):
        self.win = None
        # self.demineur = construireGrilleDemineur(lines, columns) if "construireGrilleDemineur" in globals() else None

        # Récupération des méthodes existantes
        # et remplacement par des méthodes par défaut si non existantes
        self.construirePion = load_function("construirePion")
        self.construireJoueur = load_function("construireJoueur")
        self.construirePlateau = load_function("construirePlateau")
        self.setPlateauJoueur = load_function("setPlateauJoueur")
        self.initialiserIAJoueur = load_function("initialiserIAJoueur")
        self.getPlacerPionJoueur = load_function("getPlacerPionJoueur")
        self.getCouleurJoueur = load_function("getCouleurJoueur")
        self.getPionJoueur = load_function("getPionJoueur")
        self.placerPionPlateau = load_function("placerPionPlateau")
        self.getPionsGagnantsPlateau = load_function("getPionsGagnantsPlateau")
        self.getCouleurPion = load_function("getCouleurPion")
        self.isRempliPlateau = load_function("isRempliPlateau")
        self.getIdPion = load_function("getIdPion")
        self.setIdPion = load_function("setIdPion")
        self.placerPionLignePlateau = load_function("placerPionLignePlateau")
        self.isPatPlateau = load_function("isPatPlateau")
        self.setModeEtenduJoueur = load_function("setModeEtenduJoueur")

        self.players = []
        self.plateau = self.construirePlateau()
        self.current_player = 0
        self.histo_plateau = {}

    def set_win(self, win: object) -> None:
        self.win = win
        return None

    def set_first_player(self, human: bool) -> None:
        self.players.append(self.construireJoueur(const.JAUNE))
        self.setPlateauJoueur(self.players[0], self.plateau)
        if self.win.extended_mode:
            self.setModeEtenduJoueur(self.players[0], True)
        if not human:
            self.initialiserIAJoueur(self.players[0], True)

    def set_second_player(self, human: bool) -> None:
        self.players.append(self.construireJoueur(const.ROUGE))
        self.setPlateauJoueur(self.players[1], self.plateau)
        if self.win.extended_mode:
            self.setModeEtenduJoueur(self.players[1], True)
        if not human:
            self.initialiserIAJoueur(self.players[1], False)
        return None

    def get_current_color(self) -> int:
        return self.getCouleurJoueur(self.players[self.current_player])

    def __get_adversaire(self):
        return self.players[(self.current_player + 1)%2]

    def __jeu_adversaire(self, move: int):
        player = self.__get_adversaire()
        if player is not None and const.JEU_ADVERSAIRE in player:
            player[const.JEU_ADVERSAIRE](player, move)

    def play(self):
        fn = self.getPlacerPionJoueur(self.players[self.current_player])
        # print(self.players[self.current_player])
        if fn is None:
            self.win.human_play()
        else:
            col = fn(self.players[self.current_player])
            self.win.anime_play(col)
        return None

    def human_has_played(self, col: int) -> None:
        self.__jeu_adversaire(col)

    def drop_on(self, column: int, id_piece: int) -> int:
        pion = self.getPionJoueur(self.players[self.current_player])
        self.setIdPion(pion, id_piece)
        return self.placerPionPlateau(self.plateau, pion, column)

    def drop_on_line(self, line: int, left: bool, id_piece: int) -> tuple:
        # print(f"Pushing : line = {line}, left={left}")
        # print(toStringPlateau(self.plateau))
        pion = self.getPionJoueur(self.players[self.current_player])
        self.setIdPion(pion, id_piece)
        lst, line_down = self.placerPionLignePlateau(self.plateau, pion, line, left)
        lst = [p[const.ID] for p in lst]
        # print("drop_on_line : IDs = ", lst, ", line = ", line)
        # print(toStringPlateau(self.plateau))
        return lst, line_down

    def next(self):
        self.current_player = (self.current_player + 1) % 2

    def get_winner(self):
        return self.getPionsGagnantsPlateau(self.plateau)

    def get_piece_color(self, pion: dict) -> int:
        return self.getCouleurPion(pion)

    def is_game_pat(self, extended: bool):
        # Cette fonction  est appelée à chaque fin de coups
        return not extended and self.isRempliPlateau(self.plateau)\
               or extended and self.isPatPlateau(self.plateau, self.histo_plateau)

    def get_piece_id(self, pion: dict) -> int:
        return self.getIdPion(pion)
