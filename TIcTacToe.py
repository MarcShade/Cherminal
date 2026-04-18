from random import randint

WIN_CONDITIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],

    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],

    [0, 4, 8],
    [2, 4, 6]
]

class TicTacToe:
    def __init__(self, player_1, player_2, index: int):
        self.board: list[int] = [0 for _ in range(9)]
        # self.board: list[int] = [0, 1, 2, 0, 0, 2, 0, 1, 0]
        self.turn: int = 0
        self.winner: int = 0
        self.index = index # This is only to keep track of what index in the list of games on the server this is.

        self.player_1 = player_1
        self.player_2 = player_2

        self.players = [player_1, player_2]

    def is_square_free(self, tile: int) -> bool:
        return self.board[tile] == 0

    def move(self, tile: int):
        if self.is_square_free(tile):
            if self.winner:
                return
            self.turn = (self.turn + 1) % 2
            self.board[tile] = self.turn + 1

            self.winner = self.check_win()

    def check_win(self) -> int:
        for condition in WIN_CONDITIONS:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] and self.board[condition[0]] != 0:
                return self.board[condition[0]]
        return 0