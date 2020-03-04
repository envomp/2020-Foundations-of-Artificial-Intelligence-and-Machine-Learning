import copy
import random
import sys

import numpy as np


class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.state = state.Clone()
        self.parent = parent
        self.move = move
        self.untriedMoves = state.getMoves()
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.player = state.player

    def selection(self):
        # return child with largest UCT value
        return sorted(self.childNodes, key=lambda x: x.wins / x.visits + np.sqrt(2 * np.log(self.visits) / x.visits))[-1]

    def expand(self, move, state):
        # return child when move is taken
        # remove move from current node
        child = Node(move=move, parent=self, state=state)
        self.untriedMoves.remove(move)
        self.childNodes.append(child)
        return child

    def update(self, result):
        self.wins += result
        self.visits += 1


def MCTS(currentState, itermax, currentNode=None):
    rootnode = Node(state=currentState)
    if currentNode is not None:
        rootnode = currentNode

    print(rootnode.wins, rootnode.visits)
    for child in rootnode.childNodes:
        print(child.move, child.wins, child.visits)

    for i in range(itermax):
        node = rootnode
        state = currentState.Clone()

        # selection
        # keep going down the tree based on best UCT values until terminal or unexpanded node
        while node.untriedMoves == [] and node.childNodes != []:
            node = node.selection()
            state.move(node.move)

        # expand
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            state.move(m)
            node = node.expand(m, state)

        # rollout
        while state.getMoves():
            state.move(random.choice(state.getMoves()))

        # backpropagate
        while node is not None:
            node.update(state.result(node.player))
            node = node.parent

    sortedChildNodes = sorted(rootnode.childNodes, key=lambda x: x.wins / x.visits)[::-1]
    print("AI\'s computed winning percentages")
    for node in sortedChildNodes:
        print('Move: %s    Win Rate: %d' % (node.move, 100 * node.wins / node.visits))
    print('Simulations performed: %s\n' % i)
    return rootnode, sortedChildNodes[0].move


######################################################

class Connect4:
    def __init__(self, ROW, COLUMN, LINE):
        self.bitboard = [0, 0]  # bitboard for each player
        self.dirs = [1, (ROW + 1), (ROW + 1) - 1, (ROW + 1) + 1]  # this is used for bitwise operations
        self.heights = [(ROW + 1) * i for i in range(COLUMN)]  # top empty row for each column
        self.lowest_row = [0] * COLUMN  # number of stones in each row
        self.board = np.zeros((ROW, COLUMN), dtype=int)  # matrix representation of the board (just for printing)
        self.top_row = [(x * (ROW + 1)) - 1 for x in
                        range(1, COLUMN + 1)]  # top row of the board (this will never change)
        self.ROW = ROW
        self.COLUMN = COLUMN
        self.LINE = LINE
        self.player = 1

    def Clone(self):
        clone = Connect4(self.ROW, self.COLUMN, self.LINE)
        clone.bitboard = copy.deepcopy(self.bitboard)
        clone.heights = copy.deepcopy(self.heights)
        clone.lowest_row = copy.deepcopy(self.lowest_row)
        clone.board = copy.deepcopy(self.board)
        clone.top_row = copy.deepcopy(self.top_row)
        clone.player = self.player
        return clone

    def move(self, col):
        m2 = 1 << self.heights[col]  # position entry on bitboard
        self.heights[col] += 1  # update top empty row for column
        self.player ^= 1
        self.bitboard[self.player] ^= m2  # XOR operation to insert stone in player's bitboard
        self.board[self.lowest_row[col]][col] = self.player + 1  # update entry in matrix (only for printing)
        self.lowest_row[col] += 1  # update number of stones in column

    def result(self, player):
        if self.winner(player):
            return 1  # player wins
        elif self.winner(player ^ 1):
            return 0  # if opponent wins
        elif self.draw():
            return 0.5

        # checks if column is full

    def isValidMove(self, col):
        return self.heights[col] != self.top_row[col]

    # evaluate board, find out if there's a winner
    def winner(self, color):
        for d in self.dirs:
            bb = self.bitboard[color]
            for i in range(1, self.LINE):
                bb &= self.bitboard[color] >> (i * d)
            if bb != 0:
                return True
        return False

    def draw(self):
        return not self.getMoves() and not self.winner(self.player) and not self.winner(self.player ^ 1)

    def complete(self):
        return self.winner(self.player) or self.winner(self.player ^ 1) or not self.getMoves()

    def getMoves(self):
        if self.winner(self.player) or self.winner(self.player ^ 1):
            return []

        listMoves = []
        for i in range(self.COLUMN):
            if self.lowest_row[i] < self.ROW:
                listMoves.append(i)
        return listMoves


def get_input(board):
    while True:
        try:
            cin = int(input(f"Please select a move from {board.getMoves()}: "))
            if cin == -1:
                sys.exit()  # enter "-1" to exit game
            if not board.isValidMove(cin):
                raise ValueError
            print()
            return cin
        except ValueError:
            print("Invalid move!")


def begin_game(board, order=0, itermax=20000):
    players = ['Human', 'AI']
    node = Node(state=board)
    while True:
        if order == 0:
            col = get_input(board)
        elif order == 1:
            print('AI\'s thinking...')
            node, col = MCTS(board, itermax, currentNode=node)
            print('AI played column %s\n' % (col + 1))
        board.move(col)
        [print(x) for x in board.board[::-1]]
        node = goto_childNode(node, board, col)
        order ^= 1
        if board.complete():
            break
    if not board.draw():
        print('%s won' % players[board.player])
    else:
        print('Draw')


def goto_childNode(node, board, move):
    for childnode in node.childNodes:
        if childnode.move == move:
            return childnode
    return Node(state=board)


oROW, oCOLUMN = 6, 7  # change size of board here
oLINE = 4  # change number of in-a-row here
order = 0  # 0 for Human to go first; 1 for AI to go first
print("\n%s-IN-A-ROW (Size: %s by %s)\n" % (oLINE, oROW, oCOLUMN))
c4 = Connect4(oROW, oCOLUMN, oLINE)  # create Connect4 object
[print(x) for x in c4.board[::-1]]

max_iters = 10000
timeout = 3
begin_game(c4, order, max_iters)  # start game


#Source https://repl.it/talk/share/Connect-4-AI-using-Monte-Carlo-Tree-Search/10640