import Database
import datetime
import os
import rubik
import json


def rodarFilaArquivos(every_minute):
    rodou = False
    minute = datetime.datetime.now().strftime('%M')
    while(True):
        if minute != datetime.datetime.now().strftime('%M'):
            rodou = False
        if not (int(datetime.datetime.now().strftime('%M')) % every_minute) and not rodou:
            rodou = True
            with Database.Database('rubik_platform.db') as db:
                envios = db.query('SELECT * FROM envios WHERE status = 0')
            if envios:
                for envio in envios:
                    print(envio)
                    filename = envio['filename'].rsplit('.', 1)
                    filenamewext = filename[0].lower()
                    ext = filename[1].lower()
                    with Database.Database('rubik_platform.db') as db:
                        compiler = db.query(
                            'SELECT * FROM compiladores WHERE extensao = ? LIMIT 1', (ext,))
                    if compiler:
                        compiler = compiler[0]
                        print(compiler)
                        source_code = "uploads/source_code/" + envio['filename']
                        intxt = "uploads/input/in_" + compiler['tipoEntrada'] + ".txt"
                        outtxt = "uploads/output/out_" + filenamewext + ".txt"
                        out = "uploads/source_code/out"

                        comando = compiler['comando']
                        comando = comando.replace('{!source_code!}', source_code)
                        comando = comando.replace('{!intxt!}', intxt)
                        comando = comando.replace('{!outtxt!}', outtxt)
                        comando = comando.replace('{!out!}', out)

                        with Database.Database('rubik_platform.db') as db:
                            estados = db.query(
                                'SELECT * FROM estados_cubo ORDER BY robo DESC LIMIT 5', ())

                        if estados:
                            success = 0
                            for estado in estados:
                                print(estado)
                                nome_arquivo = '../rubik-platform/uploads/input/in_' + compiler['tipoEntrada'] + '.txt'
                                arquivo = open(nome_arquivo, 'w')
                                arquivo.writelines(estado['estado_' + compiler['tipoEntrada']])
                                arquivo.close()
                                os.system(comando)

                                nome_arquivo = '../rubik-platform/uploads/output/out_' + filenamewext + '.txt'
                                arquivo = open(nome_arquivo, 'r')
                                out = arquivo.readline()
                                out = out.rstrip('\n')
                                movements = out.split(" ")

                                cubo = rubik.Rubik(json.loads(estado['estado_json']))
                                if cubo.validMovements(movements):
                                    for move in movements:
                                        cubo.move(move)

                                    if cubo.finishedCube():
                                        print('sucesso')
                                        success += 1
                                    else:
                                        print('errou')
                        if success == len(estados):
                            with Database.Database('rubik_platform.db') as db:
                                db.execute("UPDATE envios SET status = ? WHERE id = ?", (1, envio['id']))
                        else:
                            with Database.Database('rubik_platform.db') as db:
                                db.execute("UPDATE envios SET status = ? WHERE id = ?", (2, envio['id']))


if __name__ == "__main__":
    rodarFilaArquivos(1)
