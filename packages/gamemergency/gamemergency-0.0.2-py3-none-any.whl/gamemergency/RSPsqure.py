import random


class RSPsqure:
    def __init__(self):
        self.AI_choice = random.choice(["R", "S", "P"])
        self.P_choice = None
        self.ahead = None
        self.turn = 0
        self.Gameover = False

    def P_turn(self, rsp):
        if not rsp in ["R", "S", "P"]:
            raise RSPsqureError("Your choice is not in R,S,P")
        if self.Gameover == True:
            raise RSPsqureError("Game is already over")
        if rsp == self.AI_choice and self.turn == 0:
            self.AI_choice = random.choice(["R", "S", "P"])
            self.turn = 0
        if rsp == self.AI_choice and self.ahead == "P":
            self.Gameover = True
            return "Win"
        elif rsp == self.AI_choice and self.ahead == "AI":
            self.Gameover = True
            return "Lose"
        else:
            self.P_choice = rsp
            if self.AI_choice == "R":
                if rsp == "S":
                    self.ahead = "AI"
                    self.AI_choice = random.choice(["R", "S", "P"])
                elif rsp == "P":
                    self.ahead = "P"
                    self.AI_choice = random.choice(["R", "S", "P"])
            if self.AI_choice == "S":
                if rsp == "R":
                    self.ahead = "P"
                    self.AI_choice = random.choice(["R", "S", "P"])
                elif rsp == "P":
                    self.ahead = "AI"
                    self.AI_choice = random.choice(["R", "S", "P"])
            if self.AI_choice == "P":
                if rsp == "R":
                    self.ahead = "AI"
                    self.AI_choice = random.choice(["R", "S", "P"])
                elif rsp == "S":
                    self.ahead = "P"
                    self.AI_choice = random.choice(["R", "S", "P"])
            self.turn += 1


class RSPsqureError(Exception):
    pass
