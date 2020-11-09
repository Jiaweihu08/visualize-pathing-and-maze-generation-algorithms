import pygame, sys
from collections import deque
from random import randint, choice


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
START = (250, 157, 0)
END = (128, 0, 128)
OPEN = (70, 130, 180)
CLOSE = (92, 192, 219)
PATH = (255, 255, 0)
GREY = (128, 128, 128)


class Spot:
	def __init__(self, i, j, cell_size, num_cells):
		self.x_id = i
		self.y_id = j
		self.x = i * cell_size
		self.y = j * cell_size

		self.color = WHITE
		self.cell_size = cell_size
		self.num_cells = num_cells
		
		self.dist = float('inf')
		self.g_score = float('inf')
		self.h_score = float('inf')
		self.prev = None
		self.visited = False

	def is_start(self):
		return self.color == START

	def is_end(self):
		return self.color == END

	def is_barrier(self):
		return self.color == BLACK

	def make_start(self):
		self.color = START
		self.dist = 0
		self.g_score = 0
		self.h_score = 0

	def make_end(self):
		self.color = END

	def make_barrier(self):
		if not self.is_start() and not self.is_end():
			self.color = BLACK

	def make_frontier(self):
		self.color = OPEN

	def make_path(self):
		self.color = PATH

	def make_examined(self):
		self.color = CLOSE

	def reset(self):
		if not self.is_start() and not self.is_end():
			self.color = WHITE
		
		self.dist = float('inf')
		self.g_score = float('inf')
		self.h_score = float('inf')
		self.prev = None
		self.visited = False

	def draw(self, screen):
		cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
		pygame.draw.rect(screen, self.color, cell)

	def update_neighbors(self, grid):
		col_max = self.num_cells[0]
		col_min = 0
		self.neighbors = []

		if self.y_id > 0 and not grid[self.x_id][self.y_id - 1].is_barrier(): # UP
			self.neighbors.append(grid[self.x_id][self.y_id - 1])
		
		if self.x_id < col_max - 1 and not grid[self.x_id + 1][self.y_id].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.x_id + 1][self.y_id])

		if self.y_id < self.num_cells[1] - 1 and not grid[self.x_id][self.y_id + 1].is_barrier(): # DOWN
			self.neighbors.append(grid[self.x_id][self.y_id + 1])

		if self.x_id > col_min and not grid[self.x_id - 1][self.y_id].is_barrier(): # LEFT
			self.neighbors.append(grid[self.x_id - 1][self.y_id])

	def __lt__(self, other):
		return self.dist < other.dist


def update_all_neighbors(grid, draw):
	for col in grid:
		for spot in col:
			spot.update_neighbors(grid)
	return grid


# ---------------- DFS Maze ----------------
class DFSMazeSpot(Spot):
	def __init__(self, i, j, cell_size, num_cells):
		Spot.__init__(self, i, j, cell_size, num_cells)
		
		self.color = GREY
		self.lines = self.get_lines()
		
		self.neighbors = []
		
		self.reachables = []

	def get_lines(self):
		p1 = (self.x, self.y)
		p2 = (self.x + self.cell_size, self.y)
		p3 = (self.x + self.cell_size, self.y + self.cell_size)
		p4 = (self.x, self.y + self.cell_size)

		lines = {'up':(p1, p2), 'down':(p3, p4),
		'left':(p1, p4), 'right':(p2, p3)}
		return lines

	def get_reachables(self, grid):
		max_x = self.num_cells[0]
		max_y = self.num_cells[1]

		self.reachables = []
		if self.x_id < max_x - 1:
			self.reachables.append(grid[self.x_id + 1][self.y_id])
		if self.x_id > 0:
			self.reachables.append(grid[self.x_id - 1][self.y_id])
		if self.y_id < max_y - 1:
			self.reachables.append(grid[self.x_id][self.y_id + 1])
		if self.y_id > 0:
			self.reachables.append(grid[self.x_id][self.y_id - 1])

	def enable(self):
		if not self.is_start() and not self.is_end():
			self.color = WHITE
		self.visited = True
	
	def reset(self):
		if not self.is_start() and not self.is_end():
			self.color = BLACK
		
		self.dist = float('inf')
		self.g_score = float('inf')
		self.h_score = float('inf')
		self.prev = None

	def draw_lines(self, screen):
		for line in self.lines.values():
			pygame.draw.line(screen, BLACK, *line, 3)

	def pint(self, screen):
		cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
		pygame.draw.rect(screen, self.color, cell)

	def draw(self, screen):
		self.pint(screen)
		self.draw_lines(screen)


def remove_wall(candidate, curr):
	if candidate.y_id - curr.y_id == 1:
		candidate.lines.pop('up', None)
		curr.lines.pop('down', None)
	
	elif candidate.y_id - curr.y_id == -1:
		candidate.lines.pop('down', None)
		curr.lines.pop('up', None)

	elif candidate.x_id - curr.x_id == 1:
		candidate.lines.pop('left', None)
		curr.lines.pop('right', None)

	elif candidate.x_id - curr.x_id == -1:
		candidate.lines.pop('right', None)
		curr.lines.pop('left', None)

	candidate.reachables.remove(curr)

	candidate.neighbors.append(curr)
	curr.neighbors.append(candidate)


