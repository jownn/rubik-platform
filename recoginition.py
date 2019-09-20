import time as t
import json
import numpy as np
import cv2 as cv
import serial


FACES = {
    1: 'Upper',
    2: 'Left',
    3: 'Front',
    4: 'Right',
    5: 'Back',
    6: 'Down',
}

CUBO = {
    'Upper': {},
    'Left': {},
    'Front': {},
    'Right': {},
    'Back': {},
    'Down': {},
}


def get_cube():
    square_size = 40
    space_size = 60
    draw_size = (square_size * 3) + (space_size * 4)
    draw_step = square_size + space_size
    cap = cv.VideoCapture(0)
    time = t.time()
    img = np.array([])
    global FACES
    global CUBO
    num_faces = 6
    num_face = 1

    while True:
        ret, frame = cap.read()
        height, width = frame.shape[0], frame.shape[1]
        point_x, point_y = ((width - draw_size)/2) + \
            space_size, ((height - draw_size)/2) + space_size
        rect = []

        for i in range(0, 9):
            if i % 3 != 0:
                point_x += draw_step
            else:
                point_x = (width - draw_size)/2 + space_size
                if i > 0:
                    point_y += draw_step
            point_x = int(point_x)
            point_y = int(point_y)
            rect.append([point_x, point_y])
            cv.rectangle(
                         frame,
                         (point_x, point_y),
                         (point_x+square_size, point_y + square_size),
                         (255, 255, 255),
                         2
                        )
        font = cv.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        thickness = 2

        cv.putText(frame, 'Verificando: ' + FACES[num_face], org, font, fontScale, (255, 0, 0), thickness, cv.LINE_AA)

        if(t.time() > time + 10 and num_face <= num_faces):
            img = frame
            time = t.time()
            count = 0
            face = FACES[num_face]
            CUBO[face] = {}
            for point in rect:
                point_x, point_y = point[0], point[1]
                area = img[point_y:point_y+square_size,
                           point_x:point_x+square_size]
                mean = contar_kmeans(area)
                cv.rectangle(
                             img,
                             (point_x, point_y),
                             (point_x+square_size, point_y+square_size),
                             (int(mean[0]), int(mean[1]), int(mean[2])),
                             cv.FILLED
                            )
                color = get_colour_name(
                    int(mean[0]), int(mean[1]), int(mean[2]))
                CUBO[face][count] = color
                count += 1
            num_face += 1

        if num_face > num_faces:
            if verifica_cubo():
                # texto
                try:
                    nome_arquivo = '../rubik-platform/uploads/input/in_texto.txt'
                    arquivo = open(nome_arquivo, 'r+')
                except FileNotFoundError:
                    arquivo = open(nome_arquivo, 'w+')
                for face in CUBO:
                    for color in CUBO[face]:
                        arquivo.writelines(CUBO[face][color][0])
                arquivo.close()

                # json
                try:
                    nome_arquivo = '../rubik-platform/uploads/input/in_json.txt'
                    arquivo = open(nome_arquivo, 'r+')
                except FileNotFoundError:
                    arquivo = open(nome_arquivo, 'w+')
                arquivo.writelines(json.dumps(CUBO))
                arquivo.close()

                break
            else:
                num_face = 1

        cv.imshow('rubik_capture', frame)
        if img.any():
            cv.imshow('img', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def verifica_cubo():
    colors = {}
    colors['r'] = 0
    colors['o'] = 0
    colors['y'] = 0
    colors['g'] = 0
    colors['b'] = 0
    colors['w'] = 0
    error = 0
    for face in CUBO:
        for color in CUBO[face]:
            try:
                color = CUBO[face][color]
                colors[color] += 1
            except NameError:
                error = 1

    for color in colors:
        if(error or colors[color] != 9):
            return False

    return True


def getSerial():
    # Iniciando conexao serial
    comport = serial.Serial('/dev/ttyUSB0', 9600)
    # Setando timeout 1s para a conexao
    # comport = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    # param_caracter = 't'
    param_ascii = str(chr(116))       # Equivalente 116 = t

    # Time entre a conexao serial e o tempo para escrever (enviar algo)
    t.sleep(1.8)  # Entre 1.5s a 2s

    # comport.write(param_caracter)
    comport.write(param_ascii)

    value_serial = comport.readline()

    print('\nRetorno da serial: %s' % (value_serial))

    # Fechando conexao serial
    comport.close()


def contar_kmeans(img):
    data = np.reshape(img, (-1, 3))
    data = np.float32(data)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv.kmeans(
        data, 1, None, criteria, 10, flags)
    return centers[0]


def get_colour_name(b, g, r):
    bgr = np.uint8([[[b, g, r]]])
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    hue = int(hsv[0][0][0])
    saturation = int(hsv[0][0][1])
    value = int(hsv[0][0][2])
    if hue >= 0 and hue <= 4:
        color = "r"
    elif hue >= 5 and hue <= 24:
        color = "o"
    elif hue >= 25 and hue <= 38:
        color = "y"
    elif hue >= 43 and hue <= 65:
        color = "g"
    elif hue >= 110 and hue <= 125:
        color = "b"
    else:
        color = "erro"

    if saturation < 25 and value >= 170:
        color = "w"

    return color


if __name__ == '__main__':
    get_cube()
