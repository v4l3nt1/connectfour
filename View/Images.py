import pygame
import numpy as np
from Model.Constantes import *

# Partie chargement des images
# Récupération des noms des cellules du démineur
# ==============================================
# Nom des images brutes


class Images:
    # Image de fond de l'écran
    img_background = None
    # Liste de 2 images pour les pions (jaune, rouge)
    img_pieces = None
    # Liste de 2 images pour les mains déposant les pions (main venant de la gauche, main venant de la droite)
    img_hands = None
    # Image représentant le tableau de 6 rangées et 7 colonnes
    img_board = None
    # Répertoire où se trouvent les images
    sources = 'Images/'

    # Largeur de la fenêtre
    w_width = 0
    # Hauteur de la fenêtre
    w_height = 0

    #---------------------------
    #  Position du tableau
    # Point supérieur gauche
    #---------------------------
    x_board = 0
    y_board = 0

    #---------------------------
    # Position des pions
    # sur la grille
    #---------------------------
    x_piece = None
    y_piece = None

    # Position des mains
    x_hands = None
    y_hands = None
    # Position du pion par rapport à la main
    x_hand_offset = None
    y_hand_offset = None

    # Position des mains après rotation sur les bords gauches et droits
    rotated_hands_position = None


    @staticmethod
    def load_images():
        # Chargement des images et vérification...
        # ----------------------------------------
        Images.img_background = pygame.image.load(Images.sources + 'fond-2.png')
        Images.img_pieces = [pygame.image.load(Images.sources + img) for img in ['pion-jaune-2.png', 'pion-rouge-2.png']]
        Images.img_hands = [pygame.image.load(Images.sources + img) for img in ['dropping-hand-left.png', 'dropping-hand-right.png']]
        Images.img_board = pygame.image.load(Images.sources + 'plateau-puissance4-2.png')

        # TODO : il faudra convertir (convert_alpha) une fois que la fenêtre sera créée...
        # Taille de la fenêtre
        Images.w_width, Images.w_height = Images.img_background.get_width(), Images.img_background.get_height()

        # Calcul de la position de la grille centrée sur la fenêtre en largeur
        _w, _h = Images.img_board.get_width(), Images.img_board.get_height()
        Images.x_board = (Images.w_width - _w) // 2
        Images.y_board = Images.w_height - _h

        # Estimation de la position des pions sur la grille
        # en fonction de leur taille
        _wp, _hp = Images.img_pieces[0].get_width(), Images.img_pieces[0].get_height()
        # Estimation de la taille des bords des pions _m, du bord vertical _bv, et du bord horizontal _bh
        # ... voir documentation.txt
        _bv = (_h - 6 * _hp) % 6
        _mv = (_h - 6 * _hp - _bv) / 6 - 1
        _bh = (_w - 7 * _wp) % 7
        _mh = (_w - 7 * _wp - _bh) / 7 - 1.5
        # Calcul des positions des pions
        # Images.x_piece = [Images.x_board + int(x + 0.5) for x in np.arange(_bh + _mh + 1, _w, _wp + _mh)]
        # Pour la hauteur : la ligne -1 est celle au-dessus de la grille et la ligne de la grille commence au
        # numéro 0
        # Images.y_piece = [Images.y_board + int(y + 0.5) for y in np.arange(_mv/2, _h, _hp + _mv)]
        Images.x_piece = dict([(i, Images.x_board + int(x + 0.5)) for i, x in enumerate(np.arange(_bh + _mh + 1, _w, _wp + _mh))])
        Images.y_piece = dict([(i, Images.y_board + int(y + 0.5)) for i, y in enumerate(np.arange(_mv/2, _h, _hp + _mv))])
        # print("Y des pièces :", Images.y_piece)
        # Calcul de la position de la pièce à gauche de la grille
        # pour pouvoir pousser les pions sur la gauche
        Images.x_piece[-1] = 2*Images.x_piece[0] - Images.x_piece[1] - 10
        # Calcul de la position de la pièce à droite de la grille
        # pour pouvoir pousser les pions sur la droite de la grille
        idx = len(Images.x_piece) - 1
        Images.x_piece[idx] = 2*Images.x_piece[idx - 1] - Images.x_piece[idx - 2] + 10
        # print("X des pièces :", Images.x_piece)

        # estimation de la position des mains
        # Position estimée du pion dans la main gauche : 164, 110
        # Estimation de la position du pion dans la main droite
        _w, _h = Images.img_hands[0].get_width(), Images.img_hands[0].get_height()
        Images.x_hand_offset = [164, _w - 164 - _wp]
        Images.y_hand_offset = 110
        # Position en hauteur des mains (c'est la même pour la main gauche et pour la main droite)
        Images.y_hands = (Images.img_background.get_height() - Images.img_board.get_height() - _h) // 2 - 20
        Images.y_piece[-1] = Images.y_hands + Images.y_hand_offset
        # Position des mains par rapport aux colonnes de la grille
        # [0] : Main gauche
        # [1] : Main droite
        # Images.x_hands = [
        #     [Images.x_piece[i] - Images.x_hand_offset[0] for i in range(7)],
        #     [Images.x_piece[i] - Images.x_hand_offset[1] for i in range(7)],
        # ]
        # Problème : A gauche et à droite, il y a deux positions possibles.
        # Celle avec la main normale, celle avec la main après rotation !
        Images.x_hands = [
            dict([(i, Images.x_piece[i] - Images.x_hand_offset[0]) for i in Images.x_piece.keys()]),
            dict([(i, Images.x_piece[i] - Images.x_hand_offset[1]) for i in Images.x_piece.keys()]),
        ]
        # Position de la main gauche à gauche après rotation : (91, 56)
        Images.rotated_hands_position = [
            {(-1, -1): (91, 56), (-1, const.NB_COLUMNS): (806, -72)},
            {(-1, -1): (91, -72), (-1, const.NB_COLUMNS): (806, 56)},
        ]
        # Calcul des autres positions en fonction des pièces
        for c in range(0,2):
            for col in [-1, const.NB_COLUMNS]:
                for line in range(0, const.NB_LINES):
                    pos = Images.rotated_hands_position[c][(line - 1, col)]
                    _delta_y = Images.y_piece[line] - Images.y_piece[line - 1]
                    pos = (pos[0], pos[1] + _delta_y)
                    Images.rotated_hands_position[c][line, col] = pos

    @staticmethod
    def get_window_size() -> tuple:
        return Images.w_width, Images.w_height

    @staticmethod
    def get_board_coordinates() -> tuple:
        return Images.x_board, Images.y_board

    @staticmethod
    def get_piece_coordinates(line: int, column: int) -> tuple:
        return Images.x_piece[column], Images.y_piece[line]

    @staticmethod
    def get_piece_width() -> int:
        return Images.img_pieces[0].get_width()

    @staticmethod
    def get_piece_height() -> int:
        return Images.img_pieces[0].get_height()

    @staticmethod
    def get_hand_coordinates(color: int, column: int) -> tuple:
        return Images.x_hands[color][column], Images.y_hands

    @staticmethod
    def get_hand_width() -> int:
        return Images.img_hands[0].get_width()

    @staticmethod
    def get_hand_height() -> int:
        return Images.img_hands[0].get_height()
