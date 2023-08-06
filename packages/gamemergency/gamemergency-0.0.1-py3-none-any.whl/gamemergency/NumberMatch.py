import random


class NumberMatch:
    def __init__(self, lvl: int):
        if not lvl in [1, 2, 3]:
            raise NumberMatchError("level out of range")
        self.level = lvl
        self.judge = random.choice(range(1, 101))
        self.turnleft = 7 - lvl
        self.game = False

    def guess(self, num: int):
        if self.turnleft != 0:
            self.turnleft -= 1
            if self.judge != num:
                if self.turnleft == 0:
                    self.game = True
                    return ("Down" if self.judge < num else "Up"), "lose"
                return "Down" if self.judge < num else "Up"
            else:
                self.game = True
                return "Win"
        else:
            raise NumberMatchError("Game is already over")

    def gameover(self):
        return self.game

    def turn_count(self):
        return self.turnleft


class NumberMatchError(Exception):
    pass
