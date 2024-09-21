from Model.Constantes import *
from Model.Pion import *

#
# Le plateau représente la grille où sont placés les pions.
# Il constitue le coeur du jeu car c'est dans ce fichier
# où vont être programmées toutes les règles du jeu.
#
# Un plateau sera simplement une liste de liste.
# Ce sera en fait une liste de lignes.
# Les cases du plateau ne pourront contenir que None ou un pion
#
# Pour améliorer la "rapidité" du programme, il n'y aura aucun test sur les paramètres.
# (mais c'est peut-être déjà trop tard car les tests sont fait en amont, ce qui ralentit le programme...)
#

def type_plateau(plateau: list) -> bool:
    """
    Permet de vérifier que le paramètre correspond à un plateau.
    Renvoie True si c'est le cas, False sinon.

    :param plateau: Objet qu'on veut tester
    :return: True s'il correspond à un plateau, False sinon
    """
    if type(plateau) != list:
        return False
    if len(plateau) != const.NB_LINES:
        return False
    wrong = "Erreur !"
    if next((wrong for line in plateau if type(line) != list or len(line) != const.NB_COLUMNS), True) == wrong:
        return False
    if next((wrong for line in plateau for c in line if not(c is None) and not type_pion(c)), True) == wrong:
        return False
    return True

def construirePlateau() -> list :
    """
    Fonction qui construit un plateau

    :return: Tableau 2D représentant un plateau
    """
    plat = []
    for i in range(const.NB_LINES):
        tmp = []
        for j in range(const.NB_COLUMNS):
            tmp += [None]
        plat += [tmp]
    return plat

def placerPionPlateau(plateau : list, pion : dict, col : int) -> int :
    """
    Fonction qui place un pion sur le plateau

    :param plateau: Plateau qui accueillera le pion
    :param pion: Pion à placer sur le plateau
    :param col: Indice de la colonne où lâcher le pion
    :return: Indice de la ligne où le pion atterrit
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un pion
    :raise TypeError: Si le troisième paramètre n'est pas un entier
    :raise ValueError: Si la valeur de la colonne n'est pas correcte
    """
    if not type_plateau(plateau):
        raise TypeError("placerPionPlateau : Le premier paramètre ne correspond pas à un plateau")
    if not type_pion(pion):
        raise TypeError("placerPionPlateau : Le second paramètre n'est pas un pion")
    if type(col) != int :
        raise TypeError("placerPionPlateau : Le troisième paramètre n'est pas un entier")
    if col < 0 or col > const.NB_COLUMNS - 1 :
        raise ValueError(f"placerPionPlateau : La valeur de la colonne {col} n'est pas correcte")

    i = const.NB_LINES - 1
    res = -1
    while i >= 0 and res == -1 :
        if plateau[i][col] == None :
            plateau[i][col] = pion
            res = i
        else :
            i -= 1
    return res

def toStringPlateau(plateau : list) -> str :
    """
    Fonction qui affiche le plateau avec les pions en couleur

    :param plateau: Tableau 2D à transformer
    :return: Plateau sous forme de chaîne de caractères
    """
    rep = ""
    for i in range(len(plateau)):
        tmp = "|"
        for j in range(len(plateau[0])):
            if plateau[i][j] is None :
                tmp += " "
            else :
                if getCouleurPion(plateau[i][j]) == const.JAUNE:
                    tmp += f"\x1B[43m \x1B[0m"
                elif getCouleurPion(plateau[i][j]) == const.ROUGE:
                    tmp += f"\x1B[41m \x1B[0m"
            tmp += "|"
        rep += f"{tmp}\n"
    rep += ("---------------\n 0 1 2 3 4 5 6")
    return rep

