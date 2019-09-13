import os
from app import app
from flask import flash, redirect, render_template, request, session, jsonify
from werkzeug.utils import secure_filename
import Database
import solver


ALLOWED_EXTENSIONS = ['c', 'py']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return redirect('/home')


@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        if ALLOWED_EXTENSIONS:
            allowedExtentions = '.'
            for i in range(0, len(ALLOWED_EXTENSIONS)):
                allowedExtentions += ALLOWED_EXTENSIONS[i]
                if i < len(ALLOWED_EXTENSIONS)-1:
                    allowedExtentions += ', .'
        cubo = []
        try:
            nome_arquivo = '../rubik-platform/uploads/input/in_texto.txt'
            arquivo = open(nome_arquivo, 'r+')
            cores = arquivo.readlines()
            arquivo.close()
        except FileNotFoundError:
            cores = [
                'azul', 'azul', 'azul', 'azul', 'azul', 'azul', 'azul', 'azul', 'azul',
                'laranja', 'laranja', 'laranja', 'laranja', 'laranja', 'laranja', 'laranja', 'laranja', 'laranja',
                'branco', 'branco', 'branco', 'branco', 'branco', 'branco', 'branco', 'branco', 'branco',
                'vermelho', 'vermelho', 'vermelho', 'vermelho', 'vermelho', 'vermelho', 'vermelho', 'vermelho', 'vermelho',
                'verde', 'verde', 'verde', 'verde', 'verde', 'verde', 'verde', 'verde', 'verde',
                'amarelo', 'amarelo', 'amarelo', 'amarelo', 'amarelo', 'amarelo', 'amarelo', 'amarelo', 'amarelo',
            ]

        estilo = ''
        for cor in cores:
            cor = cor.rstrip('\n')
            if cor == 'azul':
                estilo = "background-color: blue; color:white;"
            elif cor == "laranja":
                estilo = "background-color: orange;"
            elif cor == "branco":
                estilo = "background-color: white;"
            elif cor == "vermelho":
                estilo = "background-color: red; color:white"
            elif cor == "verde":
                estilo = "background-color: green; color:white"
            elif cor == 'amarelo':
                estilo = "background-color: yellow;"
            cubo.append(estilo)
        return render_template('main.html', allowedExtentions=allowedExtentions, cubo=cubo)


@app.route('/home', methods=['POST'])
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
            file.save(os.path.join(path, filename))
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

                flash('File successfully uploaded', category='success')
            else:
                flash('Erro', category='danger')
            return redirect('/')
        else:
            flash('Tipo de arquivo não permitido', category='danger')
            return redirect(request.url)


@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('/home')


@app.route('/login', methods=['POST'])
def do_admin_login():
    with Database.Database('rubik_platform.db') as db:
        cadastro = db.query(
            'SELECT * FROM cadastro WHERE usuario = ?', (request.form['username'],))
    if cadastro and request.form['password'] == cadastro[0]['senha']:
        session['logged_in'] = True
    else:
        flash('Usuario/Senha incorreta', category='danger')
    return redirect('/')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')


@app.route('/configuracoes')
def config():
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        with Database.Database('rubik_platform.db') as db:
            compiladores = db.query('SELECT * FROM compiladores')
        return render_template('config.html', compiladores=compiladores)


@app.route('/adicionarCompilador')
def adicionarCompilador():
    if not session.get('logged_in'):
        return False
    else:
        return render_template('addEditCompilador.html', compilador=False)


@app.route('/editarCompilador/<idCompilador>')
def editarCompilador(idCompilador):
    if not session.get('logged_in'):
        return False
    else:
        with Database.Database('rubik_platform.db') as db:
            compilador = db.query('SELECT * FROM compiladores WHERE id = ?', (idCompilador,))
        if compilador:
            return render_template('addEditCompilador.html', compilador=compilador[0])
        else:
            flash('Compilador não encontrado', category='danger')
            return redirect('/configuracoes')


@app.route('/adicionarCompilador', methods=['POST'])
def insertCompilador():
    if not session.get('logged_in'):
        return False
    else:
        with Database.Database('rubik_platform.db') as db:
            db.execute("INSERT INTO compiladores (extensao, comando, tipoEntrada) VALUES (?,?,?)", (request.form['extensao'], request.form['comando'], request.form['entrada'], ))
        flash('Compilador adicionado com sucesso', category='success')
    return redirect('/configuracoes')


@app.route('/editarCompilador/<idCompilador>', methods=['POST'])
def editCompilador(idCompilador):
    if not session.get('logged_in'):
        return False
    else:
        with Database.Database('rubik_platform.db') as db:
            db.execute("UPDATE compiladores SET extensao = ?, comando = ?, tipoEntrada = ? WHERE id = ?", (request.form['extensao'], request.form['comando'], request.form['entrada'], idCompilador))
        flash('Compilador editado com sucesso', category='success')
    return redirect('/configuracoes')


@app.route('/excluirCompilador/<idCompilador>')
def deleteCompilador(idCompilador):
    if not session.get('logged_in'):
        return False
    else:
        with Database.Database('rubik_platform.db') as db:
            db.execute('DELETE FROM compiladores WHERE id = ?', (idCompilador,))
            flash('Compilador excluído com sucesso', category='success')
        return redirect('/configuracoes')


@app.route('/capturarCubo/')
def capturarCubo():
    if not session.get('logged_in'):
        return False
    else:
        solver.get_cube()
    return redirect('/configuracoes')


if __name__ == "__main__":
    app.run(debug=True)
