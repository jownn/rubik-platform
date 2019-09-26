
def rodarFilaArquivos():
    filename = secure_filename(file.filename)
    filenamewext = filename.rsplit('.', 1)[0].lower()
    ext = filename.rsplit('.', 1)[1].lower()
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

        os.system(comando)