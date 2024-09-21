import pygame
from View.Images import Images

# from View.Button import Button
# from View.Digit import Digit
# from View.DigitClock import DigitClock
from Controller.Controller import Controller
from random import randint, choice

from Model.Constantes import *




class ConnectFour:
    """
    Position de l'image dans le tuple du dictionnaire d'images
    """
    _pos_img = 0
    """
    Position des coordonnées de l'image dans le tuple du dictionnaire d'images
    """
    _pos_coords = 1

    def __init__(self, controller: Controller):

        pygame.init()
        pygame.font.init()
        self.font_size = 20
        # Initialisation de la fonte
        self.bold_fonte = pygame.font.SysFont('Arial', self.font_size, bold=True)
        self.fonte = pygame.font.SysFont('Times New Roman', self.font_size)
        self.bord = 10


        Images.load_images()

        self.size = Images.get_window_size()
        self.screen = pygame.display.set_mode((self.size[0], self.size[1]))

        self.do_refresh = True

        self.hand_id_img = None
        self.hand_column = -1
        self.current_player = choice([const.ROUGE, const.JAUNE])

        # Création du dictionnaire des images à afficher (sauf le décor bien-sûr)
        self.img_dict = {}
        # Gestionnaire des identifiants
        self.id_img = 0

        # Fin du jeu
        self.ended = False

        # Surligner les pions gagnants
        self.rects = None # Format : [(x, y, w, h), (x, y, w, h), ...]

        # Remplissage des jetons aléatoire
        # for line in range(6):
        #     for column in range(7):
        #         _n = randint(0, 2)
        #         if _n < 2:
        #             self.add_image(Images.img_pieces[_n], Images.get_piece_coordinates(line, column))

        from View.Animation import Animation
        # Gestion des animations
        # self._animations = Animation(self)
        self._hand_animation = None
        self.rollback_hand_animation = False
        self.hand_animation_current_column = None
        self.hand_animation_current_line = None
        self.hand_animation_color = None
        self.hand_animation_final_column = None
        self.hand_animation_final_line = None


        self.controller = Controller()
        self.controller.set_win(self)

        self.extended_mode = self.display_message("Choisissez le mode de jeu : ", ["Normal", "Etendu"]) == 1
        j = self.display_message("Choisissez le premier joueur : ", ["Humain", "Ordinateur"])
        self.controller.set_first_player(j == 0)
        j = self.display_message("Choisissez le second joueur : ", ["Humain", "Ordinateur"])
        self.controller.set_second_player(j == 0)
        self.display_message("Pour faire jouer un joueur, appuyez sur la barre d'espace.   Pour lâcher un pion, appuyez sur la barre d'espace.")




    def add_image(self, image: pygame.Surface, coords: tuple) -> int:
        self.id_img += 1
        self.img_dict[self.id_img] = [image, coords]
        return self.id_img

    def remove_image(self, id_img: int) -> None:
        del self.img_dict[id_img]
        return None

    def replace_image(self, id_img: int, img: pygame.Surface, coord: tuple) -> None:
        self.img_dict[id_img] = [img, coord]
        return None

    def set_coordinates_image(self, id_img: int, new_coords: tuple) -> tuple:
        old_coords = self.img_dict[id_img][1]
        self.img_dict[id_img][1] = new_coords
        return old_coords

    def get_image(self, id_img: int) -> pygame.Surface:
        return self.img_dict[id_img][0]

    def get_coordinates_image(self, id_img: int) -> tuple:
        return self.img_dict[id_img][1]

    def human_play(self):
        from View.HandAnimation import HandAnimation
        self._hand_animation = HandAnimation(self, self.controller.get_current_color())

    def anime_play(self, column: int) -> None:
        from View.HandAnimation import HandAnimation
        # L'animation va être simulée par un appel récursif de cette fonction...
        # On récupère la couleur du joueur
        # print("animating the hand to move to column", column)
        self.hand_animation_color = self.controller.get_current_color()
        self.hand_animation_current_column = 0 if self.hand_animation_color == const.JAUNE else const.NB_COLUMNS - 1
        self.hand_animation_final_column = -1 if column < 0 else const.NB_COLUMNS if column >= const.NB_COLUMNS else column
        self.hand_animation_current_line = 0
        if self.hand_animation_final_column == -1:
            self.hand_animation_final_line = -column - 1
        elif self.hand_animation_final_column == const.NB_COLUMNS:
            self.hand_animation_final_line = column - const.NB_COLUMNS
        else:
            self.hand_animation_final_line = None
            self.hand_animation_current_line = None
        self._hand_animation = HandAnimation(self, self.hand_animation_color)
        self.rollback_hand_animation = True

    def rollback(self) -> None:
        if not self._hand_animation.is_animating():
            if self.hand_animation_current_column == self.hand_animation_final_column:
                if  self.hand_animation_final_line is None\
                    or self.hand_animation_current_line == self.hand_animation_final_line:
                    # Fin de l'animation !
                    # print("** dropping !")
                    self.rollback_hand_animation = False
                    self._hand_animation.drop()
                else:
                    self.hand_animation_current_line += 1
                    self._hand_animation.move_down()
            elif self.hand_animation_color == const.JAUNE:
                if self.hand_animation_final_column == -1:
                    self.hand_animation_current_column -= 1
                    self._hand_animation.move_left()
                else:
                    # On est à gauche
                    # print("** move to right")
                    self.hand_animation_current_column += 1
                    self._hand_animation.move_right()
            elif self.hand_animation_final_column == const.NB_COLUMNS:
                self.hand_animation_current_column += 1
                self._hand_animation.move_right()
            else:
                # On est à droite
                # print("** move to left")
                self.hand_animation_current_column -= 1
                self._hand_animation.move_left()
        else:
            # print("** is animating !??")
            pass

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if self.ended:
                        continue
                    # print(f"Keydown: {event.key}  - {pygame.K_LEFT}, {pygame.K_RIGHT}, {pygame.K_SPACE}")
                    if event.key == pygame.K_SPACE:
                        if self._hand_animation is None:
                            self.controller.play()
                            # self._hand_animation = HandAnimation(self, self.current_player)
                        else:
                            self._hand_animation.drop()
                    elif event.key == pygame.K_LEFT and self._hand_animation is not None:
                        self._hand_animation.move_left()
                    elif event.key == pygame.K_RIGHT and self._hand_animation is not None:
                        self._hand_animation.move_right()
                    elif event.key == pygame.K_UP and self._hand_animation is not None:
                        self._hand_animation.move_up()
                    elif event.key == pygame.K_DOWN and self._hand_animation is not None:
                        self._hand_animation.move_down()
                elif event.type > pygame.USEREVENT:
                    if self._hand_animation is not None:
                        self._hand_animation.anime(event.type)
                        if (self._hand_animation is not None and
                                not self._hand_animation.is_animating()
                                and self.rollback_hand_animation):
                            # print("** rollback !")
                            self.rollback()
            if self.do_refresh:
                self.refresh()

    def get_line(self, column: int) -> int:
        return self.controller.drop_on(column, self._hand_animation.get_id_piece())

    def get_push_line(self, line: int, left: bool) -> tuple:
        return self.controller.drop_on_line(line, left, self._hand_animation.get_id_piece())

    def end_hand_action(self, move: int) -> None:
        self._hand_animation = None
        self.controller.human_has_played(move)
        res = self.controller.get_winner()
        if res is not None and len(res) > 0:
            self.outline(res)
            msg = f"Les pions {('JAUNES' if self.controller.get_piece_color(res[0]) == const.JAUNE else 'ROUGES')} gagnent !"
            self.display_message(msg)
            self.ended = True
        elif self.controller.is_game_pat(self.extended_mode):
            self.display_message("Le jeu est fini, il n'y a aucun gagnant")
            self.ended = True
        else:
            self.controller.next()
        return None
        # self.current_player = const.JAUNE if self.current_player == const.ROUGE else const.ROUGE

    def outline(self, pions: list) -> None:
        self.rects = []
        for p in pions:
            _id = self.controller.get_piece_id(p)
            if _id == 0:
                continue
            x, y = self.get_coordinates_image(_id)
            self.rects.append((x, y, Images.get_piece_width(), Images.get_piece_height()))
        self.set_refresh(True)

    def set_refresh(self, b: bool = True):
        self.do_refresh = b

    def refresh(self):
        # Dessin de l'image de fond
        self.screen.blit(Images.img_background, (0, 0))

        # Dessin des images
        for img, coord in self.img_dict.values():
            self.screen.blit(img, coord)

        # Dessin du tableau
        self.screen.blit(Images.img_board, Images.get_board_coordinates())

        # Surlignage des pions gagnants
        if self.rects is not None:
            color = pygame.Color(109, 255, 12)
            for t in self.rects:
                pygame.draw.ellipse(self.screen, color, t, 5)
        self.do_refresh = False

        pygame.display.flip()

    def display_message(self, message: str, boutons: list = ["Ok"]) -> int:
        """
        Affiche une boîte de dialogue et retourne le numéro de bouton (commençant à 0) cliqué

        :param message: Message de la boîte de dialogue
        :param boutons: Liste des boutons (chaînes de caractères)
        :return: Numéro du bouton cliqué
        """

        # Largeur maximale de la boîte de dialogue : 4/5 de la largeur de la fenêtre
        w_max = 3*self.size[0]//4
        # Premier rendu du message
        txt = self.bold_fonte.render(message, True, (0, 0, 0))
        message_list = [txt]
        if txt.get_width() > w_max:
            # Il faut découper le message !
            # Nombre de caractères :
            nb = (w_max * len(message)) // txt.get_width()
            txt = None
            # Découpe du message
            msgs = message.split(' ')
            # Construction des découpes
            s = ""
            message_list = []
            for m in msgs:
                if len(s) + len(m) <= nb:
                    s = m if len(s) == 0 else s + " " + m
                else:
                    message_list.append(self.bold_fonte.render(s, True, (0, 0, 0)))
                    s = m
            if s is not None:
                message_list.append(self.bold_fonte.render(s, True, (0, 0, 0)))
        # Calcul de la largeur max des textes
        w_t = max([m.get_width() for m in message_list]) + 2*self.bord
        # Création des boutons
        btns = []
        for s in boutons:
            btns.append(self.bold_fonte.render(s, True, (0, 0, 0)))
        # Calcul de la largeur totale des boîtes des boutons
        w = sum([s.get_width() + 2*self.bord for s in btns]) + self.bord*len(btns)
        # print("w =", w, "w_max =", w_max)
        bouton_list = []
        if w > w_max:
            # Il faut découper les boutons sur plusieurs lignes
            w = 0
            lst = []
            for btn in btns:
                _w = btn.get_width() + 3*self.bord
                if w + _w < w_max:
                    lst.append(btn)
                    w += _w
                else:
                    bouton_list.append(lst)
                    w = _w
                    lst = [btn]
            bouton_list.append(lst)
        else:
            bouton_list.append(btns)
        # print("len(bouton_list) =", len(bouton_list))
        # Calcul de la largeur max des boutons
        w_b = max([sum([b.get_width() for b in lst]) + self.bord*(len(lst)+1) for lst in bouton_list])
        # Largeur de la boîte de dialogue
        w_boite = max(w_t, w_b)
        # Calcul de la hauteur de la boîte de dialogue
        h_boite = len(message_list)*self.font_size + (len(message_list)+1)*self.bord + \
            len(bouton_list)*(self.font_size + 3*self.bord) + self.bord
        # On peut maintenant dessiner la boîte de dialogue
        x_boite = (self.size[0] - w_boite) // 2
        y_boite = (self.size[1] - h_boite) // 2
        # Dessin du fond de la boîte
        self.screen.fill((255, 255, 255), (x_boite, y_boite, w_boite, h_boite))
        # Dessin du cadre de la boîte
        pygame.draw.rect(self.screen, (0, 0, 0), (x_boite, y_boite, w_boite, h_boite), 1)
        # Affichage du texte
        y = y_boite + self.bord
        for m in message_list:
            self.screen.blit(m, (x_boite + (w_boite - m.get_width())//2, y))
            y += self.font_size + self.bord
        # Affichage des boutons
        # On construit en même temps les cadres des boutons
        y += self.bord
        btn_cadre = []
        for lst in bouton_list:
            w = sum([btn.get_width() for btn in lst]) + 3*len(lst)*self.bord
            space = (w_boite - w) // 2
            x = space + x_boite
            for btn in lst:
                # Calcul de la largeur du bouton
                w = btn.get_width() + 2*self.bord
                # Calcul de la hauteur du bouton
                h = self.font_size+ 2*self.bord
                # Stockage du cadre et du "texte" du bouton
                btn_cadre.append((x, y, x+w, y+h, btn))
                # Dessin du bouton
                self._display_button(btn_cadre[-1])
                x += w + self.bord
            y += 3*self.bord + self.font_size
        # Mise a jour de la fenêtre
        pygame.display.flip()
        # On attend que l'utilisateur clique sur un bouton...
        # On empêche la sortie de l'application ?...
        clicked_btn = -1
        # Animation du bouton lorsque la souris est dessus
        over_btn = -1
        while clicked_btn == -1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                    (x, y) = event.pos
                    # On recherche si la position se trouve sur un des boutons
                    over = -1
                    for (n, (x1, y1, x2, y2, _)) in enumerate(btn_cadre):
                        if x1 <= x <= x2 and y1 <= y <= y2:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                clicked_btn = n
                            else:
                                over = n
                    if event.type == pygame.MOUSEMOTION:
                        # On regarde s'il faut redessiner le bouton
                        refresh = False
                        if over != over_btn:
                            if over_btn != -1:
                                # On remet le bouton dans son état normal
                                self._display_button(btn_cadre[over_btn])
                                refresh = True
                            over_btn = over
                            if over_btn != -1:
                                # On active le nouveau bouton
                                self._display_button(btn_cadre[over_btn], actif=True)
                                refresh = True
                        if refresh:
                            pygame.display.flip()
        # On efface la boîte de dialogue
        self.refresh()
        return clicked_btn

    def _display_button(self, cadre: tuple, actif: bool = False, actualise: bool = False):
        """
        Usage interne uniquement : Dessine un bouton avec son texte

        :param cadre: tuple (x1, y1, x2, y2, btn) définissant le cadre du bouton (pt sup gauche, pt inf droit) et le
        contenu (btn) de type pygame.Surface
        :param actif: True si la souris est au-dessus du bouton
        :param actualise: True s'il faut rafraîchir la fenêtre immédiatement
        :return: Rien
        """
        # Récupération du cadre et du contenu
        (x1, y1, x2, y2, btn) = cadre
        w = x2 - x1
        h = y2 - y1
        # Dessin du fond du bouton
        col = (134, 255, 13) if actif else (192, 192, 192)
        self.screen.fill(col, (x1, y1, w, h))
        # Dessin du cadre
        pygame.draw.rect(self.screen, (0, 0, 0), (x1, y1, w, h), 2 if actif else 1)
        # Dessin du texte
        self.screen.blit(btn, (x1 + self.bord, y1 + self.bord))
        if actualise:
            pygame.display.flip()

