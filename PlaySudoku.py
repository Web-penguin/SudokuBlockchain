import sys
import os
import random
import pygame
import SudokuMaker as SM
import SudokuCell as SC
import web3
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import time

sudokuSize = 3
gasLimit = 4000000
white = (255, 255, 255)
initXLoc = 75
initYLoc = 80
tickValue = 60
offset = 41
sleepTime = 3

def loadImage(name):
	fullname = os.path.join("images", name)
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha() == None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except:
		print("Could not load image:", fullname)
	return image, image.get_rect()


def changeCellPosition(Cell, direction, Cells):
	xLoc, yLoc = Cell.currentCellLocation()
	Cell.unhighlightCell()
	if direction == pygame.K_DOWN:
		Cell = Cells[((yLoc + 1) * sudokuSize ** 2 + xLoc) % sudokuSize ** 4]
	elif direction == pygame.K_UP:
		Cell = Cells[(yLoc - 1) * sudokuSize ** 2 + xLoc]
	elif direction == pygame.K_LEFT:
		Cell = Cells[yLoc * sudokuSize ** 2 + xLoc - 1]
	else:
		Cell = Cells[(yLoc * sudokuSize ** 2 + xLoc + 1) % sudokuSize ** 4]
	Cell.highlightCell()
	return Cell


def takeStartPosition(value, initLoc):
	startValue = (value * offset) + (value // 3 * 4 + 2 + initLoc)
	return startValue

def main():

	contract_source_code = '''
	pragma solidity ^0.4.1;

	contract Sudoku {
		uint8[9][9] solutionGrid;
		uint8[9][9] currentGrid;

		function Sudoku() {

		}

		function setSolutionGrid(uint8[9][9] _solution) {
			solutionGrid = _solution;
		}

		function setCurrentGrid(uint8[9][9] _currentGrid) {
			currentGrid = _currentGrid;
		}

		function getSolutionGrid() view returns (uint8[9][9]) {
			return solutionGrid;
		}

		function getCurrentGrid() view returns (uint8[9][9]) {
			return currentGrid;
		}

		function isSudokuResolved() view returns (bool) {
			for (uint8 i = 0; i < solutionGrid.length; i++) {
				for (uint8 j = 0; j < solutionGrid[0].length; j++) {
					if (solutionGrid[i][j] != currentGrid[i][j]) {
						return false;
					} 
				}
			}
			return true;
		}

		function getCellOfCurrentGrid(uint8 _row, uint8 _column) view returns (uint8) {
			return currentGrid[_row][_column];
		}

		function changeCellOfCurrentGrid(uint8 _row, uint8 _column, uint8 _value) {
			currentGrid[_row][_column] = _value;
		}
	}
	'''

	compiled_sol = compile_source(contract_source_code)
	contract_interface = compiled_sol['<stdin>:Sudoku']

	w3 = Web3(TestRPCProvider())

	contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

	tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': gasLimit})

	tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
	contract_address = tx_receipt['contractAddress']

	contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

	newFullSudoku = SM.makeNewFullSudoku()
	contract_instance.setSolutionGrid(newFullSudoku.table, transact={'from': w3.eth.accounts[0]})
	newFullSudoku.showGrid()
	
	newTaskSudoku = SM.makeNewTaskSudoku(newFullSudoku)
	contract_instance.setCurrentGrid(newTaskSudoku.table, transact={'from': w3.eth.accounts[0]})


	del newFullSudoku
	del newTaskSudoku

	pygame.init()

	size = (525, 548)
	screen = pygame.display.set_mode(size)

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(white)

	board, boardRect = loadImage("background.png")
	boardRect = boardRect.move(initXLoc, initYLoc)

	pygame.display.set_caption("Sudoku on Blockchain")
	clock = pygame.time.Clock()

	Cells = []
	startX, startY, editable, number = 0, 0, False, 0

	for y in range(sudokuSize ** 2):
		for x in range(sudokuSize ** 2):
			startX = takeStartPosition(x, initXLoc)
			startY = takeStartPosition(y, initYLoc)
			number = contract_instance.getCellOfCurrentGrid(y, x)
			if number != 0:
				editable = False
			else:
				editable = True
			Cells.append(SC.SudokuCell(number, startX, startY, editable, x, y))

	currentHighlight = Cells[0]
	currentHighlight.highlightCell()

	screen.blit(background, (0, 0))
	screen.blit(board, boardRect)
	pygame.display.flip()

	theNumbers = {
	pygame.K_0 : "",
	pygame.K_1 : 1,
	pygame.K_2 : 2, 
	pygame.K_3 : 3,
	pygame.K_4 : 4,
	pygame.K_5 : 5, 
	pygame.K_6 : 6,
	pygame.K_7 : 7,
	pygame.K_8 : 8, 
	pygame.K_9 : 9,
	pygame.K_SPACE : "",
	pygame.K_BACKSPACE : "",
	pygame.K_DELETE : ""
	}

	directions = (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT)

	while True:
		isResolved = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 0
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				return 0
			if event.type == pygame.MOUSEBUTTONDOWN:
				mousePosition = pygame.mouse.get_pos()
				for x in Cells:
					if x.checkCollide(mousePosition):
						currentHighlight.unhighlightCell()
						currentHighlight = x
						currentHighlight.highlightCell()
			if event.type == pygame.KEYDOWN and event.key in directions:
				currentHighlight = changeCellPosition(currentHighlight, event.key, Cells)
			if event.type == pygame.KEYDOWN and event.key in theNumbers:
				isChanged = currentHighlight.changeCell(theNumbers[event.key])
				xLoc, yLoc = currentHighlight.currentCellLocation()
				if isChanged:
					if theNumbers[event.key] != "":
						contract_instance.changeCellOfCurrentGrid(yLoc, xLoc, theNumbers[event.key], transact={'from': w3.eth.accounts[0]})
					else:
						contract_instance.changeCellOfCurrentGrid(yLoc, xLoc, 0, transact={'from': w3.eth.accounts[0]})
					isResolved = contract_instance.isSudokuResolved()

		if isResolved:
			screen = pygame.display.get_surface()
			winImage, _ = loadImage("winner.jpg")
			screen.blit(winImage, (0, 0))
			pygame.display.flip()
			clock.tick(tickValue)
			time.sleep(sleepTime)
			break
		else:   
			for cell in Cells:
				cell.draw()
			pygame.display.flip()
			clock.tick(tickValue)


if __name__ == "__main__":
	main()
	sys.exit()