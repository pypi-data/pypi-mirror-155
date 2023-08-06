class TicTacToe:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.PlayerTurn = "O"
        self.Winner = None

    def Player_O(self, x: int, y: int):
        if self.Winner != None:
            raise TicTacToeError("Game is already over")
        if (not x in [0, 1, 2]) or (not y in [0, 1, 2]):
            raise TicTacToeError("Wrong Coordinate")
        if self.PlayerTurn == "O":
            if self.board[y][x] == 0:
                self.board[y][x] = 1
                if self.GameEnd() == False:
                    self.PlayerTurn = "X"
                else:
                    self.PlayerTurn = None
                    self.Winner = "O"
                    return True
            else:
                raise TicTacToeError("Board is occupied")
        else:
            raise TicTacToeError("Wrong turn")

    def Player_X(self, x: int, y: int):
        if self.Winner != None:
            raise TicTacToeError("Game is already over")
        if (not x in [0, 1, 2]) or (not y in [0, 1, 2]):
            raise TicTacToeError("Wrong Coordinate")
        if self.PlayerTurn == "X":
            if self.board[y][x] == 0:
                self.board[y][x] = -1
                if self.GameEnd() == False:
                    self.PlayerTurn = "O"
                else:
                    self.PlayerTurn = None
                    self.Winner = "X"
                    return True
            else:
                raise TicTacToeError("Board is occupied")
        else:
            raise TicTacToeError("Wrong turn")

    def GameEnd(self):
        for i in range(3):
            k = 0
            for j in range(3):
                k += self.board[i][j]
            if k != 0 and k % 3 == 0:
                return True
        for i in range(3):
            k = 0
            for j in range(3):
                k += self.board[j][i]
            if k != 0 and k % 3 == 0:
                return True
        a = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if a != 0 and a % 3 == 0:
            return True
        b = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if b != 0 and b % 3 == 0:
            return True
        return False

    def Board(self):
        return self.board

    def current_turn(self):
        return self.PlayerTurn

    def winner(self):
        return self.Winner


class TicTacToeError(Exception):
    pass
