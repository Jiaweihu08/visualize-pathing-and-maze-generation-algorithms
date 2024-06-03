import pygame
from pygame import Surface

from gui.menu_component import MenuComponent
from gui.menu_item import MenuItem
from algorithms.utils import Colors


class Menu(MenuItem):
    def __init__(self, name: str, surface: Surface, x: int, y: int) -> None:
        super().__init__(name, surface, x, y)
        self.menu_items: list[MenuComponent] = []
        self.pathing_item: MenuComponent | None = None
        self.barrier_item: MenuComponent | None = None
        self.start: bool = False

    def add(self, menu_component: MenuComponent) -> None:
        self.menu_items.append(menu_component)

    def remove(self, menu_component: MenuComponent) -> None:
        self.menu_items.remove(menu_component)

    def print(self, screen: Surface) -> None:
        screen.fill(Colors.WHITE.value)
        screen.blit(self.surface, (self.x, self.y))
        for item in self.menu_items:
            item.print(screen)
        pygame.display.update()

    def update_selection(self, clicked_pos: (int, int)) -> None:
        for item in self.menu_items:
            item.update_selection(clicked_pos)

    def set_pathing_item(self, pathing_item: MenuComponent) -> None:
        if self.pathing_item is not None and self.pathing_item is not pathing_item:
            self.pathing_item.is_selected = False
        self.pathing_item = pathing_item

    def set_barrier_item(self, barrier_item: MenuComponent) -> None:
        if self.barrier_item is not None and self.barrier_item is not barrier_item:
            self.barrier_item.is_selected = False
        self.barrier_item = barrier_item

    def set_start(self) -> None:
        self.start = True

    def is_ready(self) -> bool:
        return self.pathing_item is not None and self.barrier_item is not None

    def selections(self) -> (str, str):
        pathing_name = self.pathing_item.get_name()
        barrier_name = self.barrier_item.get_name()
        self.reset()
        return pathing_name, barrier_name

    def reset(self) -> None:
        self.start = False
        self.pathing_item = None
        self.barrier_item = None
        for item in self.menu_items:
            item.reset()