def detecter4horizontalPlateau(plateau : list, color : int) -> list :
    """
    Fonction qui liste toutes les séries de 4 pions alignés
    horizontalement de la couleur passée en paramètre

    :param plateau: Tableau 2D à étudier
    :param color: Entier représentant la couleur à chercher
    :return: Liste des pions alignés horizontalement de la couleur voulue
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si le second paramètre n'est pas une couleur correcte
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4horizontalPlateau : Le premier paramètre ne correspond pas à un plateau")
    if type(color) != int :
        raise TypeError("detecter4horizontalPlateau : Le second paramètre n'est pas un entier")
    if color != const.ROUGE and color != const.JAUNE :
        raise ValueError(f"detecter4horizontalPlateau : La valeur de la couleur {color} n’est pas correcte")

    rep = []
    i = 0
    while i < len(plateau):
        j = 0
        while j <= const.NB_COLUMNS - 4 :
            if plateau[i][j] is not None and plateau[i][j+1] is not None and plateau[i][j+2] is not None and plateau[i][j+3] is not None:
                if getCouleurPion(plateau[i][j]) == color and getCouleurPion(plateau[i][j+1]) == color and getCouleurPion(plateau[i][j+2]) == color and getCouleurPion(plateau[i][j+3]) == color:
                    rep += [plateau[i][j], plateau[i][j+1], plateau[i][j+2], plateau[i][j+3]]
                    j = const.NB_COLUMNS - 3
            j += 1
        i += 1
    return rep

def detecter4verticalPlateau(plateau : list, color : int) -> list :
    """
    Fonction qui liste toutes les séries de 4 pions alignés
    verticalement de la couleur passée en paramètre

    :param plateau: Tableau 2D à étudier
    :param color: Entier représentant la couleur à chercher
    :return: Liste des pions alignés verticalement de la couleur voulue
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si le second paramètre n'est pas une couleur correcte
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4verticalPlateau : Le premier paramètre ne correspond pas à un plateau")
    if type(color) != int :
        raise TypeError("detecter4verticalPlateau : Le second paramètre n'est pas un entier")
    if color != const.ROUGE and color != const.JAUNE :
        raise ValueError(f"detecter4verticalPlateau : La valeur de la couleur {color} n’est pas correcte")
    rep = []
    j = 0
    while j < len(plateau[0]):
        i = 0
        while i <= const.NB_LINES - 4 :
            if plateau[i][j] is not None and plateau[i+1][j] is not None and plateau[i+2][j] is not None and plateau[i+3][j] is not None:
                if getCouleurPion(plateau[i][j]) == color and getCouleurPion(plateau[i+1][j]) == color and getCouleurPion(plateau[i+2][j]) == color and getCouleurPion(plateau[i+3][j]) == color:
                    rep += [plateau[i][j], plateau[i+1][j], plateau[i+2][j], plateau[i+3][j]]
                    i = const.NB_LINES - 3
            i += 1
        j += 1
    return rep

