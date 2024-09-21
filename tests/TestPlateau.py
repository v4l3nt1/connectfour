import unittest
from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from random import randint, choice
from copy import deepcopy


class TestPlateau(unittest.TestCase):
    @unittest.skipIf('construirePlateau' not in globals(), "Constructeur non écrit")
    def test_construirePlateau(self):
        self.assertTrue(type_plateau(construirePlateau()))

    @unittest.skipIf('placerPionPlateau' not in globals(), 'Fonction placerPionPlateau non écrite')
    def test_placerPionPlateau(self):
        for _ in range(100):
            p = construirePlateau()
            places = [0]*const.NB_COLUMNS
            for __ in range(2*const.NB_LINES*const.NB_COLUMNS):
                col = randint(0, const.NB_COLUMNS - 1)
                places[col] = min(1 + places[col], const.NB_LINES + 1)
                self.assertEqual(const.NB_LINES - places[col], placerPionPlateau(p, construirePion(const.ROUGE), col))

