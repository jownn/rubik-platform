import Database
import datetime
import os
import rubik
import json
import serial


def rodarFilaArquivos(every_minute):
    print("Rodando Fila para envio do robô a cada " + str(every_minute) + " minuto(s)")
    rodou = False
    minute = datetime.datetime.now().strftime('%M')
    while(True):
        if minute != datetime.datetime.now().strftime('%M'):
            minute = datetime.datetime.now().strftime('%M')
            rodou = False
        if not (int(datetime.datetime.now().strftime('%M')) % every_minute) and not rodou:
            print("Verificando..")
            rodou = True
            with Database.Database('rubik_platform.db') as db:
                fila_robo = db.query('SELECT * FROM fila_robo JOIN envios ON env_id = rob_idenvio WHERE rob_status = 1 AND env_status = 1')
            if fila_robo:
                for row in fila_robo:
                    print(row)
                    ser = serial.Serial('/dev/ttyUSB0')
                    ser.write(b'hello')
                    ser.close()

print(__name__)
print("CronRobo")

if __name__ == "__main__":
    rodarFilaArquivos(1)
