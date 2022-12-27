CREATE TABLE IF NOT EXISTS clients_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rut TEXT,
    name TEXT,
    phone TEXT,
    mail TEXT
);

CREATE TABLE IF NOT EXISTS clients_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client  INTEGER NOT NULL,
    points INTEGER NOT NULL,
    date_creation DATE NOT NULL,
    date_last_update DATE NOT NULL,
    time_grab INTEGER NOT NULL,
    referido_bool BOOLEAN NOT NULL,
    id_referido INTEGER NOT NULL,
    CONSTRAINT fk_clients
        FOREIGN KEY (id_client)
        REFERENCES clients_info(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER NOT NULL,
    type_trans TEXT NOT NULL,
    date_trans DATETIME NOT NULL,
    monto INTEGER NOT NULL,
    saldo INTEGER NOT NULL,
    CONSTRAINT fk_clients2
        FOREIGN KEY (id_client)
        REFERENCES clients_info(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vencimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER NOT NULL,
    puntos INTEGER NOT NULL,
    date_venc DATE NOT NULL,
    CONSTRAINT fk_clients2
        FOREIGN KEY (id_client)
        REFERENCES clients_info(id)
        ON DELETE CASCADE
);