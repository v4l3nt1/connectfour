from View.Animation import Animation
from View.ConnectFour import ConnectFour
from View.Images import Images
from Model.Constantes import *

class HandAnimation(Animation):
    """
    Cette classe gère uniquement l'animation de la main déposant une pièce !
    """
    def __init__(self, main: ConnectFour, color: int):
        # Ajout de la main
        super().__init__(main)
        self.column = 0 if color == const.JAUNE else const.NB_COLUMNS - 1
        self.line = -1
        self.color = color
        self.line_down = None
        self.column_down = None
        self.move = None
        (xf, y) = Images.x_hands[color][self.column], Images.y_hands
        xd = -Images.get_hand_width() if color == const.JAUNE else Images.get_window_size()[0]
        img = Images.img_hands[color]
        self.hand_id_anim = self.add_new_animation(img, (xd, y), (xf, y), 1000)
        self.hand_id = self.get_image_id(self.hand_id_anim)
        self.piece_id = self.add_image(self.hand_id_anim, Images.img_pieces[color],
                                       (xd + Images.x_hand_offset[color], y + Images.y_hand_offset),
                                       (Images.x_piece[self.column], Images.y_piece[self.line]))

    def move_left(self) -> bool:
        if not self.is_ended(self.hand_id_anim):
            return False
        if not self._main.extended_mode and self.column == 0:
            return False
        if self.column not in [-1, const.NB_COLUMNS]:
            self.column -= 1
            self._move_to_column()
            return True
        return False

    def move_right(self) -> bool:
        if not self.is_ended(self.hand_id_anim):
            return False
        if not self._main.extended_mode and self.column == const.NB_COLUMNS - 1:
            return False
        if self.column not in [-1, const.NB_COLUMNS]:
            self.column += 1
            self._move_to_column()
            return True
        return False

    def move_up(self) -> bool:
        if not self.is_ended(self.hand_id_anim):
            return False
        if self.column in [-1, const.NB_COLUMNS]:
            self.line -= 1
            self._move_to_line()
            return True
        return False

    def move_down(self) -> bool:
        if not self.is_ended(self.hand_id_anim):
            return False
        if self.column in [-1, const.NB_COLUMNS]:
            if self.line == const.NB_LINES - 1:
                # On ne peut plus descendre
                return False
            self.line += 1
            self._move_to_line()
            return True
        return False

    def _move_to_column(self) -> None:
        self.hand_id_anim = self.add_animation(self.hand_id, self._main.get_coordinates_image(self.hand_id),
                                               Images.get_hand_coordinates(self.color, self.column))
        self.add_id_image(self.hand_id_anim, self.piece_id, self._main.get_coordinates_image(self.piece_id),
                          Images.get_piece_coordinates(self.line, self.column))
        if self.column in [-1, const.NB_COLUMNS] and self.line == -1:
            angle = 90 if self.column == -1 else -90
            self.add_ended_callback(self.hand_id_anim, self._turn_hand, angle, False)
        return None

    def _move_to_line(self) -> None:
        self.hand_id_anim = self.add_animation(self.hand_id, self._main.get_coordinates_image(self.hand_id),
                                               Images.rotated_hands_position[self.color][self.line, self.column])
        self.add_id_image(self.hand_id_anim, self.piece_id, self._main.get_coordinates_image(self.piece_id),
                          (Images.x_piece[self.column], Images.y_piece[self.line]))
        if self.column in [-1, const.NB_COLUMNS] and self.line == -1:
            angle = -90 if self.column == -1 else 90
            self.add_ended_callback(self.hand_id_anim, self._turn_hand, angle, True)
        return None

    def _turn_hand(self, angle: float, up: bool) -> None:
        coords = self._main.get_coordinates_image(self.hand_id)
        if not up:
            coords2 = Images.rotated_hands_position[self.color][self.line, self.column]
            fn = self._move_turned_hand_down
        else:
            coords2 = Images.x_hands[self.color][self.column], Images.y_hands
            fn = self._move_back_hand
        # print("Destination :", coords2)
        self.hand_id_anim = self.add_animation(self.hand_id, coords, coords2, rotate=angle, delay=200)
        # print("_turn_hand : id_animation =", self.hand_id_anim)
        self.add_ended_callback(self.hand_id_anim, fn)

    def _move_turned_hand_down(self):
        # print("Descente de la main")
        self.line = 0
        self.hand_id_anim = self.add_animation(self.hand_id,
                                               Images.rotated_hands_position[self.color][self.line - 1, self.column],
                                               Images.rotated_hands_position[self.color][self.line, self.column])
        self.add_id_image(self.hand_id_anim, self.piece_id,
                          (Images.x_piece[self.column], Images.y_piece[self.line - 1]),
                          (Images.x_piece[self.column], Images.y_piece[self.line]))

    def _move_back_hand(self):
        # print("Retour de la main sur la première ligne")
        self.line = -1
        if self.column == -1:
            self.column = 0
        else:
            self.column = const.NB_COLUMNS - 1
        h_dest = Images.get_hand_coordinates(self.color, self.column) #Images.x_hands[self.color][self.column], Images.y_hands
        p_dest = Images.get_piece_coordinates(-1, self.column) #Images.x_piece[self.column], Images.y_piece[-1]

        self.hand_id_anim = self.add_animation(self.hand_id,
                                               self._main.get_coordinates_image(self.hand_id),
                                               h_dest)
        self.add_id_image(self.hand_id_anim, self.piece_id,
                          self._main.get_coordinates_image(self.piece_id),
                          p_dest)

    def _remove_hand(self):
        if self.line_down is not None and self.line_down == const.NB_LINES:
            # Suppression du pion qui est poussé en dehors du plateau...
            self._main.remove_image(self.piece_id)
        self.hand_id_anim = None
        self.piece_id = None
        self._main.remove_image(self.hand_id)
        # Détermination du mouvement
        move = self.column
        if self.column == -1:
            move = -self.line - 1
        elif self.column == const.NB_COLUMNS:
            move = const.NB_COLUMNS + self.line
        self._main.end_hand_action(move)

    def drop(self) -> bool:
        if not self.is_ended(self.hand_id_anim):
            # print("Animation non terminée !!")
            return False
        if self.column in [-1, const.NB_COLUMNS]:
            if not self._main.extended_mode:
                return False # Bizarre ! On ne devrait pas arriver ici ??
            left = self.column == -1
            lst_id, line = self._main.get_push_line(self.line, left)
            return self._animate_push_line(lst_id, line)

        line = self._main.get_line(self.column)
        if line < 0:
            return False
        col = self.column
        self.hand_id_anim = self.add_animation(self.piece_id, self._main.get_coordinates_image(self.piece_id),
                                               Images.get_piece_coordinates(line, col))
        self.add_ended_callback(self.hand_id_anim, self._remove_hand)
        return True

    def _animate_push_line(self, lst_id: list, line: int) -> bool:
        col = 0 if self.column == -1 else const.NB_COLUMNS - 1
        self.hand_id_anim = self.add_animation(lst_id[0], self._main.get_coordinates_image(lst_id[0]),
                                               Images.get_piece_coordinates(self.line, col))
        for i in range(1, len(lst_id)):
            col = i if self.column == -1 else const.NB_COLUMNS - i - 1
            self.add_id_image(self.hand_id_anim, lst_id[i], self._main.get_coordinates_image(lst_id[i]),
                                               Images.get_piece_coordinates(self.line, col))
        if line is None:
            self.add_ended_callback(self.hand_id_anim, self._remove_hand)
            self.line_down = None
            self.column_down = None
        else:
            self.piece_id = lst_id[-1]
            self.line_down = line
            self.column_down = col
            self.add_ended_callback(self.hand_id_anim, self._drop)

    def _drop(self):
        if self.line_down is None or self.column_down is None:
            raise Exception("HandAnimation::_drop: événement inattendu !!??")
        self.hand_id_anim = self.add_animation(self.piece_id, self._main.get_coordinates_image(self.piece_id),
                                               Images.get_piece_coordinates(self.line_down, self.column_down))
        self.add_ended_callback(self.hand_id_anim, self._remove_hand)

    def get_id_piece(self) -> int:
        return self.piece_id

    def is_animating(self) -> bool:
        return not self.is_ended(self.hand_id_anim)



