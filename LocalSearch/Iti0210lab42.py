from __future__ import print_function

import random
import sys
from itertools import permutations

from ortools.sat.python import cp_model


def main(board_size):
    model = cp_model.CpModel()
    # Creates the variables.
    # The array index is the column, and the value is the row.
    queens = [model.NewIntVar(0, board_size - 1, 'x%i' % i)
              for i in range(board_size)]
    # Creates the constraints.
    # The following sets the constraint that all queens are in different rows.
    model.AddAllDifferent(queens)

    # Note: all queens must be in different columns because the indices of queens are all different.

    # The following sets the constraint that no two queens can be on the same diagonal.
    for i in range(board_size):
        # Note: is not used in the inner loop.
        diag1 = []
        diag2 = []
        for j in range(board_size):
            # Create variable array for queens(j) + j.
            q1 = model.NewIntVar(0, 2 * board_size, 'diag1_%i' % i)
            diag1.append(q1)
            model.Add(q1 == queens[j] + j)
            # Create variable array for queens(j) - j.
            q2 = model.NewIntVar(-board_size, board_size, 'diag2_%i' % i)
            diag2.append(q2)
            model.Add(q2 == queens[j] - j)
        model.AddAllDifferent(diag1)
        model.AddAllDifferent(diag2)
    ### Solve model.
    solver = cp_model.CpSolver()
    solution_printer = SolutionPrinter(queens)
    status = solver.SearchForAllSolutions(model, solution_printer)
    print()
    print('Solutions found : %i' % solution_printer.SolutionCount())


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('%s = %i' % (v, self.Value(v)), end=' ')
        print()

    def SolutionCount(self):
        return self.__solution_count


class DiagramPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1

        for v in self.__variables:
            queen_col = int(self.Value(v))
            board_size = len(self.__variables)
            # Print row with queen.
            for j in range(board_size):
                if j == queen_col:
                    # There is a queen in column j, row i.
                    print("Q", end=" ")
                else:
                    print("_", end=" ")
            print()
        print()

    def SolutionCount(self):
        return self.__solution_count


def google_ortools():
    board_size = 8
    if len(sys.argv) > 1:
        board_size = int(sys.argv[1])
    main(board_size)


#######################################################################################################################

def queensproblem(rows, columns):
    solutions = [[]]
    for row in range(rows):
        solutions = add_one_queen(row, columns, solutions)
    return solutions


def add_one_queen(new_row, columns, prev_solutions):
    return [solution + [new_column]
            for solution in prev_solutions
            for new_column in range(columns)
            if no_conflict(new_row, new_column, solution)]


def no_conflict(new_row, new_column, solution):
    return all(solution[row] != new_column and
               solution[row] + row != new_column + new_row and
               solution[row] - row != new_column - new_row
               for row in range(new_row))


#######################################################################################################################

class QueenChessBoard:
    def __init__(self, size):
        self.size = size
        # columns[r] is a number c if a queen is placed at row r and column c.
        # columns[r] is out of range if no queen is place in row r.
        # Thus after all queens are placed, they will be at positions
        # (columns[0], 0), (columns[1], 1), ... (columns[size - 1], size - 1)
        self.columns = []

    def place_in_next_row(self, column):
        self.columns.append(column)

    def remove_in_current_row(self):
        return self.columns.pop()

    def is_this_column_safe_in_next_row(self, column):
        # index of next row
        row = len(self.columns)

        # check column
        for queen_column in self.columns:
            if column == queen_column:
                return False

        # check diagonal
        for queen_row, queen_column in enumerate(self.columns):
            if queen_column - queen_row == column - row:
                return False

        # check other diagonal
        for queen_row, queen_column in enumerate(self.columns):
            if ((self.size - queen_column) - queen_row
                    == (self.size - column) - row):
                return False

        return True

    def display(self):
        for row in range(self.size):
            for column in range(self.size):
                if column == self.columns[row]:
                    print('Q', end=' ')
                else:
                    print('.', end=' ')
            print()


