import random


class NQPosition:
    def __init__(self, n):
        # choose some internal representation of the NxN board
        # put queens on it
        self.board = [random.randint(0, n - 1) for _ in range(n)]  # random board
        self.n = n
        self.board_value = self.value(self.board)
        self.start_value = self.value(self.board)

    def value(self, board):
        # calculate number of conflicts (queens that can capture each other)
        conflicts = 0
        for a, queen in enumerate(board):
            for b, other in enumerate(board[0:a]):
                delta = a - b
                conflicts += (
                                     queen - delta == other  # One diagonal
                             ) + (
                                     queen + delta == other  # Second diagonal
                             ) + (
                                     queen == other  # horisontal and vertical
                             )
        return conflicts

    def make_move(self, move):
        # actually execute a move (change the board) and update its value
        self.board[move[0]] = move[1]
        self.board_value = self.value(self.board)

    def best_move(self):
        # find the best move and the value function after making that move
        next_move = None
        new_value = self.board_value
        copy = self.board.copy()
        for i, queen in enumerate(self.board):
            for j in range(self.n):
                if i != j:
                    copy[i] = j
                    value = self.value(copy)
                    if new_value > value:
                        new_value = value
                        next_move = [i, j]
            copy[i] = queen
        return next_move, new_value


def hill_climbing(n):
    this_pos = NQPosition(n)
    while True:
        move, new_value = this_pos.best_move()
        if not move or new_value > this_pos.board_value:
            # no improvement, give up
            break
        else:
            # finish searching as solution was found
            if new_value == 0:
                this_pos.make_move(move)
                return this_pos

            # position improves, keep searching
            this_pos.make_move(move)
    return this_pos


for n in range(4, 100):
    while True:
        board_state = hill_climbing(n)
        if board_state.board_value == 0:
            print("Board size: ", n)
            print("Starting value: ", board_state.start_value)
            print("Final value: ", board_state.board_value)
            for y, x in enumerate(board_state.board):
                for j in range(n):
                    print(" Q" if j == x else " .", end="")
                print()
            print()
            break
