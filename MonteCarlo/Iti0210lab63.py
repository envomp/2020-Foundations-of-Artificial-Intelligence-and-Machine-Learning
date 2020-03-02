import random

GAMES = 1000

WIDTH = 7
HEIGHT = 6

PLAYER = 1
AI = 2


class ConnectFour:
    def __init__(self):
        self.scores = dict()  # { 1:[wins, ties, losses] }
        self.board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.moves_left = HEIGHT * WIDTH

    def play_game(self):
        while 1:
            print()
            self.do_player_move()
            [print(x) for x in self.board]
            if self.is_game_over(PLAYER):
                print("Player won!")
                return PLAYER
            self.moves_left -= 1

            print()
            self.do_AI_move()
            [print(x) for x in self.board]
            if self.is_game_over(AI):
                print("AI won!")
                return AI

            self.moves_left -= 1
            if self.moves_left == 0:
                print("It's a tie!")
                return 0

    def get_available_moves(self):
        return [i for i, piece in enumerate(self.board[0]) if piece == 0]

    def ask_and_validate_player_move(self):
        available_moves = self.get_available_moves()
        while True:
            player_move = input(f"Please select a move from {available_moves}: ")
            if player_move.isdigit() and int(player_move) in available_moves:
                return int(player_move)
            print("Invalid move!")

    def do_AI_move(self):
        self.scores = dict()

        move = self.get_none_or_certain_win()
        if move is not None:
            print(f"AI blocked player with move {move}")
            self.do_move_for_side(move)
            return

        for move in range(7):
            self.scores[move] = [0, 0, 0]

        for move in self.get_available_moves():
            self.monte_carlo(move)

        print()
        print(self.scores)
        scores = [value[0] + 0.5 * value[1] for value in self.scores.values()]
        best_moves = [i for i, j in enumerate(scores) if j == max(scores)]

        move = random.choice(best_moves)
        self.do_move_for_side(move)

        print(f"AI move was {move}")

    def do_move_for_side(self, move):
        for i in range(HEIGHT - 1, -1, -1):
            if self.board[i][move] == 0:
                self.board[i][move] = AI
                break

    def simulate_random_moves(self, root_move):
        for game in range(GAMES):
            board = [row[:] for row in self.board]
            game_moves = self.moves_left
            while 1:
                game_moves -= 1
                if game_moves == 0:
                    self.scores[root_move][1] += 1
                    break

                move = random.choice(self.get_available_moves())

                for i in range(HEIGHT - 1, -1, -1):
                    if self.board[i][move] == 0:
                        self.board[i][move] = PLAYER
                        break

                if self.is_game_over(PLAYER):
                    self.scores[root_move][0] += 1
                    break

                game_moves -= 1
                if game_moves == 0:
                    self.scores[root_move][1] += 1
                    break

                move = random.choice(self.get_available_moves())

                self.do_move_for_side(move)

                if self.is_game_over(AI):
                    self.scores[root_move][2] += 1
                    break

            self.board = [row[:] for row in board]  # revert board

    def get_none_or_certain_win(self):

        for move in self.get_available_moves():
            move_row = 0
            for i in range(HEIGHT - 1, -1, -1):
                if self.board[i][move] == 0:
                    # do move
                    self.board[i][move] = AI
                    move_row = i
                    break

            # undo move
            if self.is_game_over(AI):
                self.board[move_row][move] = 0
                return move
            else:
                self.board[move_row][move] = 0

            move_row = 0
            for i in range(HEIGHT - 1, -1, -1):
                if self.board[i][move] == 0:
                    # do move
                    self.board[i][move] = PLAYER
                    move_row = i
                    break

            # undo move
            if self.is_game_over(PLAYER):
                self.board[move_row][move] = 0
                return move
            else:
                self.board[move_row][move] = 0

        return None

    def monte_carlo(self, move):
        move_row = 0
        for i in range(HEIGHT - 1, -1, -1):
            if self.board[i][move] == 0:
                # do move
                self.board[i][move] = AI
                move_row = i
                break

        self.simulate_random_moves(move)

        # undo move
        self.board[move_row][move] = 0

    def do_player_move(self):
        player_move = self.ask_and_validate_player_move()
        for i in range(HEIGHT - 1, -1, -1):
            if self.board[i][player_move] == 0:
                self.board[i][player_move] = PLAYER
                return

    def is_game_over(self, move):

        # horizontalCheck
        for i in range(0, HEIGHT):
            for j in range(0, WIDTH - 3):
                if self.board[i][j] == move and \
                        self.board[i][j + 1] == move and \
                        self.board[i][j + 2] == move and \
                        self.board[i][j + 3] == move:
                    return True

        # verticalCheck
        for i in range(0, HEIGHT - 3):
            for j in range(0, WIDTH):
                if self.board[i][j] == move and \
                        self.board[i + 1][j] == move and \
                        self.board[i + 2][j] == move and \
                        self.board[i + 3][j] == move:
                    return True

        # ascendingDiagonalCheck 
        for i in range(3, HEIGHT):
            for j in range(0, WIDTH - 3):
                if self.board[i][j] == move and \
                        self.board[i - 1][j + 1] == move and \
                        self.board[i - 2][j + 2] == move and \
                        self.board[i - 3][j + 3] == move:
                    return True

        # descendingDiagonalCheck
        for i in range(3, HEIGHT):
            for j in range(3, WIDTH):
                if self.board[i][j] == move and \
                        self.board[i - 1][j - 1] == move and \
                        self.board[i - 2][j - 2] == move and \
                        self.board[i - 3][j - 3] == move:
                    return True

        return False


if __name__ == '__main__':
    game = ConnectFour()
    game.play_game()