def detecter4diagonaleDirectePlateau(plateau : list, color : int) -> list :
    """
    Fonction qui liste toutes les séries de 4 pions alignés
    en diagonale directe et de la couleur passée en paramètre

    :param plateau: Tableau 2D à étudier
    :param color: Entier représentant la couleur à chercher
    :return: Liste des pions alignés en diagonale directe et de la couleur voulue
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si le second paramètre n'est pas une couleur correcte
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4diagonaleDirectePlateau : Le premier paramètre ne correspond pas à un plateau")
    if type(color) != int :
        raise TypeError("detecter4diagonaleDirectePlateau : Le second paramètre n'est pas un entier")
    if color != const.ROUGE and color != const.JAUNE :
        raise ValueError(f"detecter4diagonaleDirectePlateau : La valeur de la couleur {color} n’est pas correcte")
    rep = []
    i = const.NB_LINES - 1
    while i >= const.NB_LINES - 3 :
        j = const.NB_COLUMNS - 1
        while j >= const.NB_COLUMNS - 4 :
            if plateau[i][j] is not None and plateau[i-1][j-1] is not None and plateau[i-2][j-2] is not None and plateau[i-3][j-3] is not None :
                if getCouleurPion(plateau[i][j]) == color and getCouleurPion(plateau[i-1][j-1]) == color and getCouleurPion(plateau[i-2][j-2]) == color and getCouleurPion(plateau[i-3][j-3]) == color :
                    if i != const.NB_LINES -1 and j != const.NB_COLUMNS - 1 :
                        if plateau[i+1][j+1] is not None and getCouleurPion(plateau[i+1][j+1]) != color:
                            rep += [[plateau[i][j], plateau[i-1][j-1], plateau[i-2][j-2], plateau[i-3][j-3]]]
                    else :
                        rep += [plateau[i][j], plateau[i-1][j-1], plateau[i-2][j-2], plateau[i-3][j-3]]
            j -= 1
        i -= 1
    return rep

def detecter4diagonaleIndirectePlateau(plateau : list, color : int) -> list :
    """
    Fonction qui liste toutes les séries de 4 pions alignés
    en diagonale indirecte et de la couleur passée en paramètre

    :param plateau: Tableau 2D à étudier
    :param color: Entier représentant la couleur à chercher
    :return: Liste des pions alignés en diagonale indirecte et de la couleur voulue
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si le second paramètre n'est pas une couleur correcte
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4diagonaleIndirectePlateau : Le premier paramètre ne correspond pas à un plateau")
    if type(color) != int :
        raise TypeError("detecter4diagonaleIndirectePlateau : Le second paramètre n'est pas un entier")
    if color != const.ROUGE and color != const.JAUNE :
        raise ValueError(f"detecter4diagonaleIndirectePlateau : La valeur de la couleur {color} n’est pas correcte")
    rep = []
    i = const.NB_LINES - 1
    while i >= const.NB_LINES - 4:
        j = 0
        while j <= const.NB_COLUMNS - 4 :
            if plateau[i][j] is not None and plateau[i-1][j+1] is not None and plateau[i-2][j+2] is not None and plateau[i-3][j+3] is not None :
                if getCouleurPion(plateau[i][j]) == color and getCouleurPion(plateau[i-1][j+1]) == color and getCouleurPion(plateau[i-2][j+2]) == color and getCouleurPion(plateau[i-3][j+3]) == color:
                    if i != const.NB_LINES - 1 and j != 0 :
                        if plateau[i+1][j-1] is not None and getCouleurPion(plateau[i+1][j-1]) != color :
                            if (i - 3) >= 0 and (j + 3) <= 6:
                                rep += [plateau[i][j], plateau[i-1][j+1], plateau[i-2][j+2], plateau[i-3][j+3]]
                    else:
                        if (i - 3) >= 0 and (j + 3) <= 6:
                            rep += [plateau[i][j], plateau[i-1][j+1], plateau[i-2][j+2], plateau[i-3][j+3]]
            j += 1
        i -= 1
    return rep

def getPionsGagnantsPlateau(plateau : list) -> list :
    """
    Fonction qui liste tous les pions de toutes les séries du plateau

    :param plateau: Tableau 2D à étudier
    :return: Liste de tous les pions de toutes les séries du plateau
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if not type_plateau(plateau):
        raise TypeError("getPionsGagnantsPlateau : Le paramètre n’est pas un plateau")
    res = []
    for elt in const.COULEURS :
        res += detecter4verticalPlateau(plateau, elt)
        res += detecter4horizontalPlateau(plateau, elt)
        res += detecter4diagonaleDirectePlateau(plateau, elt)
        res += detecter4diagonaleIndirectePlateau(plateau, elt)
    return res

def isRempliPlateau(plateau : list) -> list :
    """
    Fonction dit si un plateau est rempli ou pas

    :param plateau: Tableau 2D à étudier
    :return: True ou False suivant si le plateau est rempli ou pas
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if not type_plateau(plateau):
        raise TypeError("isRempliPlateau : Le paramètre n’est pas un plateau")
    res = True
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if plateau[i][j] is None:
                res = False
    return res

def construireJoueur(color : int) -> dict :
    """
    Fonction qui crée un dictionnnaire correspondant à un joueur

    :param color: Couleur qui sera assignée au joueur
    :return: Un dictionnaire représentant le joueur
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne correspond pas à une couleur
    """
    if type(color) != int :
        raise TypeError("construireJoueur : Le paramètre n’est pas un entier")
    if color != const.ROUGE and color != const.JAUNE :
        raise ValueError(f"construireJoueur : L’entier donné {color} n’est pas une couleur.")
    return {const.COULEUR : color, const.PLATEAU : None, const.PLACER_PION : None}


