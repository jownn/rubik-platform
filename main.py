import os
from app import app
from flask import flash, redirect, render_template, request, session
from werkzeug.utils import secure_filename
import Database

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

        return render_template('main.html', allowedExtentions=allowedExtentions)


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
        flash('Usuario/Senha incorreta')
    return redirect('/')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')


@app.route('/home', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        dirname = os.path.dirname(__file__)
        path = ''.join([dirname, app.config['UPLOAD_FOLDER']])
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(path, filename))
            ext = filename.rsplit('.', 1)[1].lower()
            if ext == 'py':
                os.system("/usr/bin/python2.7 uploads/source_code/%s < uploads/input/in_%s > uploads/output/out_%s" %
                          (filename, filename, filename))
            elif ext == 'c':
                os.system("/usr/bin/g++ uploads/source_code/%s -o uploads/source_code/out && ./uploads/source_code/out < uploads/input/in_%s > uploads/output/out_%s" %
                          (filename, filename, filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are c, py')
            return redirect(request.url)


@app.route('/configuracoes')
def config():
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        with Database.Database('rubik_platform.db') as db:
            compiladores = db.query('SELECT * FROM compiladores')
        return render_template('config.html', compiladores=compiladores)


if __name__ == "__main__":
    app.run(debug=True)
