import datetime
import Database

with Database.Database('rubik_platform.db') as db:

    db.execute("""
        CREATE TABLE cadastros (
            cad_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            cad_tipo VARCHAR(7) NOT NULL CHECK(cad_tipo IN('admin','usuario')),
            cad_data_adicionado DATETIME NOT NULL,
            cad_nome VARCHAR(255) NOT NULL,
            cad_usuario VARCHAR(45) NOT NULL,
            cad_senha VARCHAR(45) NOT NULL
        );
    """)

    db.execute("""
        CREATE TABLE compiladores (
            com_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            com_extensao varchar(45) NOT NULL,
            com_comando TEXT NOT NULL,
            com_tipoEntrada VARCHAR(5) NOT NULL CHECK(com_tipoEntrada IN('texto','json'))
        );
    """)

    db.execute("""
        CREATE TABLE envios (
            env_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            env_status INTEGER NOT NULL DEFAULT 0,
            env_data_adicionado DATETIME NOT NULL,
            env_idcadastro INTEGER NOT NULL,
            env_filename TEXT NOT NULL,
            env_extensao VARCHAR(45) NOT NULL,
            FOREIGN KEY(env_idcadastro) REFERENCES cadastro(cad_id)
        );
    """)

    db.execute("""
        CREATE TABLE estados_cubo (
            cub_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            cub_estado_texto TEXT NOT NULL,
            cub_estado_json TEXT NOT NULL,
            cub_robo INTEGER NOT NULL DEFAULT 0
        );
    """)

    db.execute("""
        CREATE TABLE fila_robo (
            rob_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            rob_status INTEGER NOT NULL DEFAULT 0,
            rob_data_adicionado DATETIME NOT NULL,
            rob_idenvio INTEGER NOT NULL,
            FOREIGN KEY(rob_idenvio) REFERENCES envio(env_id)
        )
    """)

    print('Tabelas criada com sucesso.')

    # Inserido dados

    # cadastro
    lista = [('admin', datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Administrador', 'admin', 'admin')]

    db.execute_many("""
    INSERT INTO cadastros (cad_tipo, cad_data_adicionado, cad_nome, cad_usuario, cad_senha)
    VALUES (?,?,?,?,?)
    """, lista)

    lista = [
            ('py', 'python {!source_code!} < {!intxt!} > {!outtxt!}', 'texto'),
            ('cpp', 'g++ {!source_code!} -o {!out!} && ./{!out!} < {!intxt!} > {!outtxt!}', 'texto'),
        ]

    db.execute_many("""
    INSERT INTO compiladores (com_extensao, com_comando, com_tipoEntrada)
    VALUES (?,?,?)
    """, lista)

    db.commit()

    print('Dados inseridos com sucesso.')
