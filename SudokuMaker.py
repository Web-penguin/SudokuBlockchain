import random
import SudokuSolver
import SudokuGrid

def makeNewFullSudoku():
	newGrid = SudokuGrid.Grid()
	newGrid.mixGrid()
	return newGrid

def makeNewTaskSudoku(fullSudoku):
	lookedCells = [[False for i in range(fullSudoku.n ** 2)] for j in range(fullSudoku.n ** 2)]
	it = 0
	countGivenDigits = fullSudoku.n ** 4

	while it < fullSudoku.n ** 4:
		i, j = random.randrange(fullSudoku.n ** 2), random.randrange(fullSudoku.n ** 2)
		if not lookedCells[i][j]:
			lookedCells[i][j] = True
			it += 1

			elementForBackup = fullSudoku.table[i][j]
			fullSudoku.table[i][j] = 0
			countGivenDigits -= 1

			currentTableForSolution = []
			for tmp in range(fullSudoku.n ** 2):
				currentTableForSolution.append(fullSudoku.table[tmp][:])

			solutionsCount = 0
			for solution in SudokuSolver.solve_sudoku((fullSudoku.n, fullSudoku.n), currentTableForSolution):
				solutionsCount += 1

			if solutionsCount != 1:
				fullSudoku.table[i][j] = elementForBackup
				countGivenDigits += 1

	return fullSudoku