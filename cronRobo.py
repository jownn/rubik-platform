import Database
import datetime
import serial
import compiler
import time as t


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
                fila_robo = db.query('SELECT * FROM fila_robo JOIN envios ON env_id = rob_idenvio WHERE rob_status = 0 AND env_status = 1')
            if fila_robo:
                for row in fila_robo:
                    print(row)
                    with Database.Database('rubik_platform.db') as db:
                        estados = db.query(
                            'SELECT * FROM estados_cubo ORDER BY cub_robo DESC LIMIT 5', ())
                    if estados:
                        comp = compiler.Compiler(row['env_filename'])
                        movements = comp.Compile(estados, True)
                        print(movements)
                        if movements:
                            ser = serial.Serial('/dev/ttyUSB0')
                            ser.write(movements.encode())
                            with Database.Database('rubik_platform.db') as db:
                                db.execute("UPDATE fila_robo SET rob_status = ? WHERE rob_id = ?", (1, row['rob_id']))
                            ser.close()

            print("Fim")


print(__name__)
print("CronRobo")

if __name__ == "__main__":
    rodarFilaArquivos(1)
