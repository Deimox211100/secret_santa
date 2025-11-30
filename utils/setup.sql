-- Crear la tabla de registros si no existe
CREATE TABLE IF NOT EXISTS "secret-santa".users (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    deseo1 TEXT NOT NULL,
    link_deseo1 TEXT,
    imagen_deseo1 TEXT,
    deseo2 TEXT NOT NULL,
    link_deseo2 TEXT,
    imagen_deseo2 TEXT,
    deseo3 TEXT,
    link_deseo3 TEXT,
    imagen_deseo3 TEXT,
    character_name VARCHAR(100) NOT NULL UNIQUE,
    character_photo_url TEXT,
    password VARCHAR(255) NOT NULL,
    wishes_locked BOOLEAN DEFAULT FALSE
);

COMMIT;