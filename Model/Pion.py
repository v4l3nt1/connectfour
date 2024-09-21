# Model/Pion.py

from Model.Constantes import *

#
# Ce fichier implémente les données/fonctions concernant le pion
# dans le jeu du Puissance 4
#
# Un pion est caractérisé par :
# - sa couleur (const.ROUGE ou const.JAUNE)
# - un identifiant de type int (pour l'interface graphique)
#
# L'identifiant sera initialisé par défaut à None
#

def type_pion(pion: dict) -> bool:
    """
    Détermine si le paramètre peut être ou non un Pion

    :param pion: Paramètre dont on veut savoir si c'est un Pion ou non
    :return: True si le paramètre correspond à un Pion, False sinon.
    """
    return type(pion) == dict and len(pion) == 2 and const.COULEUR in pion.keys() \
        and const.ID in pion.keys() \
        and pion[const.COULEUR] in const.COULEURS \
        and (pion[const.ID] is None or type(pion[const.ID]) == int)


def construirePion(color : int) -> dict :
    """
    Fonction permettant de construire un pion

    :param couleur: Couleur du pion à construire
    :return: Dictionnaire représentant un pion
    :raise TypeError: Si le paramètre n’est pas un entier
    :raise ValueError: Si l’entier ne représente pas une couleur
    """
    if type(color) != int :
        raise TypeError("construirePion : Le paramètre n’est pas de type entier")
    if color != const.ROUGE and color != const.JAUNE :
        raise ValueError(f"construirePion : la couleur {color} n’est pas correcte")
    return {const.COULEUR : color, const.ID : None}

def getCouleurPion(pion : dict) -> int :
    """
    Fonction permettant de récupérer la couleur d'un pion

    :param pion: Pion de la couleur à récupérer
    :return: Entier représentant une couleur
    :raise TypeError: Si le paramètre n'est pas un pion
    """
    if not type_pion(pion):
        raise TypeError("getCouleurPion : Le paramètre n’est pas un pion")
    return pion[const.COULEUR]

def setCouleurPion(pion : dict, color : int) -> None :
    """
    Fonction qui change la couleur du pion
    :param pion: Pion de la couleur à modifier
    :param color: Nouvelle couleur à définir au pion
    :return: Rien
    :raise TypeError: Si le premier paramètre n'est pas un pion
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si l’entier  du second paramètre ne représente pas une couleur
    """
    if not type_pion(pion):
        raise TypeError("setCouleurPion : Le premier paramètre n’est pas un pion")
    if type(color) != int :
        raise TypeError("setCouleurPion : Le second paramètre n’est pas un entier")
    if color != const.ROUGE and color != const.JAUNE :
        raise ValueError(f"setCouleurPion : Le second paramètre {color} n’est pas une couleur")
    pion[const.COULEUR] = color

def getIdPion(pion : dict) -> int :
    """
    Fonction permettant de récupérer l'identifiant d'un pion

    :param pion: Pion de l'identifiant à récupérer
    :return: Entier représentant l'identifiant du pion
    :raise TypeError: Si le paramètre n'est pas un pion
    """
    if not type_pion(pion):
        raise TypeError("getIdPion : Le paramètre n’est pas un pion")
    return pion[const.ID]

def setIdPion(pion : dict, val : int) -> None :
    """
    Fonction qui change l'identifiant du pion

    :param pion: Pion de l'identifiant à modifier
    :param val: Nouvel identifiant à définir au pion
    :return: Rien
    :raise TypeError: Si le premier paramètre n'est pas un pion
    :raise TypeError: Si le second paramètre n'est pas un entier
    """
    if not type_pion(pion):
        raise TypeError("setIdPion : Le premier paramètre n’est pas un pion")
    if type(val) != int :
        raise TypeError("setIdPion : Le second paramètre n’est pas un entier")
    pion[const.ID] = val

