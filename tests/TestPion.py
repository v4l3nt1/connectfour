import unittest
from random import randint

from Model.Pion import *

class TestPion(unittest.TestCase):
    @unittest.skipIf('construirePion' not in globals(), "Constructeur non écrit")
    def test_construirePion(self):
        p = construirePion(const.ROUGE)
        expected = { const.COULEUR: const.ROUGE, const.ID: None}
        self.assertTrue(type_pion(p), "Le constructeur ne retourne pas le bon type")
        self.assertEqual(expected, p, "Le constructeur ne retourne pas les bonnes données")
        p = construirePion(const.JAUNE)
        expected = { const.COULEUR: const.JAUNE,const.ID: None}
        self.assertTrue(type_pion(p), "Le constructeur ne retourne pas le bon type")
        self.assertEqual(expected, p, "Le constructeur ne retourne pas les bonnes données")

    @unittest.skipIf('construirePion' not in globals(), "Constructeur non écrit")
    def test_OPTION_construirePion_raise_TypeError(self):
        self.assertRaises(TypeError, construirePion, "blabla")

    @unittest.skipIf('construirePion' not in globals(), "Constructeur non écrit")
    def test_OPTION_construirePion_raise_ValueError(self):
        self.assertRaises(ValueError, construirePion, 100)

    @unittest.skipIf('getCouleurPion' not in globals(), "Fonction getCouleurPion non écrite")
    def test_getCouleurPion(self):
        p = {const.ID: None}
        for c in [const.ROUGE, const.JAUNE]:
            p[const.COULEUR] = c
            self.assertEqual(c, getCouleurPion(p), "getCouleurPion ne retourne pas la bonne couleur")

    @unittest.skipIf('getCouleurPion' not in globals(), "Fonction getCouleurPion non écrite")
    def test_OPTION_getCouleurPion_raise_TypeError(self):
        self.assertRaises(TypeError, getCouleurPion, "blablabla")

    @unittest.skipIf('setCouleurPion' not in globals(), "Fonction setCouleurPion non écrite")
    def test_setCouleurPion(self):
        p = {const.COULEUR: const.ROUGE, const.ID: None}
        for c in [const.ROUGE, const.JAUNE]:
            setCouleurPion(p, c)
            self.assertEqual(c, getCouleurPion(p), "setCouleurPion ne semble pas modifier la couleur ?")

    @unittest.skipIf('setCouleurPion' not in globals(), "Fonction setCouleurPion non écrite")
    def test_OPTION_setCouleurPion_raise_TypeError(self):
        self.assertRaises(TypeError, setCouleurPion, "blablabla", const.ROUGE)
        p = construirePion(const.ROUGE)
        self.assertRaises(TypeError, setCouleurPion, p, "blablabla")
        self.assertRaises(ValueError, setCouleurPion, p, 100)

    @unittest.skipIf('getIdPion' not in globals(), "Fonction getIdPion non écrite")
    def test_getIdPion(self):
        for _ in range(10):
            id = randint(-100, 100)
            p = construirePion(const.ROUGE)
            p[const.ID] = id
            self.assertEqual(id, getIdPion(p), "Le getter ne retourne pas la bonne valeur.")

    @unittest.skipIf('setIdPion' not in globals(), "Fonction setIdPion non écrite")
    def test_setIdPion(self):
        for _ in range(10):
            id = randint(-100, 100)
            p = construirePion(const.ROUGE)
            setIdPion(p, id)
            self.assertEqual(id, p[const.ID], "Le setter ne modifie pas la bonne clé ?")

    @unittest.skipIf('getIdPion' not in globals(), "Fonction getIdPion non écrite")
    def test_OPTION_getIdPion_raise_TypeError(self):
        self.assertRaises(TypeError, getIdPion, 'blablabla')

    @unittest.skipIf('setIdPion' not in globals(), "Fonction setIdPion non écrite")
    def test_OPTION_setIdPion_raise_TypeError(self):
        self.assertRaises(TypeError, setIdPion, 'blablabla', 10)
        p = construirePion(const.ROUGE)
        self.assertRaises(TypeError, setIdPion, p, 'truc')


