CRIAR DATABASE
trabalho_extensao


-- Tabela Motorista
CREATE TABLE motorista (
    motorista_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela Veiculo
CREATE TABLE veiculo (
    veiculo_id SERIAL PRIMARY KEY,
    tipo_veiculo VARCHAR(20) NOT NULL,
    placa CHAR(8) NOT NULL UNIQUE
);

-- Tabela Regiao
CREATE TABLE regiao (
    regiao_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela Entrega
CREATE TABLE entrega (
    entrega_id SERIAL PRIMARY KEY,
    numero_entrega INT NOT NULL,
    data_entrega DATE NOT NULL,
    hora_saida TIME NOT NULL,
    km_inicial INTEGER NOT NULL,
    km_final INTEGER NULL,
    km_rodado INTEGER GENERATED ALWAYS AS (km_final - km_inicial) STORED,
    motorista_id INT REFERENCES motorista(motorista_id),
    veiculo_id INT REFERENCES veiculo(veiculo_id),
    quantidade_notas_fiscais INTEGER NOT NULL,
    quantidade_coletas INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL
);

-- Tabela Entrega_Regiao (Tabela intermediária)
CREATE TABLE entrega_regiao (
    id SERIAL PRIMARY KEY,
    entrega_id INT REFERENCES entrega(entrega_id),
    regiao_id INT REFERENCES regiao(regiao_id)
);

-- Tabela Combustivel
CREATE TABLE combustivel (
    id SERIAL PRIMARY KEY,
    veiculo_id INT REFERENCES veiculo(veiculo_id),
    data_abastecimento DATE NOT NULL,
    tipo_combustivel CHAR (20),
    quantidade_combustivel NUMERIC (6,4) NOT NULL,
    valor_abastecido REAL NOT NULL
);