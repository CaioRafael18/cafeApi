DROP TABLE IF EXISTS tb_usuario;

CREATE TABLE tb_usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    nascimento DATE NOT NULL
);

DROP TABLE IF EXISTS tb_categoria;
CREATE TABLE tb_categoria (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS tb_setor;
CREATE TABLE tb_setor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS tb_produto;
CREATE TABLE tb_produto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    categoria_id INTEGER NOT NULL,
    setor_id INTEGER NOT NULL,
    foreign key (categoria_id) references tb_categoria(id),
    foreign key (setor_id) references tb_setor(id)
);

insert into tb_usuario(nome, nascimento) values ('Administrador', '2024-07-23');