def placerPionLignePlateau(plateau : list, pion : dict, numligne : int, left : bool) -> tuple :
    """
    Fonction qui permet de placer un pion sur le coté du plateau, à droite ou à gauche

    :param plateau: Plateau du pion à placer
    :param pion: Pion à placer sur le coté du plateau
    :param numligne: Numéro de la ligne où placer le pion
    :param left: Booléen à True si le pion va à gauche du plateau, faux sinon
    :return: Tuple contenant la liste des pions décalés par le pion placé, et un
             entier correspondant au numéro de ligne où se retrouve le dernier
             pion de la liste ou None si le dernier pion ne change pas de ligne
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un pion
    :raise TypeError: Si le troisème paramètre n'est pas un entier
    :raise ValueError: Si le troisième paramètre ne désigne pas une ligne
    :raise TypeError: Si le quatrième paramètre n'est pas un booléen
    """
    if not type_plateau(plateau) :
        raise TypeError("placerPionLignePlateau : Le premier paramètre n’est pas un plateau")
    if not type_pion(pion) :
        raise TypeError("placerPionLignePlateau : Le second paramètre n’est pas un pion")
    if type(numligne) != int :
        raise TypeError("placerPionLignePlateau : le troisième paramètre n’est pas un entier")
    if numligne < 0 or numligne > const.NB_LINES - 1 :
        raise ValueError(f"placerPionLignePlateau : le troisième paramètre {numligne} ne désigne pas une ligne")
    if type(left) != bool :
        raise TypeError("placerPionLignePlateau : le quatrième paramètre n’est pas un booléen")
    res = [pion]
    ligne = None
    if left :
        i = 0
        while i < const.NB_COLUMNS and plateau[numligne][i] != None :
            res += [plateau[numligne][i]]
            plateau[numligne][i] = res[i]
            i += 1
        if i == const.NB_COLUMNS :
            ligne = const.NB_LINES
        else :
            ligne = placerPionPlateau(plateau,res[i],i)
    else :
        i = const.NB_COLUMNS - 1
        while i > -1 and plateau[numligne][i] != None :
            res += [plateau[numligne][i]]
            plateau[numligne][i] = res[const.NB_COLUMNS - i - 1]
            i -= 1
        if i == -1 :
            ligne = const.NB_LINES
        else :
            ligne = placerPionPlateau(plateau, res[const.NB_COLUMNS - i - 1], i)
    return (res, ligne)

def equals(plat1 : list, plat2 : list) -> bool :
    res = False
    if plat1 == plat2 :
        res = True
    return res

def encoderPlateau(plateau : list) -> str :
    """
    Fonction qui transforme un plateau en une chaîne de caractères simple

    :param plateau: Plateau à transformer
    :return: Chaîne de caractères représentant le tableau
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if not type_plateau(plateau) :
        raise TypeError("encoderPlateau : le paramètre ne correspond pas à un plateau")
    res = ""
    for i in range(len(plateau)) :
        for j in range(len(plateau[i])) :
            if plateau[i][j] is None :
                res += "_"
            else :
                if getCouleurPion(plateau[i][j]) == const.ROUGE :
                    res += "R"
                elif getCouleurPion(plateau[i][j]) == const.JAUNE :
                    res += "J"
    return res

def isPatPlateau(plateau : list, hist : dict) -> bool :
    """
    Fonction qui vérifie si le plateau ets apparu 5 fois

    :param plateau: Plateau à étudier
    :param hist: Histogrammme des plateaux
    :return: Booléen à True si le plateau est identique 5 fois, False sinon
    :raise TypeError: Le premier paramètre n'est pas un plateau
    :raise TypeError: Le second paramètre n'est pas un dictionnaire
    """
    if not type_plateau(plateau) :
        raise TypeError("isPatPlateau : le premier paramètre ne correspond pas à un plateau")
    if type(hist) != dict :
        raise TypeError("isPatPlateau : Le second paramètre n’est pas un dictionnaire")
    res = False
    plateaustr = encoderPlateau(plateau)
    if plateaustr in hist :
        hist[plateaustr] += 1
        if hist[plateaustr] >= 5 :
            res = True
    else :
        hist[plateaustr] = 1
    return res




