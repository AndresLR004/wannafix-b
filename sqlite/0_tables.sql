CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    password TEXT NOT NULL,
    email_token TEXT DEFAULT NULL,
    verified INTEGER NOT NULL DEFAULT 0, -- Cambiado FALSE a 0
    auth_token TEXT DEFAULT NULL,
    auth_token_expiration DATETIME DEFAULT NULL,
    created DATETIME NOT NULL DEFAULT (DATETIME('now')),
    updated DATETIME NOT NULL DEFAULT (DATETIME('now'))
);

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    photo TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    duration_hours INTEGER NOT NULL,
    duration_days INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    user_id INTEGER, -- Hemos eliminado la restricción NOT NULL
    created DATETIME NOT NULL DEFAULT (DATETIME('now')),
    updated DATETIME NOT NULL DEFAULT (DATETIME('now')),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (status_id) REFERENCES statuses(id),
    FOREIGN KEY (user_id) REFERENCES users(id) -- Hemos añadido una clave foránea opcional
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE
);

CREATE TABLE statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    slug TEXT UNIQUE
);

CREATE TABLE download_info_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    admin_role_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT (DATETIME('now')),
    FOREIGN KEY (user_id) REFERENCES users(id),
    -- Supongo que tienes una tabla roles
    FOREIGN KEY (admin_role_id) REFERENCES roles(id) 
    -- Asumí que tienes una tabla roles, asegúrate de reemplazar 'roles' con el nombre real de tu tabla de roles
);



-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL UNIQUE,
--     email TEXT NOT NULL UNIQUE,
--     role TEXT NOT NULL,
--     password TEXT NOT NULL,
--     email_token TEXT DEFAULT NULL,
--     verified INTEGER NOT NULL DEFAULT 0, -- Cambiado FALSE a 0
--     auth_token TEXT DEFAULT NULL,
--     auth_token_expiration DATETIME DEFAULT NULL,
--     created DATETIME NOT NULL DEFAULT (DATETIME('now')),
--     updated DATETIME NOT NULL DEFAULT (DATETIME('now'))
-- );

-- CREATE TABLE services (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     title TEXT NOT NULL,
--     description TEXT NOT NULL,
--     photo TEXT NOT NULL,
--     price DECIMAL(10, 2) NOT NULL,
--     duration_hours INTEGER NOT NULL,
--     duration_days INTEGER NOT NULL,
--     category_id INTEGER NOT NULL,
--     status_id INTEGER NOT NULL,
--     user_id INTEGER, -- Hemos eliminado la restricción NOT NULL
--     created DATETIME NOT NULL DEFAULT (DATETIME('now')),
--     updated DATETIME NOT NULL DEFAULT (DATETIME('now')),
--     FOREIGN KEY (category_id) REFERENCES categories(id),
--     FOREIGN KEY (status_id) REFERENCES statuses(id),
--     FOREIGN KEY (user_id) REFERENCES users(id) -- Hemos añadido una clave foránea opcional
-- );

-- CREATE TABLE categories (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL UNIQUE,
--     slug TEXT NOT NULL UNIQUE
-- );

-- CREATE TABLE statuses (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT UNIQUE,
--     slug TEXT UNIQUE
-- );

-- CREATE TABLE download_info_users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     admin_role_id INTEGER NOT NULL,
--     timestamp DATETIME NOT NULL DEFAULT (DATETIME('now')),
--     FOREIGN KEY (user_id) REFERENCES users(id),
--     -- Supongo que tienes una tabla roles
--     FOREIGN KEY (admin_role_id) REFERENCES roles(id) 
--     -- Asumí que tienes una tabla roles, asegúrate de reemplazar 'roles' con el nombre real de tu tabla de roles
-- );
