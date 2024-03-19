-- Script do Banco de Dados Players


-- Criando Schema
begin;
drop schema if exists players; 
create schema players;
use players;

-- Criando as tabelas

-- Tabela para jogadores
CREATE TABLE players_info (
    player_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    player_nick VARCHAR(255)
);

-- Tabela para estatísticas de jogador
CREATE TABLE players_statics (
    player_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    score_axis DOUBLE NOT NULL,
    score_alies DOUBLE NOT NULL
);

-- Inserir players
INSERT INTO players_info (player_id, player_nick)
VALUES  (1001,	'Pepe Popo'),
        (1002,	'Zero'),
        (1003,	'Liquid'),
        (1004,	'Shadow'),
        (1005,	'Muca'),
        (1006,	'Brujoga10'),
        (1007,	'Luck'),
        (1008,	'Nargoth');


-- Inserir estatísticas
INSERT INTO players_statics (player_id, score_axis, score_alies)
VALUES  (1001,	7.5 , 6.0),
        (1002,	9.5 , 8.5),
        (1003,	7.5 , 8.0),
        (1004,	7.0 , 7.0),
        (1005,	6.0 , 9.0),
        (1006,	8.5 , 8.8),
        (1007,	8.0 , 8.2),
        (1008,	8.1 , 7.9);



