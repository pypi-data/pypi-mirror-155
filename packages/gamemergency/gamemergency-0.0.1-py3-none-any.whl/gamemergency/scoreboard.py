class ScoreBoard:
    def __init__(self, user_count: int):
        if user_count < 1:
            raise ScoreBoardError("Wrong number of user")
        self.user_count = user_count
        self.board = []
        self.history = []
        for i in range(self.user_count):
            self.board.append(0)
            self.history.append({})

    def append_score(self, user_num: int, score: int, reason=None):
        if not user_num in range(self.user_count):
            raise ScoreBoardError("Wrong user number")
        self.board[user_num] += score
        self.history[user_num][score] = reason

    def check_score(self, user_num=None):
        if user_num == None:
            return self.board
        else:
            if not user_num in range(self.user_count):
                raise ScoreBoardError("Wrong user number")
            return self.board[user_num]

    def check_history(self):
        return self.history


class ScoreBoardError(Exception):
    pass
