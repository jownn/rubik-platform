import random


class Rubik:

    def __init__(self, cube={}):
        self.moves = ["U", "L", "F", "R", "B", "D"]
        self.direction = ["", "'"]
        self.slen = random.randint(25, 28)
        self.cube_default = {
            'Upper':    {'0': 'b', '1': 'b', '2': 'b', '3': 'b', '4': 'b', '5': 'b', '6': 'b', '7': 'b', '8': 'b'},
            'Left':     {'0': 'o', '1': 'o', '2': 'o', '3': 'o', '4': 'o', '5': 'o', '6': 'o', '7': 'o', '8': 'o'},
            'Front':    {'0': 'w', '1': 'w', '2': 'w', '3': 'w', '4': 'w', '5': 'w', '6': 'w', '7': 'w', '8': 'w'},
            'Right':    {'0': 'r', '1': 'r', '2': 'r', '3': 'r', '4': 'r', '5': 'r', '6': 'r', '7': 'r', '8': 'r'},
            'Back':     {'0': 'y', '1': 'y', '2': 'y', '3': 'y', '4': 'y', '5': 'y', '6': 'y', '7': 'y', '8': 'y'},
            'Down':     {'0': 'g', '1': 'g', '2': 'g', '3': 'g', '4': 'g', '5': 'g', '6': 'g', '7': 'g', '8': 'g'},
        }
        if cube:
            self.cube = cube
        else:
            self.cube = self.cube_default

    def validMovements(self, movements):
        for move in movements:
            if move not in ["U", "U'", "L", "L'", "F", "F'", "R", "R'", "B", "B'", "D", "D'"]:
                return False
        return True

    def move(self, move):
        if move == "U" or move == "U'":
            moviment = "Upper"
            adjacente = {
                "0": "Left",
                "1": "Front",
                "2": "Right",
                "3": "Back"
            }
            part = {
                "Left":     {"0": "0", "1": "1", "2": "2"},
                "Front":    {"0": "0", "1": "1", "2": "2"},
                "Right":    {"0": "0", "1": "1", "2": "2"},
                "Back":     {"0": "0", "1": "1", "2": "2"}
            }
            direct = ''
            if move == "U":
                direct = "horario"
            elif move == "U'":
                direct = "antihorario"
        elif move == "L" or move == "L'":
            moviment = "Left"
            adjacente = {
                "0": "Back",
                "1": "Down",
                "2": "Front",
                "3": "Upper"
            }
            part = {
                "Back":     {"0": "2", "1": "5", "2": "8"},
                "Down":     {"0": "6", "1": "3", "2": "0"},
                "Front":    {"0": "6", "1": "3", "2": "0"},
                "Upper":    {"0": "6", "1": "3", "2": "0"}
            }
            direct = ''
            if move == "L":
                direct = "horario"
            elif move == "L'":
                direct = "antihorario"
        elif move == "F" or move == "F'":
            moviment = "Front"
            adjacente = {
                "0": "Left",
                "1": "Down",
                "2": "Right",
                "3": "Upper"
            }
            part = {
                "Left":     {"0": "2", "1": "5", "2": "8"},
                "Down":     {"0": "0", "1": "1", "2": "2"},
                "Right":    {"0": "6", "1": "3", "2": "0"},
                "Upper":    {"0": "8", "1": "7", "2": "6"}
            }
            direct = ''
            if move == "F":
                direct = "horario"
            elif move == "F'":
                direct = "antihorario"
        elif move == "R" or move == "R'":
            moviment = "Right"
            adjacente = {
                "0": "Front",
                "1": "Down",
                "2": "Back",
                "3": "Upper"
            }
            part = {
                "Front":    {"0": "2", "1": "5", "2": "8"},
                "Down":     {"0": "2", "1": "5", "2": "8"},
                "Back":     {"0": "6", "1": "3", "2": "0"},
                "Upper":    {"0": "2", "1": "5", "2": "8"}
            }
            direct = ''
            if move == "R":
                direct = "horario"
            elif move == "R'":
                direct = "antihorario"
        elif move == "B" or move == "B'":
            moviment = "Back"
            adjacente = {
                "0": "Right",
                "1": "Down",
                "2": "Left",
                "3": "Upper"
            }
            part = {
                "Right":    {"0": "2", "1": "5", "2": "8"},
                "Down":     {"0": "8", "1": "7", "2": "6"},
                "Left":     {"0": "6", "1": "3", "2": "0"},
                "Upper":    {"0": "0", "1": "1", "2": "2"}
            }
            direct = ''
            if move == "B":
                direct = "horario"
            elif move == "B'":
                direct = "antihorario"
        elif move == "D" or move == "D'":
            moviment = "Down"
            adjacente = {
                "0": "Left",
                "1": "Back",
                "2": "Right",
                "3": "Front"
            }
            part = {
                "Left":     {"0": "8", "1": "7", "2": "6"},
                "Back":     {"0": "8", "1": "7", "2": "6"},
                "Right":    {"0": "8", "1": "7", "2": "6"},
                "Front":    {"0": "8", "1": "7", "2": "6"}
            }
            direct = ''
            if move == "D":
                direct = "horario"
            elif move == "D'":
                direct = "antihorario"

        if direct == "horario":
            newface = {
                '0': self.cube[moviment]['6'],
                '1': self.cube[moviment]['3'],
                '2': self.cube[moviment]['0'],
                '3': self.cube[moviment]['7'],
                '4': self.cube[moviment]['4'],
                '5': self.cube[moviment]['1'],
                '6': self.cube[moviment]['8'],
                '7': self.cube[moviment]['5'],
                '8': self.cube[moviment]['2']
            }
            self.cube[moviment] = newface
            adj = adjacente['0']
            aux = {
                '0': self.cube[adj][part[adj]['0']],
                '1': self.cube[adj][part[adj]['1']],
                '2': self.cube[adj][part[adj]['2']],
            }
            for i in range(0, 3):
                adj1 = adjacente[str(i)]
                adj2 = adjacente[str(i+1)]
                self.cube[adj1][part[adj1]['0']] = self.cube[adj2][part[adj2]['0']]
                self.cube[adj1][part[adj1]['1']] = self.cube[adj2][part[adj2]['1']]
                self.cube[adj1][part[adj1]['2']] = self.cube[adj2][part[adj2]['2']]

            adj = adjacente['3']
            self.cube[adj][part[adj]['0']] = aux['0']
            self.cube[adj][part[adj]['1']] = aux['1']
            self.cube[adj][part[adj]['2']] = aux['2']

        elif direct == "antihorario":
            newface = {
                '0': self.cube[moviment]['2'],
                '1': self.cube[moviment]['5'],
                '2': self.cube[moviment]['8'],
                '3': self.cube[moviment]['1'],
                '4': self.cube[moviment]['4'],
                '5': self.cube[moviment]['7'],
                '6': self.cube[moviment]['0'],
                '7': self.cube[moviment]['3'],
                '8': self.cube[moviment]['6']
            }

            self.cube[moviment] = newface
            adj = adjacente['3']
            aux = {
                '0': self.cube[adj][part[adj]['0']],
                '1': self.cube[adj][part[adj]['1']],
                '2': self.cube[adj][part[adj]['2']],
            }
            for i in range(3, 0, -1):
                adj1 = adjacente[str(i)]
                adj2 = adjacente[str(i-1)]
                self.cube[adj1][part[adj1]['0']] = self.cube[adj2][part[adj2]['0']]
                self.cube[adj1][part[adj1]['1']] = self.cube[adj2][part[adj2]['1']]
                self.cube[adj1][part[adj1]['2']] = self.cube[adj2][part[adj2]['2']]

            adj = adjacente['0']
            self.cube[adj][part[adj]['0']] = aux['0']
            self.cube[adj][part[adj]['1']] = aux['1']
            self.cube[adj][part[adj]['2']] = aux['2']

    def scramble_gen(self):
        scramble = [0] * self.slen
        for x in range(len(scramble)):
            scramble[x] = [0] * 2
        return scramble

    def scramble_replace(self, ar):
        for x in range(len(ar)):
            ar[x][0] = random.choice(self.moves)
            ar[x][1] = random.choice(self.direction)
        return self.sprint(self.valid(ar))

    def valid(self, ar):
        for x in range(1, len(ar)):
            while ar[x][0] == ar[x-1][0]:
                ar[x][0] = random.choice(self.moves)
        for x in range(2, len(ar)):
            while ar[x][0] == ar[x-2][0] or ar[x][0] == ar[x-1][0]:
                ar[x][0] = random.choice(self.moves)
        return ar

    def sprint(self, ar):
        result = ''
        for x in range(len(ar)):
            result += (str(ar[x][0]) + str(ar[x][1]) + " ")
        return result[:-1]

    def finishedCube(self):
        colors = {}
        colors['r'] = 0
        colors['o'] = 0
        colors['y'] = 0
        colors['g'] = 0
        colors['b'] = 0
        colors['w'] = 0
        error = 0
        for face in self.cube:
            for color in self.cube[face]:
                try:
                    color = self.cube[face][color]
                    colors[color] += 1
                except NameError:
                    error = 1

        for color in colors:
            if(error or colors[color] != 9):
                return False

        return True


