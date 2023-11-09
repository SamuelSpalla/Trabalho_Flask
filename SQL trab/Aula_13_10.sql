CREATE DATABASE aula_13_10;

USE aula_13_10;

CREATE TABLE setor (
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(50) NOT NULL
);

CREATE TABLE funcionarios(
id INT AUTO_INCREMENT PRIMARY KEY,
primeiro_nome VARCHAR(50) NOT NULL,
sobrenome VARCHAR(50) NOT NULL,
data_admissao DATE NOT NULL,
status_funcionario BOOL NOT NULL,
id_setor INT,
FOREIGN KEY (id_setor) REFERENCES setor(id)
);

CREATE TABLE cargos(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(50),
id_setor INT,
FOREIGN KEY (id_setor) REFERENCES setor(id)
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

ALTER TABLE cargos MODIFY COLUMN nome VARCHAR(50) NOT NULL;

ALTER TABLE funcionarios ADD COLUMN id_cargo INT;
ALTER TABLE funcionarios ADD FOREIGN KEY (id_cargo) REFERENCES cargos(id);


insert into usuarios (username, senha) values ('admin', '1234');


INSERT INTO setor (nome)
VALUES
('TI'),
('RH'),
('ADM');

INSERT INTO cargos (nome, id_setor)
VALUES
('Rei', 1),
('Dev Jr', 1),
('Dev Pleno', 1),
('Gerente RH', 2),
('Gerente ADM', 3);


INSERT INTO funcionarios (primeiro_nome, sobrenome, data_admissao, status_funcionario, id_setor, id_cargo)
VALUES
('Samuel', 'Spalla', '2023-10-23', 1, 1, 1),
('Ed', 'Belloti', '1985-10-11', 1, 1, 2),
('Matheus', 'Caetano', '1997-04-20', 1, 2, 3),
('Yago', 'Guimarães', '1996-05-07', 0, 1, 4),
('Fabricio', 'Dias', '2023-11-08', 1, 1, 4),
('Pipico', 'Ele mesmo', '2023-11-08', 1, 3, 3),
('Raphael', 'Cardim', '2023-11-08', 1, 1, 4);







