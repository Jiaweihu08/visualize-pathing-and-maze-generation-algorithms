import pygame
from pygame import Surface

from gui.menu_component import MenuComponent
from algorithms.utils import Colors


def _get_points(x: int, y: int, surface: Surface) -> list[(int, int)]:
    surface_width = surface.get_width()
    surface_height = surface.get_height()
    top_left = (x, y)
    top_right = (x + surface_width, y)
    bottom_left = (x, y + surface_height)
    bottom_right = (x + surface_width, y + surface_height)
    return [top_left, top_right, bottom_right, bottom_left]


class MenuItem(MenuComponent):
    def __init__(self, name: str, surface: Surface, x: int, y: int) -> None:
        self.name: str = name
        self.surface: Surface = surface
        self.x: int = x
        self.y: int = y
        self.owner: MenuComponent | None = None
        self.is_selected: bool = False
        self.points: list[(int, int)] = _get_points(x, y, surface)

    def get_name(self) -> str:
        return self.name

    def set_owner(self, owner: MenuComponent) -> None:
        self.owner = owner

    def print(self, screen: Surface) -> None:
        screen.blit(self.surface, (self.x, self.y))
        if self.is_selected:
            pygame.draw.lines(screen, Colors.BLACK.value, True, self.points, 2)

    def update_selection(self, clicked_pos: (int, int)) -> None:
        x, y = clicked_pos
        is_selected_x = self.x <= x <= self.x + self.surface.get_width()
        is_selected_y = self.y <= y <= self.y + self.surface.get_height()
        self.is_selected = self.is_selected or (is_selected_x and is_selected_y)

    def reset(self) -> None:
        self.is_selected = False
