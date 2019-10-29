import Database
import os
import rubik
import json


class Compiler():

    def __init__(self, filename):
        self.filename = filename

    def Compile(self, estados={}):
        filename = self.filename.rsplit('.', 1)
        filenamewext = filename[0].lower()
        ext = filename[1].lower()
        with Database.Database('rubik_platform.db') as db:
            compiler = db.query(
                'SELECT * FROM compiladores WHERE com_extensao = ? LIMIT 1', (ext,))
        if compiler:
            compiler = compiler[0]
            source_code = "uploads/source_code/" + self.filename
            intxt = "uploads/input/in_" + compiler['com_tipoEntrada'] + ".txt"
            outtxt = "uploads/output/out_" + filenamewext + ".txt"
            out = "uploads/source_code/out"

            comando = compiler['com_comando']
            comando = comando.replace('{!source_code!}', source_code)
            comando = comando.replace('{!intxt!}', intxt)
            comando = comando.replace('{!outtxt!}', outtxt)
            comando = comando.replace('{!out!}', out)

            if estados:
                success = 0
                for estado in estados:
                    nome_arquivo = 'uploads/input/in_' + compiler['com_tipoEntrada'] + '.txt'
                    arquivo = open(nome_arquivo, 'w')
                    arquivo.writelines(estado['cub_estado_' + compiler['com_tipoEntrada']])
                    arquivo.close()
                    os.system(comando)

                    nome_arquivo = 'uploads/output/out_' + filenamewext + '.txt'
                    arquivo = open(nome_arquivo, 'r')
                    out = arquivo.readline()
                    out = out.rstrip('\n')
                    movements = out.split(" ")

                    cubo = rubik.Rubik(json.loads(estado['cub_estado_json']))
                    if cubo.validMovements(movements):
                        for move in movements:
                            cubo.move(move)

                        if cubo.finishedCube():
                            success += 1

            if success == len(estados):
                return True
            else:
                return False
