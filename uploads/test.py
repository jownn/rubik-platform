from rubik_solver import utils

cubo = input('')
faces = {}
faces['upper'] = ''
faces['left'] = ''
faces['front'] = ''
faces['right'] = ''
faces['back'] = ''
faces['down'] = ''

cores = []
cores.append(cubo[4])
cores.append(cubo[13])
cores.append(cubo[22])
cores.append(cubo[31])
cores.append(cubo[40])
cores.append(cubo[49])

for i in range(0, 6):
    if cores[i] == 'y':
        numface = 4
        face = 'upper'
    elif cores[i] == 'b':
        numface = 13
        face = 'left'
    elif cores[i] == 'r':
        numface = 22
        face = 'front'
    elif cores[i] == 'g':
        numface = 31
        face = 'right'
    elif cores[i] == 'o':
        numface = 40
        face = 'back'
    elif cores[i] == 'w':
        numface = 49
        face = 'down'

    for j in range(-4, 5):
        faces[face] += cubo[numface+j]

newcubo = faces['upper'] + faces['left'] + faces['front'] + faces['right'] + faces['back'] + faces['down']

solve = utils.solve(newcubo, 'Kociemba')
finishedsolve = " ".join(str(x) for x in solve)

moves = finishedsolve.split(" ")
finishedmoves = ""
for move in moves:
    if move == "F2":
        finishedmoves += "F F"
    elif move == "B2":
        finishedmoves += "B B"
    elif move == "R2":
        finishedmoves += "R R"
    elif move == "L2":
        finishedmoves += "L L"
    elif move == "U2":
        finishedmoves += "U U"
    elif move == "D2":
        finishedmoves += "D D"
    elif move == "M":
        finishedmoves += "R L"
    elif move == "M'":
        finishedmoves += "R' L'"
    elif move == "M2":
        finishedmoves += "R L R L"
    else:
        finishedmoves += move
    finishedmoves += " "

finishedmoves = finishedmoves[:-1]
print(finishedmoves)
