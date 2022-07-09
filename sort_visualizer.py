import pygame
import random
from itertools import cycle
from sorters import bubble_sort, insertion_sort, selection_sort, quick_sort

DARK = 33, 33, 33
LIGHT = 255, 255, 255
PINK = 233, 30, 99
YELLOW = 255, 235, 59
CYAN = 0, 188, 212

GREY = 158, 158, 158
GREEN = 0, 255, 0
RED = 255, 0, 0

GRADIENT = (YELLOW, CYAN, PINK)

WIDTH = 700
HEIGHT = 600
MARGIN = 50

SORTERS = {
	'Bubble Sort': bubble_sort,
	'Insertion Sort': insertion_sort,
	'Selection Sort': selection_sort,
	'Quick Sort': quick_sort,
}

algorithms = cycle(SORTERS)

class RandList:
	def __init__(self, count, min_val, max_val):
		self.count = count 
		self.min_val = min_val
		self.max_val = max_val
		self._list = []
		self.algorithm = None
		self.randomize()

	def randomize(self):
		self._list = [random.randint(self.min_val, self.max_val) for _ in range(self.count)]

	def sort(self, ascending):
		if self.algorithm is None:
			return 
		self._list, all_sorted = self.algorithm(self._list, ascending)
		return all_sorted

	@property
	def items(self):
		for i, v in enumerate(self._list):
			yield i, v

	@property
	def min(self):
		return min(self._list)

	@property
	def max(self):
		return max(self._list)

	@property
	def len(self):
		return len(self._list)


class Visualizer:
	WIDTH = WIDTH
	HEIGHT = HEIGHT

	BG_COLOR = DARK
	XMARGIN = MARGIN
	YMARGIN = 3*MARGIN

	def __init__(self, lst):
		self.lst = lst
		self.sorting = False
		self.ascending = True 
		self.algo_name = 'None'
		self.started_time = 0
		self.counter = 0

		self.font = pygame.font.SysFont('comicsans', 20)
		self.title_font = pygame.font.SysFont('comicsans', 40)
		self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption('Sorting Visualizer')

	def select_algorithm(self, algo_name):
		self.algo_name = algo_name 
		self.lst.algorithm = SORTERS[algo_name]

	def draw_list(self):
		self.bar_width = (self.WIDTH - self.XMARGIN*2) // self.lst.len
		self.bar_scale = (self.HEIGHT - self.YMARGIN) // (self.lst.max - self.lst.min) 

		for index, value in self.lst.items:
			x = self.XMARGIN + index * self.bar_width
			y = self.HEIGHT - (value-self.lst.min)*self.bar_scale
			color = GRADIENT[index%3]

			pygame.draw.rect(self.window, GREEN, (x, self.YMARGIN+20, self.bar_width, self.HEIGHT), 1)
			pygame.draw.rect(self.window, color, (x, y, self.bar_width, self.HEIGHT))

	def draw_text(self, txt, color, x, y, title=False):
		font = self.title_font if title else self.font 
		text = font.render(txt, 1, color)
		if x == 'c':
			x = self.WIDTH//2 - text.get_width()//2
		elif x == 'l':
			x = self.XMARGIN
		elif x == 'r':
			x = self.WIDTH - self.XMARGIN - text.get_width()
		self.window.blit(text, (x, y))

	def refresh(self):
		self.sorting = False
		self.counter = 0
		self.lst.randomize()

	def start_sorting(self):
		if self.counter > 0:
			return
		self.sorting = True
		self.started_time = pygame.time.get_ticks()

	def process_sorting(self):
		all_sorted = self.lst.sort(self.ascending)
		self.counter = pygame.time.get_ticks() - self.started_time
		if all_sorted:
			self.sorting = False

	def display_info(self):
		mode = 'A' if self.ascending else 'D'
		self.draw_text(f"{self.algo_name} ({mode})", YELLOW, 'l', 5, True)
		self.draw_text(f"[ {self.counter} ]", GREEN, 'r', 5, True )
		self.draw_text("R-refresh | SPACE-solve | M-mode", LIGHT, 'c', self.YMARGIN-55)
		self.draw_text("A-ascending | D-descending", LIGHT, 'c', self.YMARGIN-25)
		

	def update_display(self):
		self.window.fill(self.BG_COLOR)
		self.display_info()
		self.draw_list()
		pygame.display.update()


def main(count, min_val, max_val):
	pygame.init()

	lst = RandList(count, min_val, max_val)
	viz = Visualizer(lst)
	viz.select_algorithm(next(algorithms))

	running = True
	clock = pygame.time.Clock()

	while running:
		clock.tick(60)
		viz.update_display()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				viz.refresh()

			if viz.sorting:
				continue

			if event.key == pygame.K_SPACE:
				viz.start_sorting()
			elif event.key == pygame.K_a:
				viz.ascending = True
			elif event.key == pygame.K_d:
				viz.ascending = False
			elif event.key == pygame.K_m:
				viz.select_algorithm(next(algorithms))

		if viz.sorting:
			viz.process_sorting()

	pygame.quit()

if __name__ == '__main__':
	count = 50
	min_val = 1
	max_val = 100
	main(count, min_val, max_val)
