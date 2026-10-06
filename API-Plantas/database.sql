-- Execute este arquivo na aba SQL do phpMyAdmin.
CREATE DATABASE IF NOT EXISTS api_plantas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE api_plantas;

-- A tabela está no plural e possui exatamente 7 colunas consultadas no JSON.
CREATE TABLE IF NOT EXISTS plantas (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome_popular VARCHAR(100) NOT NULL,
    nome_cientifico VARCHAR(120) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    necessidade_luz VARCHAR(50) NOT NULL,
    frequencia_rega_dias INT UNSIGNED NOT NULL,
    toxica TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO plantas
    (id, nome_popular, nome_cientifico, tipo, necessidade_luz, frequencia_rega_dias, toxica)
VALUES
    (1, 'Jiboia', 'Epipremnum aureum', 'Trepadeira', 'Luz indireta', 7, 1),
    (2, 'Espada-de-São-Jorge', 'Dracaena trifasciata', 'Herbácea', 'Meia-sombra ou sol', 14, 1),
    (3, 'Zamioculca', 'Zamioculcas zamiifolia', 'Herbácea', 'Pouca luz', 14, 1),
    (4, 'Violeta-africana', 'Streptocarpus ionanthus', 'Florífera', 'Luz indireta', 5, 0),
    (5, 'Alecrim', 'Salvia rosmarinus', 'Erva aromática', 'Sol pleno', 3, 0),
    (6, 'Costela-de-adão', 'Monstera deliciosa', 'Trepadeira', 'Luz indireta', 7, 1),
    (7, 'Samambaia-americana', 'Nephrolepis exaltata', 'Samambaia', 'Meia-sombra', 3, 0),
    (8, 'Lavanda', 'Lavandula angustifolia', 'Arbusto', 'Sol pleno', 5, 0);