def dfs_maze(grid, draw):
	begin = grid[0][0]
	begin.enable()

	stack = deque()
	stack.append(begin)

	while stack:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		curr = stack.pop()
		curr.reachables = [cand for cand in curr.reachables if cand.visited == False]

		if curr.reachables:
			stack.append(curr)
			
			idx = choice(range(len(curr.reachables)))
			candidate = curr.reachables.pop(idx)
			
			remove_wall(candidate, curr)
			candidate.enable()
			stack.append(candidate)

		draw()

	return grid


# ---------------- Recursive Division ----------------
class Chamber:
	def __init__(self, x_min, x_max, y_min, y_max, x_to_avoid=[], y_to_avoid=[]):
		self.x_min = x_min
		self.x_max = x_max
		self.y_min = y_min
		self.y_max = y_max
		
		self.x_to_avoid = x_to_avoid
		self.y_to_avoid = y_to_avoid

		self.get_wall_center()

	def get_wall_center(self):
		x_to_avoid = set(self.x_to_avoid)
		y_to_avoid = set(self.y_to_avoid)

		x_cands = [x for x in range(self.x_min + 1, self.x_max) if x not in x_to_avoid]

		y_cands = [y for y in range(self.y_min + 1, self.y_max) if y not in y_to_avoid]

		if x_cands and y_cands:
			self.center_x = choice(x_cands)
			self.center_y = choice(y_cands)
			self.is_qualified = True
		else:
			self.is_qualified = False


	def build_walls(self, grid, draw):
		for spot in grid[self.center_x][self.y_min:self.y_max + 1]:
			spot.make_barrier()
			draw()
		for col in grid[self.x_min:self.x_max + 1]:
			col[self.center_y].make_barrier()
			draw()

	def build_walls_and_open_doors(self, grid, draw):
		self.build_walls(grid, draw)
		# draw()

		self.walls = {
		'upper': [self.y_min, self.center_y - 1,
				(self.center_x, randint(self.y_min, self.center_y - 1))],

		'lower': [self.center_y + 1, self.y_max,
				(self.center_x, randint(self.center_y + 1, self.y_max))],

		'left': [self.x_min, self.center_x - 1,
				(randint(self.x_min, self.center_x - 1), self.center_y)],

		'right': [self.center_x + 1, self.x_max,
				(randint(self.center_x + 1, self.x_max), self.center_y)]
		}

		rm_wall = choice(['upper', 'lower', 'left', 'right'])
		self.walls[rm_wall][2] = (None, None)
		
		for vals in self.walls.values():
			x, y = vals[2]
			if x != None:
				grid[x][y].reset()
		draw()

	def build_sub_chambers(self, stack):
		for vert in ['lower', 'upper']:
			for horiz in ['right', 'left']:
				col_wall = self.walls[vert]
				row_wall = self.walls[horiz]

				x_min = row_wall[0]
				x_max = row_wall[1]
				y_min = col_wall[0]
				y_max = col_wall[1]
				x_to_avoid = [row_wall[2][0]]
				y_to_avoid = [col_wall[2][1]]

				if (x_max - x_min >= 3) and (y_max - y_min >= 3):
					for x in self.x_to_avoid:
						if x != None and (x_min <= x <= x_max):
							x_to_avoid.append(x)
					for y in self.y_to_avoid:
						if y != None and (y_min <= y <= y_max):
							y_to_avoid.append(y)

					sub_chamber = Chamber(
						x_min, x_max,
						y_min, y_max,
						x_to_avoid, y_to_avoid)

					stack.append(sub_chamber)


def recursive_division_maze(grid, draw, num_cells):
	num_cells_h, num_cells_v = num_cells

	begin = Chamber(0, num_cells_h - 1, 0, num_cells_v - 1)
	stack = deque([begin])

	while stack:
		chamber = stack.pop()
		if chamber.is_qualified:
			chamber.build_walls_and_open_doors(grid, draw)
			chamber.build_sub_chambers(stack)

	grid = update_all_neighbors(grid, None)

	return grid


# ---------------- Random Barriers ----------------
def random_barriers(grid, draw):
	num_cells_v, num_cells_h = len(grid), len(grid[0])
	num_barriers_per_col = num_cells_h * num_cells_v * 0.08 // num_cells_h
	for col in grid:
		num_barriers = randint(num_barriers_per_col-3, num_barriers_per_col)
		barrier_idx = set()
		while len(barrier_idx) != num_barriers:
			idx = randint(0, len(col) - 1)
			if idx not in barrier_idx:
				barrier_idx.add(idx)
				col[idx].make_barrier()
				draw()

	grid = update_all_neighbors(grid, None)

	return grid



# ----------------
def make_grid(spot_type, cell_size, num_cells):
	h_counts, v_counts = num_cells
	grid = []
	for i in range(h_counts):
		col = []
		for j in range(v_counts):
			col.append(spot_type(i, j, cell_size, num_cells))
		grid.append(col)

	if spot_type == DFSMazeSpot:
		for col in grid:
			for spot in col:
				spot.get_reachables(grid)

	return grid






