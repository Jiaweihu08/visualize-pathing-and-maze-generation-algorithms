import sys

import pygame
from pygame import Surface, KEYDOWN, K_SPACE, K_c, K_m

from grid import Grid
from menu import create_menu, menu_loop


def main(screen: Surface):
    menu = create_menu(screen)
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    num_columns = screen_width // 20
    cell_size = screen_width // num_columns
    num_rows = screen_height // cell_size

    guide_1 = "Place a START and an END on the board and press SPACE to start."
    guide_2 = "Press C to clear the screen, and M to go back to the Menu."
    pygame.display.set_caption(guide_1)

    algo_name, barrier_name = menu_loop(menu, screen)
    grid = Grid.create(algo_name, barrier_name, num_rows, num_columns, cell_size)
    solved = False
    while True:
        grid.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                grid.process_click(pos)
            if event.type == KEYDOWN:
                # Start visualization
                if event.key == K_SPACE and grid.is_ready() and not solved:
                    # Draw maze
                    grid.generate_barriers(screen)
                    # Solve path finding
                    solved = grid.find_path(screen)
                    pygame.display.set_caption(guide_2)
                # Clear
                if event.key == K_c:
                    grid.reset()
                    solved = False
                # Back to menu
                if event.key == K_m:
                    algo_name, barrier_name = menu_loop(menu, screen)
                    grid = Grid.create(
                        algo_name, barrier_name, num_rows, num_columns, cell_size
                    )
                    solved = False

                pygame.display.set_caption(guide_1)


if __name__ == "__main__":
    WIDTH: int = 1300
    HEIGHT: int = 500
    SCREEN_SIZE: (int, int) = (WIDTH, HEIGHT)

    pygame.init()
    main(pygame.display.set_mode(SCREEN_SIZE))
