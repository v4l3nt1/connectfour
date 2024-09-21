import pygame, math
from View.ConnectFour import ConnectFour


class Animation:
    """
    Classe gérant l'animation d'une image.
    On doit pouvoir lui accrocher d'autres images pour faire une
    animation d'un groupe d'images... (le vecteur de déplacements étant les mêmes)
    """
    def __init__(self, main: ConnectFour):
        """
        Initialisation de la classe gérant les animations

        :param main: fenêtre/classe gérant l'affichage et le stockage des images
        """
        self._anims = {}
        self._nb_calls = {}
        # Format des rotations
        # [ image, angle, inc_angle, final_angle ]
        self._rotations = {}
        self._delay = 10
        self._main = main
        # Le format des images ajoutées est une liste du type [(id_img, coords_actuelles, coords_finales), ... ]
        self._added = {}
        # Format des rotations des images ajoutées :
        # { idx: [img, angle, inc_angle, final_angle] } où idx : indice dans la liste précédente (_added)
        self._added_rotations = {}
        # Fonctions à appeler quand l'animation est terminée
        self._callback_end = {}


    def add_new_animation(self, image: pygame.Surface, from_coord: tuple, to_coord: tuple, delay: int = 500,
                          rotate: int = None, center: tuple = None) -> int:
        """
        Ajoute une nouvelle animation à partir d'une image

        :param image: Image à animer
        :param from_coord: Coordonnées de départ de l'image
        :param to_coord: Coordonnées de la position finale de l'image
        :param rotate: Rotation à animer sur l'image (par défaut None)
        :param center: Centre de rotation (par rapport au centre de l'image)
        :param delay: Durée de l'animation (en ms)
        :return: Identifiant de l'animation
        """
        id_img = self._main.add_image(image, from_coord)
        return self.add_animation(id_img, from_coord, to_coord, delay, rotate=rotate, center=center)

    def add_image(self, id_anim: int, image: pygame.Surface, coord: tuple, to_coord: tuple, rotation: int = None,
                  center: tuple = None) -> int:
        """
        Ajoute une image à une animation existante. Cette image suivra le même déplacement que celle de base
        de l'animation, en fonction de sa position de départ.

        Il faut que le vecteur (position initiale, position finale) de cette image soit le même que l'image
        de base de l'animation, sinon l'animation risque d'être désordonnée

        :param id_anim: Identifiant de l'animation
        :param image: Image à ajouter à l'animation
        :param coord: Coordonnées de départ de l'image
        :param to_coord: Coordonnées de la position finale de l'image
        :param rotation: Rotation à appliquer pendant l'animation
        :param center: Centre de rotation
        :return: Identifiant de l'image ajoutée
        """
        id_img = self._main.add_image(image, coord)
        self.add_id_image(id_anim, id_img, coord, to_coord, rotation=rotation, center=center)
        return id_img

    def add_id_image(self, id_anim: int, id_img: int, coord: tuple, to_coord: tuple, rotation: int = None,
                     center: tuple = None) -> None:
        """
        Ajoute une image à une animation existante. Cette image suivra le même déplacement que celle de base
        de l'animation, en fonction de sa position de départ.

        Il faut que le vecteur (position initiale, position finale) de cette image soit le même que l'image
        de base de l'animation, sinon l'animation risque d'être désordonnée

        :param id_anim: Identifiant de l'animation
        :param id_img: Identifiant de l'image à ajouter
        :param coord: Coordonnées de départ de l'image à ajouter
        :param to_coord: Position finale de l'image à ajouter
        :param rotation: Rotation à appliquer pendant l'animation
        :param center: Centre de rotation
        :return: Rien
        """
        if id_anim in self._added:
            idx = len(self._added[id_anim])
            self._added[id_anim].append([id_img, coord, to_coord])
        else:
            idx = 0
            self._added[id_anim] = [[id_img, coord, to_coord]]

        if rotation is not None:
            if id_anim in self._added_rotations:
                self._added_rotations[id_anim][idx] = [self._main.get_image(id_img), 0,
                                                       rotation / self._nb_calls[id_anim], rotation, center]
            else:
                self._added_rotations[id_anim] = {idx: [self._main.get_image(id_img), 0,
                                                        rotation / self._nb_calls[id_anim], rotation, center]}

    def add_ended_callback(self, id_anim: int, fn: callable, *params: list) -> None:
        # print("Callback : id_anim =", id_anim, ", fn =", fn)
        self._callback_end[id_anim] = (fn, params)
        # print(self._callback_end)

    def add_animation(self, id_img: int, from_coord: tuple, to_coord: tuple, delay: int = 500, rotate: float = None,
                      center: tuple = None) -> int:
        """
        Ajoute une nouvelle animation à partir d'une image

        :param id_img: Identifiant de l'image
        :param from_coord: Position de départ de l'image
        :param to_coord: Position finale de l'image après animation
        :param rotate: Rotation à appliquer à l'image (par défaut None)
        :param center: Centre de rotation
        :param delay: Durée de l'animation (en ms)
        :return: Identifiant de l'animation
        """
        id_timer = (max(self._anims.keys()) if len(self._anims) > 0 else pygame.USEREVENT) + 1
        nb_call = delay / self._delay
        self._nb_calls[id_timer] = nb_call
        _xdeb, _ydeb = from_coord
        _xfin, _yfin = to_coord
        _dx, _dy = (_xfin - _xdeb) / nb_call, (_yfin - _ydeb) / nb_call
        if rotate is not None:
            _delta_rotate = rotate / nb_call
            self._rotations[id_timer] = [ self._main.get_image(id_img), 0, _delta_rotate, rotate, center]
        # print(f"nb_call = {nb_call}")
        pygame.time.set_timer(id_timer, self._delay)
        self._anims[id_timer] = [id_img, from_coord, to_coord, (_dx, _dy)]
        return id_timer

    def anime(self, id_timer: int) -> None:
        """
        Méthode déplaçant/animant l'animation repérée par son identifiant

        :param id_timer: Identifiant de l'animation
        :return: Rien
        """
        # print("Playing animation :", id_timer, self._callback_end)
        if id_timer not in self._anims:
            return None # Ce cas peut arriver si le timer est déjà dans la liste des événements à traiter alors
        # qu'on vient de mettre le timer à 0
        id_img, (_xd, _yd), (_xf, _yf), (_dx, _dy) = self._anims[id_timer]
        _xd += _dx
        _yd += _dy
        if abs(_xd - _xf) + abs(_yd - _yf) < 1e-2:
            # Fin de l'animation
            # print("*** Fin de l'animation ***")
            if id_timer in self._rotations:
                # Inconvénient : l'image est modifiée!
                # Il faut la supprimer et ajouter la nouvelle version après rotation...
                # PROBLEME : On doit appliquer la rotation sur l'image SOURCE !
                # Il faut donc mémoriser l'image source...
                # --> Créer un dictionnaire d'images dans la classe Animation.
                image, angle, inc_angle, final_angle, center = self._rotations[id_timer]
                _img = pygame.transform.rotate(image, final_angle)
                # Calcul du decalage si le centre n'est pas celui de l'image
                if center is not None:
                    final_angle *= math.pi / 180.0
                    # _xf += center[0]*math.cos(final_angle) - center[1]*math.sin(final_angle) - center[0]
                    # _yf += center[0]*math.sin(final_angle) + center[1]*math.cos(final_angle) - center[1]
                self._main.replace_image(id_img, _img, (_xf, _yf))
                del self._rotations[id_timer]
            else:
                self._main.set_coordinates_image(id_img, (_xf, _yf))
            pygame.time.set_timer(id_timer, 0)
            if id_timer in self._added:
                idx = 0
                for id_img, _, to_coord in self._added[id_timer]:
                    if id_timer in self._added_rotations and idx in self._added_rotations[id_timer]:
                        img, _, _, final_angle, center = self._added_rotations[id_timer][idx]
                        _img = pygame.transform.rotate(img, final_angle)
                        if center is not None:
                            final_angle *= math.pi / 180.0
                            # to_coord[0] += center[0] * math.cos(final_angle)\
                            #                - center[1] * math.sin(final_angle) - center[0]
                            # to_coord[1] += center[0] * math.sin(final_angle)\
                            #                + center[1] * math.cos(final_angle) - center[1]
                        self._main.replace_image(id_img, _img, to_coord)
                    else:
                        self._main.set_coordinates_image(id_img, to_coord)
                del self._added[id_timer]
            if id_timer in self._added_rotations:
                del self._added_rotations[id_timer]
            # Appel de l'éventuelle fonction callback
            # print(self._callback_end)
            if id_timer in self._callback_end:
                # print(self._callback_end[id_timer][0])
                # print(self._callback_end[id_timer][1])
                self._callback_end[id_timer][0](*self._callback_end[id_timer][1])
                del self._callback_end[id_timer]
                # print("deleting _callback_end :", self._callback_end)
            # A METTRE EN DERNIER !!
            del self._anims[id_timer]
        else:
            self._anims[id_timer][1] = _xd, _yd
            if id_timer in self._rotations:
                img, angle, inc_angle, _, center = self._rotations[id_timer]
                angle += inc_angle
                self._rotations[id_timer][1] = angle
                img2 = pygame.transform.rotate(img, angle)
                if center is not None:
                    angle *= math.pi / 180.0
                    __dx = (center[0]*math.cos(angle) + center[1]*math.sin(angle)) - center[0]
                    __dy = (-center[0]*math.sin(angle) + center[1]*math.cos(angle)) - center[1]
                    # _xd += __dx
                    # _yd += -__dy
                    print(angle, math.cos(angle), math.sin(angle), __dx, __dy, center)
                self._main.replace_image(id_img, img2, (_xd, _yd))
            else:
                self._main.set_coordinates_image(id_img, (_xd, _yd))
            if id_timer in self._added:
                lst = self._added[id_timer]
                for i in range(len(lst)):
                    id_img, (x, y), _ = lst[i]
                    x += _dx
                    y += _dy
                    lst[i][1] = x, y
                    if id_timer in self._added_rotations and i in self._added_rotations[id_timer]:
                        img, angle, inc_angle, _, center = self._added_rotations[id_timer][i]
                        angle += inc_angle
                        self._added_rotations[id_timer][i][1] = angle
                        img2 = pygame.transform.rotate(img, angle)
                        self._main.replace_image(id_img, img2, (x, y))
                    else:
                        self._main.set_coordinates_image(id_img, (x, y))
        self._main.set_refresh()

    def get_image_id(self, id_anim: int) -> int:
        return self._anims[id_anim][0]

    def is_ended(self, id_anim: int) -> bool:
        return id_anim not in self._anims
