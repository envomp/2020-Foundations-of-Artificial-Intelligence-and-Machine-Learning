def hill_climbing(pos):
    curr_value = pos.value()
    while True:
        move, new_value = pos.best_move()
        if new_value >= curr_value:
            # no improvement, give up
            return pos, curr_value
        else:
            # position improves, keep searching
            curr_value = new_value
            pos.make_move(move)


class NQPosition:
    def __init__(self, N):
        pass
    # choose some internal representation of the NxN board
    # put queens on it

    def value(self):
        # calculate number of conflicts (queens that can capture each other)
        return value


    def make_move(self, move):
        pass
    # actually execute a move (change the board)

    def best_move(self):
        # find the best move and the value function after making that move
        return move, value