def solve_queen(size):
    """Display a chessboard for each possible configuration of placing n queens
    on an n x n chessboard and print the number of such configurations."""
    board = QueenChessBoard(size)
    number_of_solutions = 0

    row = 0
    column = 0
    # iterate over rows of board
    while True:
        # place queen in next row
        while column < size:
            if board.is_this_column_safe_in_next_row(column):
                board.place_in_next_row(column)
                row += 1
                column = 0
                break
            else:
                column += 1

        # if could not find column to place in or if board is full
        if (column == size or row == size):
            # if board is full, we have a solution
            if row == size:
                board.display()
                print()
                number_of_solutions += 1

                # small optimization:
                # In a board that already has queens placed in all rows except
                # the last, we know there can only be at most one position in
                # the last row where a queen can be placed. In this case, there
                # is a valid position in the last row. Thus we can backtrack two
                # times to reach the second last row.
                board.remove_in_current_row()
                row -= 1

            # now backtrack
            try:
                prev_column = board.remove_in_current_row()
            except IndexError:
                # all queens removed
                # thus no more possible configurations
                break
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column

    print('Number of solutions:', number_of_solutions)


def page_i_cant_remember():
    n = int(input('Enter n: '))
    solve_queen(n)


#######################################################################################################################

class Solution:

    def __init__(self):
        self.paths = []

    def dpSolveNQueens(self, n, prefix, level):
        for i in range(0, n):
            point = (i, level)
            is_valid = True
            for m in range(0, len(prefix)):
                if i == prefix[m]:
                    is_valid = False
                    break
                if level - m == i - prefix[m] or level - m == prefix[m] - i:
                    is_valid = False
                    break
            if is_valid:
                new_prefix = prefix[:]
                new_prefix.append(i)
                if n - 1 != level:
                    self.dpSolveNQueens(n, new_prefix, level + 1)
                else:
                    self.paths.append(new_prefix)

    def solveNQueens(self, n):
        self.dpSolveNQueens(n, [], 0)
        lists = []
        for path in self.paths:
            list = []
            for num in path:
                str = "." * num + "Q" + "." * (n - num - 1)
                list.append(str)
            lists.append(list)
        return lists


def some_chinese_webpage():
    solution = Solution()
    [print(x) for x in solution.solveNQueens(100)]


#######################################################################################################################

def solveNQueens(n):
    ans = []
    queens = [-1] * n
    columns = [True] * n + [False]  # || col with dummy for boundary
    back = [True] * n * 2  # \\ col - row
    forward = [True] * n * 2  # // col + row
    row = col = 0
    while True:
        if columns[col] and back[col - row + n] and forward[col + row]:
            queens[row] = col
            columns[col] = back[col - row + n] = forward[col + row] = False
            row += 1
            col = 0
            if row == n:
                ans.append(['.' * q + 'Q' + '.' * (n - q - 1) for q in queens])
        else:
            if row == n or col == n:
                if row == 0:
                    return ans
                row -= 1
                col = queens[row]
                columns[col] = back[col - row + n] = forward[col + row] = True
            col += 1


#######################################################################################################################

def myBoardAnalysis(n):
    board = [[0 for i in range(n)] for j in range(n)]
    for y, line in enumerate(board):
        for x, place in enumerate(line):
            board[y][x] += 1
            fillBoard(board, n, x, y)

    [print(x) for x in board]


def fillBoard(board, n, x, y):
    step = 1
    while True:
        toBreak = True

        if y - step >= 0 and x + step < n:
            board[y - step][x + step] += 1
            toBreak = False
        if y - step >= 0 and x - step >= 0:
            board[y - step][x - step] += 1
            toBreak = False
        if y + step < n and x + step < n:
            board[y + step][x + step] += 1
            toBreak = False
        if y + step < n and x - step >= 0:
            board[y + step][x - step] += 1
            toBreak = False

        if y - step >= 0:
            board[y - step][x] += 1
            toBreak = False
        if x - step >= 0:
            board[y][x - step] += 1
            toBreak = False
        if y + step < n:
            board[y + step][x] += 1
            toBreak = False
        if x + step < n:
            board[y][x + step] += 1
            toBreak = False

        if toBreak:
            break
        step += 1


