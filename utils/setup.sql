-- Crear la tabla de registros si no existe
CREATE TABLE IF NOT EXISTS "secret-santa".users (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    deseo1 TEXT NOT NULL,
    link_deseo1 TEXT,
    deseo2 TEXT NOT NULL,
    link_deseo2 TEXT,
    deseo3 TEXT,
    link_deseo3 TEXT,
    estacion VARCHAR(50) NOT NULL UNIQUE
);

COMMIT;