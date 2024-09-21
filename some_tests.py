from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from random import randint, choice
"""
p = construirePlateau()
print(p)
pion = construirePion(const.JAUNE)
line = placerPionPlateau(p, pion, 2)
print("Placement d’un pion en colonne 2. Numéro de ligne :", line)
print(p)

# Essais sur les couleurs
print("\x1B[43m \x1B[0m : carré jaune ")
print("\x1B[41m \x1B[0m : carré rouge ")
print("\x1B[41mA\x1B[0m : A sur fond rouge")
"""
"""
p = construirePlateau()
for _ in range(40):
    placerPionPlateau(p, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
print(toStringPlateau(p))
"""

a = []
while a == []:
    p = construirePlateau()
    for _ in range(100):
        placerPionPlateau(p, construirePion(0), randint(0, const.NB_COLUMNS - 1))
    a = detecter4diagonaleIndirectePlateau(p, 0)
print(toStringPlateau(p))
print(a)
print(len(a))