#######################################################################################################################

class NQueens:
    def __init__(self, size):
        self.n = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.queenPositions = []

        for x in range(size):
            randomIndex = random.randint(0, size - 1)
            self.board[x][randomIndex] = 1
            self.queenPositions.append((x, randomIndex))

    def allQueensSafe(self):
        return all(not self.UnderAttack(pos) for pos in self.queenPositions)

    def attackViaCol(self, pos):
        return any(pos[1] == queen[1] and queen != pos for queen in self.queenPositions)

    def attackViaRow(self, pos):
        return any(pos[0] == queen[0] and queen != pos for queen in self.queenPositions)

    def attackViaDiagonal(self, pos):
        return any(abs(queen[0] - pos[0]) == abs(queen[1] - pos[1]) and queen != pos for queen in self.queenPositions)

    def UnderAttack(self, position):
        return self.attackViaDiagonal(position) or self.attackViaRow(position) or self.attackViaCol(position)

    def specificQueenConflicts(self, pos):  # returns number of pieces attacking queen at position pos
        assert pos in self.queenPositions  # checks to make sure given position is a queen
        count = 0
        for queen in self.queenPositions:
            count += (abs(queen[0] - pos[0]) == abs(queen[1] - pos[1]) or pos[0] == queen[0] or pos[1] == queen[
                1]) and queen != pos
        return count

    def pickRandomQueen(self):  # returns position of random queen
        newIndex = random.randint(0, self.n - 1)
        return self.queenPositions[newIndex]

    def printBoard(self):  # prints out all positions of queens
        for queen in self.queenPositions:
            print(queen)

    def moveQueen(self, startPos, endPos):  # moves queen from startpos to endpos
        assert self.board[startPos[0]][startPos[1]] == 1
        # above assert will fail if the start position does not have a queen
        self.board[startPos[0]][startPos[1]] = 0
        self.board[endPos[0]][endPos[1]] = 1
        self.queenPositions.remove(startPos)
        self.queenPositions.append(endPos)

    def availablePositions(self, pos):
        # returns list of tuples with all positions queen can go
        availablePos = []
        for x in range(self.n):
            availablePos.append((pos[0], x))

        return availablePos


def min_conflicts_AI():
    n = 6
    NQ = NQueens(n)
    timer = 0
    while not NQ.allQueensSafe():
        minAttacks = n + 1  # n + 1 is greater than any possibility of attacks so this is guaranteed to get minimized
        pickedQueen = NQ.pickRandomQueen()

        minConflictPosition = (-1, -1)
        for pos in NQ.availablePositions(pickedQueen):
            NQ.moveQueen(pickedQueen, pos)
            newNumberOfConflicts = NQ.specificQueenConflicts(pos)
            if newNumberOfConflicts < minAttacks:
                minConflictPosition = pos
                minAttacks = newNumberOfConflicts
            NQ.moveQueen(pos, pickedQueen)  # move queen back

        NQ.moveQueen(pickedQueen, minConflictPosition)  # move queen to least conflict spot
    NQ.printBoard()


def iterations():
    n = 8
    cols = range(n)
    [print(vec) if n == len(set(vec[i] + i for i in cols)) == len(set(vec[i] - i for i in cols)) else None for vec in
     permutations(cols)]


if __name__ == '__main__':
    google_ortools() # gets slow at 100 x 100
    # rosettacode() # not actually viable
    # page_i_cant_remember() # slow
    # some_chinese_webpage() # slow
    # print(solveNQueens(3)) # slow
    # displaygrid(4) # mystatistics
    # min_conflicts_AI() # inconsistent

    # iterations()

