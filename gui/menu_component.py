from abc import ABC

from pygame import Surface


class MenuComponent(ABC):
    def get_name(self) -> str:
        raise NotImplementedError

    def add(self, menu_component: "MenuComponent") -> None:
        raise NotImplementedError

    def remove(self, menu_component: "MenuComponent") -> None:
        raise NotImplementedError

    def print(self, screen: Surface) -> None:
        raise NotImplementedError

    def update_selection(self, clicked_pos: (int, int)) -> None:
        raise NotImplementedError

    def set_pathing_item(self, pathing_item: "MenuComponent") -> None:
        raise NotImplementedError

    def set_barrier_item(self, barrier_item: "MenuComponent") -> None:
        raise NotImplementedError

    def set_start(self) -> None:
        raise NotImplementedError

    def set_owner(self, owner: "MenuComponent") -> None:
        raise NotImplementedError

    def is_ready(self) -> bool:
        raise NotImplementedError

    def selections(self) -> (str, str):
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError
