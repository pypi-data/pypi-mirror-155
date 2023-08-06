import random


class RSP:
    def __init__(self, option=None):
        if option == "AI":
            self.gamemode = "AI"
            self.AI_choice = random.choice(["R", "S", "P"])
            self.P_choice = None
        else:
            self.gamemode = "2P"
            self.X = None
            self.Y = None

    def AI(self, rsp):
        if self.gamemode == "AI":
            if not rsp in ["R", "S", "P"]:
                raise RSPError("Your choice is not in R,S,P")
            self.P_choice = rsp
            if self.AI_choice == rsp:
                return "Draw"
            if self.AI_choice == "R":
                if rsp == "S":
                    return "Lose"
                elif rsp == "P":
                    return "Win"
            if self.AI_choice == "S":
                if rsp == "R":
                    return "Win"
                elif rsp == "P":
                    return "Lose"
            if self.AI_choice == "P":
                if rsp == "R":
                    return "Lose"
                elif rsp == "S":
                    return "Win"

    def P2(self, p1, p2):
        if self.gamemode == "2P":

            if not p1 in ["R", "S", "P"] or not p2 in ["R", "S", "P"]:
                raise RSPError("Your choice is not in R,S,P")
            if p1 == p2:
                return "Draw"
            if p1 == "R":
                if p2 == "S":
                    return "p1 Win"
                elif p2 == "P":
                    return "p2 Win"
            if p1 == "S":
                if p2 == "R":
                    return "p2 Win"
                elif p2 == "P":
                    return "p1 Win"
            if p1 == "P":
                if p2 == "R":
                    return "p1 Win"
                elif p2 == "S":
                    return "p2 Win"
        else:
            raise RSPError("Wrong gamemode")

    def AI_rsp(self):
        if self.gamemode == "AI":
            return self.AI_choice
        else:
            raise RSPError("Wrong gamemode")


class RSPError(Exception):
    pass
