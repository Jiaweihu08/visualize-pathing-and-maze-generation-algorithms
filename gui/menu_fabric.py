from abc import ABC, abstractmethod
from typing import Type, TypeVar

from pygame.font import Font

from gui.barrier_item import BarrierItem
from gui.menu import Menu
from gui.menu_component import MenuComponent
from gui.menu_item import MenuItem
from gui.pathing_item import PathingItem
from gui.start_item import StartItem
from algorithms.utils import Colors


T = TypeVar("T", bound=MenuComponent)


class AbstractMenuFabric(ABC):
    @abstractmethod
    def create_menu(self, item_name: str, center: (int, int)) -> Menu:
        pass

    @abstractmethod
    def create_title_item(self, item_name: str, center: (int, int)) -> MenuItem:
        pass

    @abstractmethod
    def create_pathing_item(self, item_name: str, center: (int, int)) -> PathingItem:
        pass

    @abstractmethod
    def create_barrier_item(self, item_name: str, center: (int, int)) -> BarrierItem:
        pass

    @abstractmethod
    def create_start_item(self, item_name: str, center: (int, int)) -> StartItem:
        pass


class MenuFabric(AbstractMenuFabric):
    def __init__(self, title_font: Font, option_font: Font) -> None:
        self.title_font = title_font
        self.option_font = option_font

    def create_menu(self, item_name: str, center: (int, int)) -> Menu:
        return create(item_name, center, self.title_font, Menu)

    def create_title_item(self, item_name: str, center: (int, int)) -> MenuItem:
        return create(item_name, center, self.title_font, MenuItem)

    def create_pathing_item(self, item_name: str, center: (int, int)) -> PathingItem:
        return create(item_name, center, self.option_font, PathingItem)

    def create_barrier_item(self, item_name: str, center: (int, int)) -> BarrierItem:
        return create(item_name, center, self.option_font, BarrierItem)

    def create_start_item(self, item_name: str, center: (int, int)) -> StartItem:
        return create(item_name, center, self.title_font, StartItem)


def create(item_name: str, center: (int, int), font: Font, cls: Type[MenuItem]) -> T:
    item_surface = font.render(item_name, True, Colors.BLACK.value)
    center_x, y = center
    x = center_x - item_surface.get_width() // 2
    return cls(item_name, item_surface, x, y)