# scramble = cubo.scramble_replace(cubo.scramble_gen())
# scramble = scramble.split(" ")
# cubo.validMovements(scramble)

# cubo = Rubik({
#     "Upper":    {"0": "o", "1": "w", "2": "g", "3": "y", "4": "y", "5": "b", "6": "b", "7": "b", "8": "b"},
#     "Left":     {"0": "y", "1": "b", "2": "w", "3": "g", "4": "g", "5": "w", "6": "r", "7": "w", "8": "r"},
#     "Front":    {"0": "r", "1": "o", "2": "o", "3": "g", "4": "o", "5": "g", "6": "y", "7": "y", "8": "o"},
#     "Right":    {"0": "w", "1": "r", "2": "o", "3": "o", "4": "b", "5": "o", "6": "w", "7": "y", "8": "g"},
#     "Back":     {"0": "y", "1": "r", "2": "b", "3": "w", "4": "r", "5": "r", "6": "w", "7": "y", "8": "y"},
#     "Down":     {"0": "g", "1": "o", "2": "g", "3": "b", "4": "w", "5": "r", "6": "b", "7": "g", "8": "r"}})
# movements = "L' B' U B' R' L L D' R R B L' F U U B B D F F U D F F B B R R"

# cubo = Rubik({
#     "Upper":    {"0": "b", "1": "b", "2": "g", "3": "g", "4": "y", "5": "o", "6": "y", "7": "g", "8": "g"},
#     "Left":     {"0": "y", "1": "r", "2": "r", "3": "y", "4": "r", "5": "y", "6": "b", "7": "r", "8": "b"},
#     "Front":    {"0": "g", "1": "o", "2": "o", "3": "g", "4": "g", "5": "w", "6": "o", "7": "r", "8": "g"},
#     "Right":    {"0": "y", "1": "b", "2": "w", "3": "o", "4": "o", "5": "y", "6": "w", "7": "b", "8": "b"},
#     "Back":     {"0": "o", "1": "w", "2": "r", "3": "o", "4": "b", "5": "r", "6": "w", "7": "w", "8": "w"},
#     "Down":     {"0": "y", "1": "w", "2": "r", "3": "b", "4": "w", "5": "y", "6": "r", "7": "g", "8": "o"}
# })
# movements = "D D L' U R' L' F' D D B' R B D B B D L L U U B B U' L L F F U"

# movements = movements.split(" ")
# if cubo.validMovements(movements):
#     for move in movements:
#         cubo.move(move)
# print(cubo.cube)

# moves = finishedsolve.split(" ")
# finishedmoves = ""
# for move in moves:
#     if move == "F2":
#         finishedmoves += "F F"
#     elif move == "B2":
#         finishedmoves += "B B"
#     elif move == "R2":
#         finishedmoves += "R R"
#     elif move == "L2":
#         finishedmoves += "L L"
#     elif move == "U2":
#         finishedmoves += "U U"
#     elif move == "D2":
#         finishedmoves += "D D"
#     elif move == "M":
#         finishedmoves += "R L"
#     elif move == "M'":
#         finishedmoves += "R' L'"
#     elif move == "M2":
#         finishedmoves += "R L R L"
#     else:
#         finishedmoves += move
#     finishedmoves += " "

# finishedmoves = finishedmoves[:-1]
# print(finishedmoves)
