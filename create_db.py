import datetime
import Database

with Database.Database('rubik_platform.db') as db:

    db.execute("""
        CREATE TABLE cadastros (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            tipo VARCHAR(7) NOT NULL CHECK(tipo IN('admin','usuario')),
            data_adicionado DATETIME NOT NULL,
            nome VARCHAR(255) NOT NULL,
            usuario VARCHAR(45) NOT NULL,
            senha VARCHAR(45) NOT NULL
        );
    """)

    db.execute("""
        CREATE TABLE compiladores (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            extensao varchar(45) NOT NULL,
            comando TEXT NOT NULL,
            tipoEntrada VARCHAR(5) NOT NULL CHECK(tipoEntrada IN('texto','json'))
        );
    """)

    db.execute("""
        CREATE TABLE envios (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            status INTEGER NOT NULL DEFAULT 0,
            data_adicionado DATETIME NOT NULL,
            idcadastro INTEGER NOT NULL,
            arquivo TEXT NOT NULL,
            extensao VARCHAR(45) NOT NULL,
            FOREIGN KEY(idcadastro) REFERENCES cadastro(id)
        );
    """)

    db.execute("""
        CREATE TABLE fila_robo (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data_adicionado DATETIME NOT NULL,
            idenvio INTEGER NOT NULL,
            FOREIGN KEY(idenvio) REFERENCES envio(id)
        )
    """)

    print('Tabelas criada com sucesso.')

    # Inserido dados

    # cadastro
    lista = [('admin', datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Administrador', 'admin', 'admin')]

    db.execute_many("""
    INSERT INTO cadastros (tipo, data_adicionado, nome, usuario, senha)
    VALUES (?,?,?,?,?)
    """, lista)

    lista = [
            ('py', '/usr/bin/python {!source_code!} < {!intxt!} > {!outtxt!}', 'texto'),
            ('cpp', '/usr/bin/g++ {!source_code!} -o {!out!} && ./{!out!} < {!intxt!} > {!outtxt!}', 'texto'),
        ]

    db.execute_many("""
    INSERT INTO compiladores (extensao, comando, tipoEntrada)
    VALUES (?,?,?)
    """, lista)

    db.commit()

    print('Dados inseridos com sucesso.')
