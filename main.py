import os
from app import app
from flask import flash, redirect, render_template, request, session, jsonify
from werkzeug.utils import secure_filename
import Database
import recoginition
import datetime
import rubik
import json

PERMISSIONS = ['home', 'listaEnvios']


def getExtensions():
    with Database.Database('rubik_platform.db') as db:
        extensoes = db.query('SELECT * FROM compiladores')
    result = []
    for extensao in extensoes:
        result.append(extensao["extensao"])
    return result


@app.context_processor
def context():
    return dict(cadastroLogado=getUserLogged())


def allowed_file(filename):
    extensions = getExtensions()
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


def getUserLogged():
    with Database.Database('rubik_platform.db') as db:
        cadastro = db.query('SELECT * FROM cadastros WHERE id = ?', (session.get('idCadastro'),))
    if cadastro:
        return cadastro[0]
    else:
        return False


def permissions(func):
    if func in PERMISSIONS:
        return True
    else:
        if(getUserLogged()['tipo'] == 'admin'):
            return True
        else:
            return False


@app.route('/')
def index():
    return redirect('/home')


@app.route('/home')
def home():
    func = 'home'
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        extensions = getExtensions()
        if extensions:
            allowedExtentions = '.'
            for i in range(0, len(extensions)):
                allowedExtentions += extensions[i]
                if i < len(extensions)-1:
                    allowedExtentions += ', .'
        with Database.Database('rubik_platform.db') as db:
            extensions = db.query('SELECT * FROM compiladores')
        cubo = []
        with Database.Database('rubik_platform.db') as db:
            estado_cubo = db.query('SELECT * FROM estados_cubo WHERE robo = 1 LIMIT 1')
        if estado_cubo:
            cores = estado_cubo[0]['estado_texto']
        else:
            cores = 'bbbbbbbbbooooooooowwwwwwwwwrrrrrrrrryyyyyyyyyggggggggg'
        estilo = ''
        for i in range(0, len(cores)):
            if cores[i] == 'b':
                estilo = "background-color: blue; color:white;"
            elif cores[i] == "o":
                estilo = "background-color: orange;"
            elif cores[i] == "w":
                estilo = "background-color: white;"
            elif cores[i] == "r":
                estilo = "background-color: red; color:white"
            elif cores[i] == "g":
                estilo = "background-color: green; color:white"
            elif cores[i] == 'y':
                estilo = "background-color: yellow;"
            cubo.append(estilo)

        cadastro = getUserLogged()
        return render_template('main.html', func=func, allowedExtentions=allowedExtentions, extensions=extensions, cubo=cubo, cadastro=cadastro)


@app.route('/home/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        dirname = os.path.dirname(__file__)
        path = ''.join([dirname, app.config['UPLOAD_FOLDER']])
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', category='danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading', category='danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(path, filename))
            try:
                with Database.Database('rubik_platform.db') as db:
                    db.execute("INSERT INTO envios (data_adicionado, idcadastro, filename, extensao) VALUES (?,?,?,?)", (datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), session.get('idCadastro'), filename, ext))
                flash('Arquivo adicionado com sucesso, aguarde a verificação. Para consultar <a href="" class="alert-link">clique aqui</a>.', category='success')
            except:
                flash('Erro', category='danger')
            return redirect('/')
        else:
            flash('Tipo de arquivo não permitido', category='danger')
            return redirect('/home')
    else:
        return redirect('/home')


@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('/home')


@app.route('/login', methods=['POST'])
def do_login():
    with Database.Database('rubik_platform.db') as db:
        cadastro = db.query(
            'SELECT * FROM cadastros WHERE usuario = ?', (request.form['username'],))
    if cadastro and request.form['password'] == cadastro[0]['senha']:
        session['logged_in'] = True
        session['idCadastro'] = cadastro[0]['id']
    else:
        flash('Usuario/Senha incorreta', category='danger')
    return redirect('/')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')


@app.route('/listaEnvios')
def listaEnvios():
    func = 'listaEnvios'
    if not session.get('logged_in'):
        return redirect('/login')
    elif not permissions(func):
        return redirect('/home')
    else:
        wh = ''
        if getUserLogged()['tipo'] == 'usuario':
            wh = 'WHERE idcadastro = ' + str(session.get('idCadastro'))
        with Database.Database('rubik_platform.db') as db:
            envios = db.query('SELECT * FROM envios ' + wh)
        return render_template('listaEnvios.html', func=func, envios=envios)


@app.route('/configuracoes')
def config():
    func = 'config'
    if not session.get('logged_in'):
        return redirect('/login')
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            compiladores = db.query('SELECT * FROM compiladores')
            cadastros = db.query('SELECT * FROM cadastros WHERE id != 1')
            estados = db.query('SELECT * FROM estados_cubo')
        return render_template('config.html', func=func, compiladores=compiladores, cadastros=cadastros, estados=estados)


@app.route('/configuracoes/adicionarCompilador')
def adicionarCompilador():
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        return render_template('addEditCompilador.html', func=func, compilador=False)


@app.route('/configuracoes/editarCompilador/<idCompilador>')
def editarCompilador(idCompilador):
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            compilador = db.query('SELECT * FROM compiladores WHERE id = ?', (idCompilador,))
        if compilador:
            return render_template('addEditCompilador.html', func=func, compilador=compilador[0])
        else:
            flash('Compilador não encontrado', category='danger')
            return redirect('/configuracoes')


