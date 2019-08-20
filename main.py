import os
from app import app
from flask import Flask, flash, redirect, render_template, request, session, abort
from werkzeug.utils import secure_filename
import subprocess

ALLOWED_EXTENSIONS = set(['c', 'py'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('upload.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('Senha incorreta')
    return redirect('/')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/', methods=['POST'])
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
                os.system("/usr/bin/python2.7 uploads/source_code/%s < uploads/input/in_%s > uploads/output/out_%s" % (filename,filename,filename))
            elif ext == 'c':
                os.system("/usr/bin/g++ uploads/source_code/%s -o uploads/source_code/out && ./uploads/source_code/out < uploads/input/in_%s > uploads/output/out_%s" % (filename,filename,filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are c, py')
            return redirect(request.url)


if __name__ == "__main__":
    app.run()
