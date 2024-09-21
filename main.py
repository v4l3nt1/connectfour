import pygame
from Controller.Controller import Controller
from View.ConnectFour import ConnectFour

# Essais graphiques
#



# Calcul de la taille de la fenêtre
# Nombre de cellules
CELL_LINE_COUNT = 16
CELL_COLUMN_COUNT = 16

# controller = Controller(CELL_LINE_COUNT, CELL_COLUMN_COUNT)
connect4 = ConnectFour(None)

connect4.play()


