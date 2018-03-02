import random

class Grid():
	n = property(lambda self: self.__n)
	table = property(lambda self: self.__table)

	def __init__(self, n = 3):
		self.__n = n
		self.__table = [[((i * n + i // n + j) % (n * n) + 1) for i in range(n ** 2)] for j in range(n ** 2)]
	
	def showGrid(self):
		print("=" * 30)
		for i in range(self.n * self.n):
			print(self.__table[i])
		print("=" * 30)

	def transposeGrid(self):
		self.__table = list(map(list, zip(*self.__table)))

	def swapRowsInArea(self):

		line1, line2 = random.sample(range(self.__n), 2)
		area = random.randrange(self.__n)

		N1 = area * self.__n + line1
		N2 = area * self.__n + line2
		
		self.__table[N1], self.__table[N2] = self.__table[N2], self.__table[N1]


	def swapColumnsInArea(self):
		self.transposeGrid()
		self.swapRowsInArea()
		self.transposeGrid()


	def swapHorizontalAreas(self):
		area1, area2 = random.sample(range(self.__n), 2)
		
		for i in range(self.__n):
			N1, N2 = area1 * self.__n + i, area2 * self.__n + i
			self.__table[N1], self.__table[N2] = self.__table[N2], self.__table[N1]
			self.__table[N1], self.__table[N2] = self.__table[N2], self.__table[N1]


	def swapVerticalAreas(self):
		self.transposeGrid()
		self.swapHorizontalAreas()
		self.transposeGrid()
	
	def mixGrid(self, timesToChangeGrid=50):
		allMixFunctions = (
			self.transposeGrid,
			self.swapRowsInArea,
			self.swapColumnsInArea,
			self.swapHorizontalAreas,
			self.swapVerticalAreas,
		)
		
		for i in range(timesToChangeGrid):
			random.choice(allMixFunctions)()
