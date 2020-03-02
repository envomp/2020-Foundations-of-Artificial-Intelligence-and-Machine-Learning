import random

GAMES = 200

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
        ai_move = 0
        self.scores = dict()

        for move in self.get_available_moves():
            self.scores[move] = []

        for move in self.get_available_moves():
            self.monte_carlo(move)

        print(f"AI move was {ai_move}")

    def simulate_random_moves(self):
        for game in range(GAMES):
            game_moves = self.moves_left
            while 1:
                move = random.choice(self.get_available_moves())


    def monte_carlo(self, move):
        # do move
        move_row = -1
        for i in range(HEIGHT - 1, -1, -1):
            if self.board[i][move] == 0:
                self.board[i][move] = AI
                move_row = i

        self.simulate_random_moves()

        # undo move
        self.board[move_row][move_row] = 0

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
