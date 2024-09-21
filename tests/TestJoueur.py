import unittest
from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from Model.Constantes import *
from Model.Joueur import *
from random import randint

def _placer_pion() -> None:
    return None

class TestJoueur(unittest.TestCase):
    @unittest.skipIf('construireJoueur' not in globals(), "Constructeur non écrit")
    def test_construireJoueur(self):
        self.assertTrue(type_joueur(construireJoueur(const.JAUNE)))

    @unittest.skipIf('construireJoueur' not in globals(), "Constructeur non écrit")
    def test_OPTION_construireJoueurRaiseTypeError(self):
        self.assertRaises(TypeError, construireJoueur, "blablabla")
        self.assertRaises(TypeError, construireJoueur, [])

    @unittest.skipIf('construireJoueur' not in globals(), "Constructeur non écrit")
    def test_OPTION_construireJoueurRaiseValueError(self):
        self.assertRaises(ValueError, construireJoueur, 100)
        self.assertRaises(ValueError, construireJoueur, -1)

    @unittest.skipIf('getCouleurJoueur' not in globals(), 'Fonction getCouleurJoueur non écrite')
    def test_getCouleurJoueur(self):
        self.assertEqual(const.JAUNE, getCouleurJoueur(construireJoueur(const.JAUNE)))
        self.assertEqual(const.ROUGE, getCouleurJoueur(construireJoueur(const.ROUGE)))

    @unittest.skipIf('getCouleurJoueur' not in globals(), 'Fonction getCouleurJoueur non écrite')
    def test_OPTION_getCouleurJoueurRaiseTypeError(self):
        self.assertRaises(TypeError, getCouleurJoueur, "blablabla")
        self.assertRaises(TypeError, getCouleurJoueur, { "blablabla": 0})

    @unittest.skipIf('getPlateauJoueur' not in globals(), 'Fonction getPlateauJoueur non écrite')
    def test_getPlateauJoueur(self):
        j = construireJoueur(const.JAUNE)
        self.assertEqual(None, getPlateauJoueur(j), "Par défaut, devrait renvoyer None")
        p = construirePlateau()
        j[const.PLATEAU] = p
        self.assertEqual(p, getPlateauJoueur(j), "getPlateauJoueur ne renvoie pas la bonne valeur")

    @unittest.skipIf('getPlateauJoueur' not in globals(), 'Fonction getPlateauJoueur non écrite')
    def test_OPTION_getPlateauJoueurRaisesTypeError(self):
        j = construireJoueur(const.JAUNE)
        self.assertRaises(TypeError, getPlateauJoueur, "blablabla")
        self.assertRaises(TypeError, getPlateauJoueur, {const.PLATEAU: None})

    @unittest.skipIf('setPlateauJoueur' not in globals(), 'Fonction setPlateauJoueur non écrite')
    def test_setPlateauJoueur(self):
        j = construireJoueur(const.JAUNE)
        p = construirePlateau()
        setPlateauJoueur(j, p)
        self.assertEqual(p, getPlateauJoueur(j), "setPlateauJoueur ne modifie pas la bonne valeur ?")

    @unittest.skipIf('setPlateauJoueur' not in globals(), 'Fonction setPlateauJoueur non écrite')
    def test_OPTION_setPlateauJoueurRaisesTypeError(self):
        self.assertRaises(TypeError, setPlateauJoueur, construirePlateau(), construirePlateau())
        self.assertRaises(TypeError, setPlateauJoueur, construireJoueur(const.JAUNE), construireJoueur(const.JAUNE))
        # On ne doit pas accepter None comme argument pour le plateau
        self.assertRaises(TypeError, setPlateauJoueur, construireJoueur(const.JAUNE), None)

    @unittest.skipIf('getPlacerPionJoueur' not in globals(), 'Fonction getPlacerPionJoueur non écrite')
    def test_getPlacerPionJoueur(self):
        j = construireJoueur(const.JAUNE)
        self.assertEqual(None, getPlacerPionJoueur(j), "getPlacerPionJoueur devrait retourner None par défaut")
        j[const.PLACER_PION] = _placer_pion
        self.assertEqual(_placer_pion, getPlacerPionJoueur(j), "getPlacerPionJoueur ne retourne pas la bonne valeur ?")

    @unittest.skipIf('getPlacerPionJoueur' not in globals(), 'Fonction getPlacerPionJoueur non écrite')
    def test_OPTION_getPlacerPionJoueurRaisesTypeError(self):
        j = construireJoueur(const.JAUNE)
        self.assertRaises(TypeError, getPlacerPionJoueur, "blablabla")

    @unittest.skipIf('setPlacerPionJoueur' not in globals(), 'Fonction setPlacerPionJoueur non écrite')
    def test_setPlacerPionJoueur(self):
        j = construireJoueur(const.JAUNE)
        setPlacerPionJoueur(j, _placer_pion)
        self.assertEqual(_placer_pion, getPlacerPionJoueur(j), "setPlacerPionJoueur ne modifie pas la bonne valeur ?")

    @unittest.skipIf('setPlacerPionJoueur' not in globals(), 'Fonction setPlacerPionJoueur non écrite')
    def test_OPTION_setPlacerPionJoueurRaisesTypeError(self):
        j = construireJoueur(const.JAUNE)
        self.assertRaises(TypeError, setPlacerPionJoueur, "blablabla", _placer_pion)
        self.assertRaises(TypeError, setPlacerPionJoueur, j, "blablabla")
        # La fonction ne doit pas accepter None
        self.assertRaises(TypeError, setPlacerPionJoueur, j, None)

    @unittest.skipIf('getPionJoueur' not in globals(), 'Fonction getPionJoueur non écrite')
    def test_getPionJoueur(self):
        for col in const.COULEURS:
            j = construireJoueur(col)
            pion = getPionJoueur(j)
            self.assertTrue(type_pion(pion), "L'objet retourné par getPionJoueur n'est pas un pion")
            self.assertEqual(col, getCouleurPion(pion), "La couleur du pion retournée par getPionJoueur ne correspond pas à la couleur du joueur")

    @unittest.skipIf('getPionJoueur' not in globals(), 'Fonction getPionJoueur non écrite')
    def test_OPTION_getPionJoueurRaisesTypeError(self):
        self.assertRaises(TypeError, getPionJoueur, "blablabla")

    @unittest.skipIf('getModeEtenduJoueur' not in globals(), 'Fonction getModeEtenduJoueur non écrite')
    def test_getModeEtenduJoueur(self):
        j = construireJoueur(const.JAUNE)
        self.assertFalse(getModeEtenduJoueur(j), "Par défaut, Le mode étendu ne devrait pas être activé")
        j[const.MODE_ETENDU] = True
        self.assertTrue(getModeEtenduJoueur(j), "Le mode étendu devrait être activé...")
        j[const.MODE_ETENDU] = 12
        self.assertTrue(getModeEtenduJoueur(j), "Le mode étendu ne devrait pas être dépendant de la valeur affectée à la clé.")
        del j[const.MODE_ETENDU]
        self.assertFalse(getModeEtenduJoueur(j), "Le mode étendu ne devrait pas être activé")

    @unittest.skipIf('getModeEtenduJoueur' not in globals(), 'Fonction getModeEtenduJoueur non écrite')
    def test_OPTION_getModeEtenduJoueurRaisesTypeError(self):
        self.assertRaises(TypeError, getModeEtenduJoueur, "blablabla")

    @unittest.skipIf('setModeEtenduJoueur' not in globals(), 'Fonction setModeEtenduJoueur non écrite')
    def test_setModeEtenduJoueur(self):
        j = construireJoueur(const.JAUNE)
        setModeEtenduJoueur(j)
        self.assertTrue(getModeEtenduJoueur(j), "Le mode étendu devrait être activé quand on ne met pas de paramètre.")
        setModeEtenduJoueur(j, False)
        self.assertFalse(getModeEtenduJoueur(j), "Le mode étendu devrait être désactivé")
        setModeEtenduJoueur(j, True)
        self.assertTrue(getModeEtenduJoueur(j), "Le mode étendu devrait être activé")
        setModeEtenduJoueur(j, False)
        setModeEtenduJoueur(j, False)
        self.assertFalse(getModeEtenduJoueur(j), "Il ne devrait pas y avoir d'erreur si on désactive 2 fois le mode étendu")

    @unittest.skipIf('setModeEtenduJoueur' not in globals(), 'Fonction setModeEtenduJoueur non écrite')
    def test_OPTION_setModeEtenduJoueurRaisesTypeError(self):
        self.assertRaises(TypeError, setModeEtenduJoueur, None, True)
        self.assertRaises(TypeError, setModeEtenduJoueur, "blablabla", True)
        j = construireJoueur(const.JAUNE)
        self.assertRaises(TypeError, setModeEtenduJoueur, j, 12)




