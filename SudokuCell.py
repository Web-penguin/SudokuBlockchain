import pygame

black = (0, 0, 0)
currentCellColour = (117, 255, 205)
white = (255, 255, 255, 255)
digitColour = (255, 46, 46)


class SudokuCell:
	def __init__(self, number=None, offsetX=0, offsetY=0, edit=True, xLoc=0, yLoc=0):

		if number == 0:
			number = ""
		
		self.__font = pygame.font.Font(None, 30)
		self.__text = self.__font.render(str(number), 1, black)
		self.__textpos = self.__text.get_rect()
		self.__textpos = self.__textpos.move(offsetX + 12, offsetY + 6)

		self.__collide = pygame.Surface((40, 40))
		self.__collide = self.__collide.convert()
		self.__collide.fill(white)
		self.__collideRect = self.__collide.get_rect()
		self.__collideRect = self.__collideRect.move(offsetX + 1, offsetY + 1)

		self.__edit = edit
		self.__xLoc = xLoc
		self.__yLoc = yLoc


	def highlightCell(self):
		self.__collide.fill(currentCellColour)
		self.draw()


	def unhighlightCell(self):
		self.__collide.fill(white)
		self.draw()


	def draw(self):
		screen = pygame.display.get_surface()
		screen.blit(self.__collide, self.__collideRect)
		screen.blit(self.__text, self.__textpos)


	def changeCell(self, number):
		if self.__edit == True:
			self.__text = self.__font.render(str(number), 1, digitColour)
			self.draw()
			return True
		else:
			return False


	def checkCollide(self, collision):
		if len(collision) == 2:
			return self.__collideRect.collidepoint(collision)
		elif len(collision) == 4:
			return self.__collideRect.colliderect(collision)
		else:
			return False


	def currentCellLocation(self):
		return self.__xLoc, self.__yLoc