@app.route('/configuracoes/adicionarCompilador', methods=['POST'])
def insertCompilador():
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            db.execute("INSERT INTO compiladores (extensao, comando, tipoEntrada) VALUES (?,?,?)", (request.form['extensao'], request.form['comando'], request.form['entrada'], ))
        flash('Compilador adicionado com sucesso', category='success')
    return redirect('/configuracoes')


@app.route('/configuracoes/editarCompilador/<idCompilador>', methods=['POST'])
def editCompilador(idCompilador):
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            db.execute("UPDATE compiladores SET extensao = ?, comando = ?, tipoEntrada = ? WHERE id = ?", (request.form['extensao'], request.form['comando'], request.form['entrada'], idCompilador))
        flash('Compilador editado com sucesso', category='success')
    return redirect('/configuracoes')


@app.route('/configuracoes/excluirCompilador/<idCompilador>')
def deleteCompilador(idCompilador):
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            db.execute('DELETE FROM compiladores WHERE id = ?', (idCompilador,))
            flash('Compilador excluído com sucesso', category='success')
        return redirect('/configuracoes')


@app.route('/configuracoes/adicionarCadastro')
def adicionarCadastro():
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        return render_template('addEditCadastro.html', func=func, cadastro=False)


@app.route('/configuracoes/editarCadastro/<idCadastro>')
def editarCadastro(idCadastro):
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            cadastro = db.query('SELECT * FROM cadastros WHERE id = ? AND id != 1', (idCadastro,))
        if cadastro:
            return render_template('addEditCadastro.html', func=func, cadastro=cadastro[0])
        else:
            flash('Cadastro não encontrado', category='danger')
            return redirect('/configuracoes')


@app.route('/configuracoes/adicionarCadastro', methods=['POST'])
def insertCadastro():
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            cadastro = db.query('SELECT * FROM cadastros WHERE usuario = ?', (request.form['usuario'],))
        if cadastro:
            flash('Usuário já existe', category='danger')
            return redirect('/configuracoes/adicionarCadastro')
        with Database.Database('rubik_platform.db') as db:
            db.execute("INSERT INTO cadastros (tipo, data_adicionado, nome, usuario, senha) VALUES (?,?,?,?,?)", (request.form['tipo'], datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), request.form['nome'], request.form['usuario'], request.form['senha'], ))
        flash('Cadastro adicionado com sucesso', category='success')
    return redirect('/configuracoes')


@app.route('/configuracoes/editarCadastro/<idCadastro>', methods=['POST'])
def editCadastro(idCadastro):
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            cadastro = db.query('SELECT * FROM cadastros WHERE usuario = ? AND id != ?', (request.form['usuario'], idCadastro,))
        if cadastro:
            flash('Usuário já existe', category='danger')
            return redirect('/configuracoes/adicionarCadastro')
        with Database.Database('rubik_platform.db') as db:
            db.execute("UPDATE cadastros SET tipo = ?, nome = ?, usuario = ?, senha = ? WHERE id = ?", (request.form['tipo'], request.form['nome'], request.form['usuario'], request.form['senha'], idCadastro))
        flash('Cadastro editado com sucesso', category='success')
    return redirect('/configuracoes')


@app.route('/configuracoes/excluirCadastro/<idCadastro>')
def deleteCadastro(idCadastro):
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            db.execute('DELETE FROM cadastros WHERE id = ?', (idCadastro,))
            flash('Cadastro excluído com sucesso', category='success')
        return redirect('/configuracoes')


@app.route('/configuracoes/excluirEstado/<idEstado>')
def deleteEstado(idEstado):
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        with Database.Database('rubik_platform.db') as db:
            db.execute('DELETE FROM estados_cubo WHERE id = ?', (idEstado,))
            flash('Estado excluído com sucesso', category='success')
        return redirect('/configuracoes')


@app.route('/configuracoes/capturarCubo/')
def capturarCubo():
    func = 'config'
    if not session.get('logged_in'):
        return False
    elif not permissions(func):
        return redirect('/home')
    else:
        try:
            recoginition.get_cube()
            flash('Cubo capturado com sucesso', 'success')
        except:
            flash('Ocorreu um erro, verifique as conexões', 'danger')
            return redirect('/configuracoes')
    return redirect('/configuracoes')


@app.route('/configuracoes/gerarNovoEstado')
def gerarNovoEstado():
    try:
        cubo = rubik.Rubik()
        scramble = cubo.scramble_replace(cubo.scramble_gen())
        scramble = scramble.split(" ")
        if cubo.validMovements(scramble):
            for move in scramble:
                cubo.move(move)

        texto = ''
        for face in cubo.cube:
            for color in cubo.cube[face]:
                texto += cubo.cube[face][color]
        with Database.Database('rubik_platform.db') as db:
            db.execute("INSERT INTO estados_cubo (estado_texto, estado_json, robo) VALUES (?,?,?)", (texto, json.dumps(cubo.cube), 0))
        flash('Novo estado adicionado com sucesso', 'success')
    except:
        flash('Ocorreu um erro ao adicionar', 'danger')
    return redirect('/configuracoes')

if __name__ == "__main__":
    app.run(debug=True)
