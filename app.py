import pygame, sys
from time import sleep

from menu import menu_loop
from algorithms import astar, dijkstra, dfs
from mazes import Spot, DFSMazeSpot, update_all_neighbors, dfs_maze, \
			recursive_division_maze, random_barriers, make_grid



WIDTH = 1200
HEIGHT = 400
screen_size = [WIDTH, HEIGHT]

num_cells_h = WIDTH // 20
cell_size = WIDTH // num_cells_h
num_cells_v = HEIGHT // cell_size
num_cells = [num_cells_h, num_cells_v]

algo_map = {'A*': astar, "Dijkstra's": dijkstra, 'Depth First Search': dfs}
barrier_map = {'Draw it Yourself': [Spot, update_all_neighbors, 0.01],
				'Recursive Division Maze': [Spot, recursive_division_maze, 0.02],
				'DFS Maze': [DFSMazeSpot, dfs_maze, 0.02],
				'Random Obstacles': [Spot, random_barriers, 0.01]}


def get_clicked_pos(pos, cell_size):
	x, y = pos

	x_id = x // cell_size
	y_id = y // cell_size

	return x_id, y_id


def draw(grid, screen, speed=0):
	for col in grid:
		for spot in col:
			spot.draw(screen)
	
	pygame.display.update()
	if speed != 0:
		sleep(speed)


def main(screen):
	algo_name, barrier_name = menu_loop(screen)
	algorithm = algo_map[algo_name]
	spot_type, maze_func, speed = barrier_map[barrier_name]
	grid = make_grid(spot_type, cell_size, num_cells)
	start = None
	end = None

	guide_1 = 'Place a START and an END on the board and press SPACE to start.'
	guide_2 = 'Press C to crear the screen, M to back to the Menu.'
	
	pygame.display.set_caption(guide_1)

	while True:
		draw(grid, screen)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				i, j = get_clicked_pos(pos, cell_size)
				spot = grid[i][j]

				if not start and spot != end:
					spot.make_start()
					start = spot

				elif not end and spot != start:
					spot.make_end()
					end = spot

				elif spot != start and spot != end:
					spot.make_barrier()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					if maze_func == recursive_division_maze:
						grid = maze_func(grid, lambda: draw(grid, screen), num_cells)
					else:
						grid = maze_func(grid, lambda: draw(grid, screen))

					algorithm(lambda: draw(grid, screen, speed), start, end)
					pygame.display.set_caption(guide_2)

				if event.key == pygame.K_c:
					grid = make_grid(spot_type, cell_size, num_cells)
					start = None
					end = None
				
				if event.key == pygame.K_m:
					algo_name, barrier_name = menu_loop(screen)
					algorithm = algo_map[algo_name]
					spot_type, maze_func, speed = barrier_map[barrier_name]

					grid = make_grid(spot_type, cell_size, num_cells)
					start = None
					end = None
					
					pygame.display.set_caption(guide_1)



if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode(screen_size)

	main(screen)







