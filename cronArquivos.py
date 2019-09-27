import Database
import datetime
import os
import rubik

def rodarFilaArquivos(minute):
    if datetime.now().strftime('%M') == minute:
        with Database.Database('rubik_platform.db') as db:
            envios = db.query('SELECT * FROM envios WHERE status = 0')
        if envios:
            for envio in envios:
                filename = envio['filename'].rsplit('.', 1)
                filenamewext = filename[0].lower()
                ext = filename[1].lower()
                with Database.Database('rubik_platform.db') as db:
                    compiler = db.query(
                        'SELECT * FROM compiladores WHERE extensao = ? LIMIT 1', (ext,))
                if compiler:

                    compiler = compiler[0]
                    source_code = "uploads/source_code/" + filename
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
                            # texto
                            nome_arquivo = '../rubik-platform/uploads/input/in_texto.txt'
                            arquivo = open(nome_arquivo, 'w+')
                            arquivo.writelines(estado['estado_texto'])
                            arquivo.close()

                            # json
                            nome_arquivo = '../rubik-platform/uploads/input/in_json.txt'
                            arquivo = open(nome_arquivo, 'w+')
                            arquivo.writelines(estado['estado_json'])
                            arquivo.close()
                            os.system(comando)

                            nome_arquivo = '../rubik-platform/uploads/output/out_' + filenamewext + '.txt'
                            arquivo = open(nome_arquivo, 'r')
                            out = arquivo.readline()

                            cubo = rubik.Rubik(estado['estado_json'])
                            if cubo.validMovements(out):
                                for move in out:
                                    cubo.move(move)

                            if cubo.finishedCube():
                                success += 1
                        if success == 5:
                            with Database.Database('rubik_platform.db') as db:
                                db.execute("UPDATE compiladores SET extensao = ?, comando = ?, tipoEntrada = ? WHERE id = ?", (request.form['extensao'], request.form['comando'], request.form['entrada'], idCompilador))
