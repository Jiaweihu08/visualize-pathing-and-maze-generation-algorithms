import sys

import pygame
from pygame import Surface, KEYDOWN, K_SPACE, K_c, K_m

from grid import Grid
from menu import menu_loop


def main(screen: Surface):
	screen_width = screen.get_width()
	screen_height = screen.get_height()
	num_cells_h = screen_width // 20
	cell_size = screen_width // num_cells_h
	num_cells_v = screen_height // cell_size

	guide_1 = 'Place a START and an END on the board and press SPACE to start.'
	guide_2 = 'Press C to clear the screen, and M to go back to the Menu.'
	pygame.display.set_caption(guide_1)

	algo_name, barrier_name = menu_loop(screen)
	grid = Grid.create(algo_name, barrier_name, num_cells_h, num_cells_v, cell_size)

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
				if event.key == K_SPACE and grid.is_ready():
					# Draw maze
					grid.draw_barriers()
					# Solve path finding
					grid.find_path()
					pygame.display.set_caption(guide_2)
				# Clear
				if event.key == K_c:
					grid.reset()
				# Back to menu
				if event.key == K_m:
					algo_name, barrier_name = menu_loop(screen)
					grid = Grid.create(algo_name, barrier_name, num_cells_h, num_cells_v, cell_size)

				pygame.display.set_caption(guide_1)


if __name__ == "__main__":
	WIDTH: int = 1200
	HEIGHT: int = 400
	SCREEN_SIZE: (int, int) = (WIDTH, HEIGHT)

	pygame.init()
	main(pygame.display.set_mode(SCREEN_SIZE))
