import pygame, sys


WIDTH = 1200
HEIGHT = 400
screen_size = [WIDTH, HEIGHT]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.font.init()
option_font = pygame.font.SysFont('Verdana', 15)
title_font = pygame.font.SysFont('Verdana', 20)
title_font.set_underline(True)


title_names = ['Visualizing Path Finding Algorithms',
				'Algorigthms',
				'Barriers',
				'Start']

algo_names = ['A*', "Dijkstra's", 'Depth First Search']

barrier_names = ['Draw it Yourself', 'Recursive Division Maze',
					'DFS Maze', 'Random Obstacles']


class MenuElement:
	def __init__(self, surface, name, pos):
		self.surface = surface
		self.x, self.y = pos
		self.name = name

	def show(self, screen, selected_item):
		screen.blit(self.surface, (self.x, self.y))


class ClickableElement(MenuElement):
	def __init__(self, surface, name, pos):
		MenuElement.__init__(self, surface, name, pos)
		
		self.get_rect()

	def get_rect(self):
		self.width = self.surface.get_width()
		self.height = self.surface.get_height()

		p1 = (self.x, self.y)
		p2 = (self.x + self.width, self.y)
		p3 = (self.x + self.width, self.y + self.height)
		p4 = (self.x, self.y + self.height)

		self.lines = [p1, p2, p3, p4]

	def show(self, screen, selected_item):
		if self.name in selected_item:
			pygame.draw.lines(screen, BLACK, True, self.lines, 2)
		screen.blit(self.surface, (self.x, self.y))

	def is_selected(self, clicked_pos):
		x, y = clicked_pos

		selected_x = self.x <= x <= self.x + self.width
		selected_y = self.y <= y <= self.y + self.height

		if selected_x and selected_y:
			return True
		return False


# ------------------------ Define title surfaces ans positions ------------------------
titles = [title_font.render(title, True, BLACK) for title in title_names]
title_pos = [[WIDTH//2, HEIGHT//8],
				[WIDTH//4, HEIGHT//4],
				[WIDTH//4*3, HEIGHT//4],
				[WIDTH//2, HEIGHT//4*3]]
for i in range(len(titles)):
	title_pos[i][0] -= titles[i].get_width()//2


# ------------------------ Define algorithm surfaces ans positions ------------------------
algo_options = [option_font.render(option, True, BLACK) for option in algo_names]
algo_x = title_pos[1][0]
algo_y = title_pos[1][1] + 30
algo_pos = []
for i in range(len(algo_options)):
	algo_pos.append([algo_x, algo_y])
	algo_y += 25


# ------------------------ Define barrier surfaces ans positions ------------------------
barrier_options = [option_font.render(option, True, BLACK) for option in barrier_names]
barrier_x = title_pos[2][0]
barrier_y = title_pos[2][1] + 30
barrier_pos = []
for i in range(len(barrier_options)):
	barrier_pos.append([barrier_x, barrier_y])
	barrier_y += 25


# ------------------------ Creating objects for unclickables menu elements ------------------------
unclickables = []
for surf, name, pos in zip(titles[:-1], title_names[:-1], title_pos[:-1]):
	unclickables.append(MenuElement(surf, name, pos))


# ------------------------ Creating objects for clickables menu elements ------------------------
clickable_items = algo_options + barrier_options + [titles[-1]]
clickable_item_names = algo_names + barrier_names + [title_names[-1]]
clickable_item_pos = algo_pos + barrier_pos + [title_pos[-1]]
clickables = []
for surf, name, pos in zip(clickable_items, clickable_item_names, clickable_item_pos):
	clickables.append(ClickableElement(surf, name, pos))


def display_menu(screen, selected_items,
				clickables=clickables, unclickables=unclickables):
	
	screen.fill(WHITE)

	for item in unclickables + clickables:
		item.show(screen, selected_items)

	pygame.display.update()


def update_selected_items(pos, selected_items, clickables=clickables, barrier_x=barrier_x):
	start = clickables[-1]
	
	if start.is_selected(pos):
		return True, selected_items

	elif pos[0] >= barrier_x:
		candidates = clickables[len(algo_names):-1]
		for cand in candidates:
			if cand.is_selected(pos):
				selected_items[1] = cand.name
	else:
		candidates = clickables[:len(algo_names)]
		for cand in candidates:
			if cand.is_selected(pos):
				selected_items[0] = cand.name

	return False, selected_items


def menu_loop(screen):
	selected_items = ["A*", 'Draw it Yourself']
	start = False
	
	while start == False:
		display_menu(screen, selected_items)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				start, selected_items = update_selected_items(pos, selected_items)
				
	return selected_items


if __name__ == "__main__":
	screen = pygame.display.set_mode(screen_size)
	menu_loop(screen)




