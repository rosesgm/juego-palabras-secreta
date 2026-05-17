CREATE IF NOT EXISTS DATABASE crossover_db;
USE crossover_db;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(85) NOT NULL UNIQUE,
    password VARCHAR(450) NOT NULL,
    profile TINYINT(1) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS level (
    id             INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    level_number   TINYINT      NOT NULL UNIQUE,
    title          VARCHAR(120) NOT NULL,
    image_filename VARCHAR(255) NOT NULL,
    hint           TEXT         NOT NULL,
    encrypted_word TEXT         NOT NULL
);
-- Cambien el nombre de la columna --
ALTER TABLE level CHANGE encrypted_word word TEXT NOT NULL;