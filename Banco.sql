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
    placa VARCHAR(10) NOT NULL UNIQUE
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
    km_inicial NUMERIC(10,2) NOT NULL,
    km_final NUMERIC(10,2) NULL,
    km_rodado NUMERIC(10,2) GENERATED ALWAYS AS (KM_Final - KM_Inicial) STORED,
    motorista_id INT REFERENCES motorista(motorista_id),
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

-- Tabela Motorista_Veiculo (Tabela intermediária)
CREATE TABLE motorista_veiculo (
    id SERIAL PRIMARY KEY,
    motorista_id INT REFERENCES motorista(motorista_id),
    veiculo_id INT REFERENCES veiculo(veiculo_id)
);
