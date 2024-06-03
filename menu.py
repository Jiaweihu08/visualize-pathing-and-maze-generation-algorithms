import sys

import pygame
from pygame import Surface

from gui.menu import Menu
from gui.menu_fabric import MenuFabric


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


def create_menu(screen: Surface) -> Menu:
    menu_fabric = MenuFabric(TITLE_FONT, OPTION_FONT)
    w, h = screen.get_width(), screen.get_height()

    title_center = (w // 2, h // 8)
    menu = menu_fabric.create_menu("Visualizing Path Finding Algorithms", title_center)

    pathing_center = (w // 4, h // 4)
    pathing_title_item = menu_fabric.create_title_item(
        "Pathing Algorithms", pathing_center
    )
    menu.add(pathing_title_item)
    pathing_title_item.set_owner(menu)

    pathing_options = ["A*", "Dijkstra's", "Depth First Search"]
    for item_name in pathing_options:
        pathing_center = (pathing_center[0], pathing_center[1] + 30)
        pathing_item = menu_fabric.create_pathing_item(item_name, pathing_center)
        menu.add(pathing_item)
        pathing_item.set_owner(menu)

    barrier_center = (w // 4 * 3, h // 4)
    barrier_title_item = menu_fabric.create_title_item("Barriers", barrier_center)
    menu.add(barrier_title_item)
    barrier_title_item.set_owner(menu)
    barrier_options = [
        "Draw it yourself",
        "Recursive Division Maze",
        "DFS Maze",
        "Random Obstacles",
    ]
    for item_name in barrier_options:
        barrier_center = (barrier_center[0], barrier_center[1] + 30)
        barrier_item = menu_fabric.create_barrier_item(item_name, barrier_center)
        menu.add(barrier_item)
        barrier_item.set_owner(menu)

    start_center = (w // 2, h // 4 * 3)
    start_item = menu_fabric.create_start_item("Start", start_center)
    menu.add(start_item)
    start_item.set_owner(menu)

    return menu


def menu_loop(menu: Menu, screen: Surface) -> (str, str):
    while not menu.start:
        menu.print(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                menu.update_selection(pos)
    pathing, barrier = menu.selections()
    return _map[pathing], _map[barrier]


if __name__ == "__main__":
    _screen = pygame.display.set_mode((1200, 400))
    _menu = create_menu(_screen)
    _pathing, _barrier = menu_loop(_menu, _screen)
    print(_pathing, _barrier)
