import sqlite3
import datetime

conn = sqlite3.connect('rubik_platform.db')
cursor = conn.cursor()

# Criando a tabelas

cursor.execute("""
    CREATE TABLE cadastro (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        tipo VARCHAR(7) NOT NULL CHECK(tipo IN('admin','usuario')),
        data_adicionado DATETIME NOT NULL,
        usuario VARCHAR(45) NOT NULL,
        senha VARCHAR(45) NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE compiladores (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        extensao varchar(45) NOT NULL,
        comando TEXT NOT NULL,
        so VARCHAR(7) NOT NULL CHECK(so IN('windows','linux'))
    );
""")

cursor.execute("""
    CREATE TABLE entrada (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        data_adicionado DATETIME NOT NULL,
        arquivo TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE teste (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        status INTEGER NOT NULL DEFAULT 1,
        data_adicionado DATETIME NOT NULL,
        idcadastro INTEGER NOT NULL,
        arquivo TEXT NOT NULL,
        extensao VARCHAR(45) NOT NULL,
        acertou BOOLEAN,
        qtd_movimentos INT,
        FOREIGN KEY(idcadastro) REFERENCES cadastro(id)
    );
""")

print('Tabelas criada com sucesso.')

# Inserido dados

# cadastro
lista = [('admin', datetime.datetime.now(), 'admin', 'admin')]

cursor.executemany("""
INSERT INTO cadastro (tipo, data_adicionado, usuario, senha)
VALUES (?,?,?,?)
""", lista)

conn.commit()

print('Dados inseridos com sucesso.')

conn.close()