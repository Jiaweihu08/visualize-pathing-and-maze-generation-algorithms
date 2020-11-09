import pygame
from queue import PriorityQueue
from collections import deque


def astar(draw, start, end):
	title = 'A* Algorithm'
	pygame.display.set_caption(title)
	
	q = PriorityQueue()
	q_set = set()

	count = 0
	q.put((start.dist, count, start))
	q_set.add(start)
	
	while q_set:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		curr = q.get()[-1]
		q_set.remove(curr)

		if curr == end:
			while curr.prev != start:
				curr = curr.prev
				curr.make_path()
				draw()
			pygame.display.set_caption(title+'- Path Found!')
			return True

		for neigh in curr.neighbors:
			new_g_score = curr.g_score + 1
			if neigh.g_score > new_g_score:
				neigh.g_score = new_g_score
				neigh.h_score = compute_h_score(neigh, end)
				neigh.dist = neigh.g_score + neigh.h_score
				neigh.prev = curr

				if neigh not in q_set:
					if neigh != end:
						neigh.make_frontier()

					count += 1
					q.put((neigh.dist, count, neigh))
					q_set.add(neigh)
		
		if curr != start:
			curr.make_examined()
		
		draw()
	pygame.display.set_caption(title+'- No Path Found!')
	return False


def compute_h_score(spot, end):
	x1, y1 = spot.x_id, spot.y_id
	x2, y2 = end.x_id, end.y_id
	return abs(x1 - x2) + abs(y1 - y2)


def dijkstra(draw, start, end):
	title = 'Dijkstra Algorithm'
	pygame.display.set_caption(title)

	q = set()
	q.add(start)

	while q:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		curr = min(q)
		q.remove(curr)

		if curr == end:
			while curr.prev != start:
				curr = curr.prev
				curr.make_path()
				draw()
			pygame.display.set_caption(title+'- Path Found!')
			return True

		for neighbor in curr.neighbors:
			new_dist = curr.dist + 1
			if neighbor.dist > new_dist:
				neighbor.dist = new_dist
				neighbor.prev = curr

				if neighbor != end:
					neighbor.make_frontier()
				
				q.add(neighbor)

		if curr != start:
			curr.make_examined()

		draw()
	pygame.display.set_caption(title+'- No Path Found.')
	return False


def dfs(draw, start, end):
	title = 'Depth First Search Algorithm'
	pygame.display.set_caption(title)

	stack = deque()
	stack.append(start)

	while stack:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		curr = stack.pop()

		if curr.neighbors:
			stack.append(curr)
			neighbor = curr.neighbors.pop(0)

			if neighbor == end:
				while curr.prev != start:
					curr = curr.prev
					curr.make_path()
					draw()
				pygame.display.set_caption(title+'- Path Found!')
				return True

			if neighbor.visited == False:
				neighbor.visited = True
				neighbor.prev = curr

				if neighbor != end:
					neighbor.make_frontier()
				
				stack.append(neighbor)

		if curr != start:
			curr.make_examined()

		draw()
	pygame.display.set_caption(title+'- No Path Found.')
	return False


