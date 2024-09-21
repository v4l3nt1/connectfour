from Model.Constantes import *
from Model.Pion import *
from Model.Plateau import *
from random import randint



#
# Ce fichier contient les fonctions gérant le joueur
#
# Un joueur sera un dictionnaire avec comme clé :
# - const.COULEUR : la couleur du joueur entre const.ROUGE et const.JAUNE
# - const.PLACER_PION : la fonction lui permettant de placer un pion, None par défaut,
#                       signifiant que le placement passe par l'interface graphique.
# - const.PLATEAU : référence sur le plateau de jeu, nécessaire pour l'IA, None par défaut
# - d'autres constantes nécessaires pour lui permettre de jouer à ajouter par la suite...
#

def type_joueur(joueur: dict) -> bool:
    """
    Détermine si le paramètre peut correspondre à un joueur.

    :param joueur: Paramètre à tester
    :return: True s'il peut correspondre à un joueur, False sinon.
    """
    if type(joueur) != dict:
        return False
    if const.COULEUR not in joueur or joueur[const.COULEUR] not in const.COULEURS:
        return False
    if const.PLACER_PION not in joueur or (joueur[const.PLACER_PION] is not None
            and not callable(joueur[const.PLACER_PION])):
        return False
    if const.PLATEAU not in joueur or (joueur[const.PLATEAU] is not None and
        not type_plateau(joueur[const.PLATEAU])):
        return False
    return True

def getCouleurJoueur(joueur : dict) -> int :
    """
    Fonction permettant de récupérer la couleur d'un joueur

    :param joueur: Joueur de la couleur à récupérer
    :return: Entier représentant une couleur
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getCouleurJoueur : Le paramètre n’est pas un joueur")
    return joueur[const.COULEUR]

def getPlateauJoueur(joueur : dict) -> list :
    """
    Fonction permettant de récupérer le plateau d'un joueur

    :param joueur: Joueur du plateau à récupérer
    :return: Tableau 2D représentant le plateau
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getPlateauJoueur : Le paramètre n’est pas un joueur")
    return joueur[const.PLATEAU]

def getPlacerPionJoueur(joueur : dict) -> callable :
    """
    Fonction permettant de récupérer la fonction d'un joueur

    :param joueur: Joueur de la fonction à récupérer
    :return: Fonction du joueur passé en paramètre
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getPlacerPionJoueur : le paramètre ne correspond pas à un joueur")
    return joueur[const.PLACER_PION]

def getPionJoueur(joueur : dict) -> dict :
    """
    Fonction permettant de créer un pion de la couleur du joueur

    :param joueur: Joueur du pion à créer
    :return: Pion de la couleur du joueur
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getPionJoueur : le paramètre ne correspond pas à un joueur")
    return construirePion(getCouleurJoueur(joueur))

def setPlateauJoueur(joueur : dict, plateau : list) -> None :
    """
    Fonction permettant d'affecter le plateau à un joueur

    :param joueur: Joueur du plateau à affecter
    :return: Rien
    :raise TypeError: Si le premier paramètre n'est pas un joueur
    :raise TypeError: Si le second paramètre n'est pas un plateau
    """
    if not type_joueur(joueur):
        raise TypeError("setPlateauJoueur : le premier paramètre ne correspond pas à un joueur")
    if not type_plateau(plateau):
        raise TypeError("setPlateauJoueur : le second paramètre ne correspond pas à un plateau")
    joueur[const.PLATEAU] = plateau

def setPlacerPionJoueur(joueur : dict, fn : callable) -> None :
    """
    Fonction permettant d'affecter la fonction à un joueur

    :param joueur: Joueur de la fonction à affecter
    :return: Rien
    :raise TypeError: Si le premier paramètre n'est pas un joueur
    :raise TypeError: Si le second paramètre n'est pas une fonction
    """
    if not type_joueur(joueur):
        raise TypeError("setPlacerPionJoueur : le premier paramètre ne correspond pas à un joueur")
    if not callable(fn):
        raise TypeError("setPlacerPionJoueur : le second paramètre n’est pas une fonction")
    joueur[const.PLACER_PION] = fn

def _placerPionJoueur(joueur : dict) -> int :
    """
    Fonction qui détermine dans quelle colonne/ligne le pion sera lâché

    :param joueur: Joueur du pion à lâcher
    :return: Entier de la colonne qui accueillera le pion
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("_placerPionJoueur : Le paramètre n’est pas un joueur")
    if getModeEtenduJoueur(joueur) is False :
        collign = randint(0, const.NB_COLUMNS - 1)
        while joueur[const.PLATEAU][0][collign] is not None:
            collign = randint(0, const.NB_COLUMNS - 1)
    else :
        collign = randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES -1)
        while collign >= 0 and collign <= const.NB_COLUMNS - 1 and joueur[const.PLATEAU][0][collign] is not None :
            collign = randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES -1)

    return collign

def initialiserIAJoueur(joueur : dict, ordre : bool) -> None :
    """
    Fonction qui affecte la fonction d'IA au joueur

    :param joueur: Joueur de la fonction à affecter
    :return: Rien
    :raise TypeError: Si le premier paramètre n'est pas un joueur
    :raise TypeError: Si le second paramètre n'est pas un booléen
    """
    if not type_joueur(joueur):
        raise TypeError("initialiserIAJoueur : Le premier paramètre n’est pas un joueur")
    if type(ordre) is not bool:
        raise TypeError("initialiserIAJoueur : Le second paramètre n’est pas un booléen")
    if ordre is not True :
        setPlacerPionJoueur(joueur, _placerPionJoueur)
    else :
        setPlacerPionJoueur(joueur, _placerPionJoueur)

def getModeEtenduJoueur(joueur : dict) -> bool :
    """
    Fonction qui permet de savoir si le joueur est en mode étendu ou pas

    :param joueur: Joueur à étudier
    :return: True si il est en mode étendu, False sinon
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getModeEtenduJoueur : Le paramètre ne correspond pas à un joueur")
    res = False
    if const.MODE_ETENDU in joueur :
        res = True
    return res

def setModeEtenduJoueur(joueur : dict, cle : bool = True) -> None :
    """
    Fonction qui permet d'attribuer ou non le mode etendu au joueur en paramètre

    :param joueur: Joueur à modifier
    :param cle: Booléen à True si on ajoute la clé, False si on la supprime
    :return: Rien
    """
    if not type_joueur(joueur):
        raise TypeError("setModeEtenduJoueur : Le premier paramètre ne correspond pas à un joueur")
    if type(cle) is not bool :
        raise TypeError("setModeEtenduJoueur : le second paramètre ne correspond pas à un booléen")
    if cle is True :
        joueur[const.MODE_ETENDU] = ""
    else :
        del joueur[const.MODE_ETENDU]

