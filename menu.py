from dataclasses import dataclass
import sys

import pygame
from pygame import Surface
from pygame.font import Font

from algorithms.utils import Colors


pygame.font.init()
TITLE_FONT = pygame.font.SysFont("Verdana", 20)
TITLE_FONT.set_underline(True)
OPTION_FONT = pygame.font.SysFont("Verdana", 15)

_map = {
    "A*": "a*",
    "Dijkstra's": "dijkstra",
    "Depth First Search": "dfs",
    "Draw it yourself": "diy",
    "Recursive Division Maze": "recursive_division_maze",
    "DFS Maze": "dfs",
    "Random Obstacles": "random",
}


class MenuItem:
    def __init__(
        self, name: str, surface: Surface, x: int, y: int, is_clickable: bool
    ) -> None:
        self.name: str = name
        self.surface: Surface = surface
        self.x: int = x
        self.y: int = y
        self.is_clickable: bool = is_clickable

        surface_width = self.surface.get_width()
        surface_height = self.surface.get_height()

        top_left = (self.x, self.y)
        top_right = (self.x + surface_width, self.y)
        bottom_left = (self.x, self.y + surface_height)
        bottom_right = (self.x + surface_width, self.y + surface_height)
        self.points: list[(int, int)] = [top_left, top_right, bottom_right, bottom_left]

    @classmethod
    def create(
        cls, item_name: str, center: (int, int), font: Font, is_clickable: bool
    ) -> "MenuItem":
        item_surface = font.render(item_name, True, (0, 0, 0))
        center_x, y = center
        x = center_x - item_surface.get_width() // 2
        return cls(item_name, item_surface, x, y, is_clickable)

    def show(self, screen: Surface, is_selected: bool) -> None:
        screen.blit(self.surface, (self.x, self.y))
        if is_selected:
            pygame.draw.lines(screen, Colors.BLACK.value, True, self.points, 2)

    def is_selected(self, clicked_pos: (int, int)) -> bool:
        if self.is_clickable:
            x, y = clicked_pos
            is_selected_x = self.x <= x <= self.x + self.surface.get_width()
            is_selected_y = self.y <= y <= self.y + self.surface.get_height()
            return is_selected_x and is_selected_y
        return False


def _get_item_column(
    column_title: str,
    column_start_position: (int, int),
    options: list[str],
    line_space: int = 30,
) -> (MenuItem, list[MenuItem]):
    center_x, center_y = column_start_position
    title_item = MenuItem.create(
        column_title, column_start_position, TITLE_FONT, column_title == "Start"
    )
    option_items = []
    for option_name in options:
        center_y += line_space
        item = MenuItem.create(option_name, (center_x, center_y), OPTION_FONT, True)
        option_items.append(item)
    return title_item, option_items


@dataclass
class Menu:
    screen: Surface
    title_item: MenuItem
    pathing_title_item: MenuItem
    pathing_algorithm_items: list[MenuItem]
    barrier_title_item: MenuItem
    barrier_items: list[MenuItem]
    start_item: MenuItem
    _selected_algo: str = "A*"
    _selected_barrier: str = "Draw it yourself"
    _start: bool = False

    @classmethod
    def from_screen(cls, screen: Surface) -> "Menu":
        w, h = screen.get_width(), screen.get_height()
        title_item, _ = _get_item_column(
            "Visualizing Path Finding Algorithms", (w // 2, h // 8), []
        )
        pathing_title_item, pathing_items = _get_item_column(
            "Pathing Algorithms",
            (w // 4, h // 4),
            ["A*", "Dijkstra's", "Depth First Search"],
        )
        barrier_title_item, barrier_items = _get_item_column(
            "Barriers",
            (w // 4 * 3, h // 4),
            [
                "Draw it yourself",
                "Recursive Division Maze",
                "DFS Maze",
                "Random Obstacles",
            ],
        )
        start_item, _ = _get_item_column("Start", (w // 2, h // 4 * 3), [])
        return cls(
            screen=screen,
            title_item=title_item,
            pathing_title_item=pathing_title_item,
            pathing_algorithm_items=pathing_items,
            barrier_title_item=barrier_title_item,
            barrier_items=barrier_items,
            start_item=start_item,
        )

    def show(self) -> None:
        self.screen.fill(Colors.WHITE.value)
        self.title_item.show(self.screen, False)
        self.pathing_title_item.show(self.screen, False)
        for algo_item in self.pathing_algorithm_items:
            algo_item.show(self.screen, algo_item.name == self._selected_algo)
        self.barrier_title_item.show(self.screen, False)
        for barrier_item in self.barrier_items:
            barrier_item.show(self.screen, barrier_item.name == self._selected_barrier)
        self.start_item.show(self.screen, False)
        pygame.display.update()

    def update_selected_items(self, clicked_pos: (int, int)) -> None:
        if self.start_item.is_selected(clicked_pos):
            # Start visualizer with current selections
            self._start = True
        else:
            for barrier in self.barrier_items:
                if barrier.is_selected(clicked_pos):
                    # Update pathing algorithm
                    self._selected_barrier = barrier.name
                    break
            else:
                for algo in self.pathing_algorithm_items:
                    if algo.is_selected(clicked_pos):
                        # Update barrier
                        self._selected_algo = algo.name
                        break

    @property
    def start(self) -> bool:
        return self._start

    @property
    def selections(self) -> (str, str):
        return _map.get(self._selected_algo), _map.get(self._selected_barrier)


def menu_loop(screen: Surface) -> (str, str):
    menu = Menu.from_screen(screen)
    while not menu.start:
        menu.show()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                menu.update_selected_items(pos)
    return menu.selections


if __name__ == "__main__":
    menu_loop(pygame.display.set_mode((1200, 400)))
