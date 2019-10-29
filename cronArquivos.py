import Database
import datetime
import compiler


def rodarFilaArquivos(every_minute):
    print("Rodando Fila de Arquivos a cada " + str(every_minute) + " minuto(s)")
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
                envios = db.query('SELECT * FROM envios WHERE env_status = 0')
            if envios:
                for envio in envios:
                    print(envio)
                    with Database.Database('rubik_platform.db') as db:
                        estados = db.query(
                            'SELECT * FROM estados_cubo ORDER BY cub_robo DESC LIMIT 5', ())
                    if estados:
                        comp = compiler.Compiler(envio['env_filename'])
                        success = comp.Compile(estados)

                        if success:
                            print("sucesso")
                            with Database.Database('rubik_platform.db') as db:
                                db.execute("UPDATE envios SET env_status = ? WHERE env_id = ?", (1, envio['env_id']))
                        else:
                            print("erro")
                            with Database.Database('rubik_platform.db') as db:
                                db.execute("UPDATE envios SET env_status = ? WHERE env_id = ?", (2, envio['env_id']))
                    else:
                        print("Não há estados disponiveis")
            print("fim")
            

print(__name__)
print("CronArquivo")

if __name__ == "__main__":
    rodarFilaArquivos(1)
