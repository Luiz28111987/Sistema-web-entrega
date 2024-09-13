-- Consulta regiões
SELECT  DISTINCT regiao FROM dados
	ORDER BY regiao;

-- Padronizar regiões
UPDATE dados
SET regiao = 'NUCLEO BANDEIRANTE'
WHERE regiao = 'NUCLEO';

--
UPDATE dados
SET regiao = 'VICENTE PIRES'
WHERE regiao = 'VICENTE';

-- Inserindo motoristas
INSERT INTO motorista(nome)
	SELECT  DISTINCT motorista FROM dados
	ORDER BY motorista;

--Inserindo regiões
INSERT INTO regiao(nome)
	SELECT  DISTINCT regiao FROM dados
	ORDER BY regiao;

--Inserindo veiculos
INSERT INTO veiculo(tipo_veiculo, placa)
	SELECT tipo_veiculo, placa FROM dados
	GROUP BY tipo_veiculo, placa;

--Inserindo entregas
INSERT INTO entrega(
	numero_entrega, data_entrega, hora_saida, km_inicial, km_final, 
    motorista_id, veiculo_id, quantidade_notas_fiscais, quantidade_coletas, status
)
SELECT d.numero_entrega, d.data_entrega, d.hora_saida, d.km_inicial, d.km_final, 
m.motorista_id, v.veiculo_id, d.quantidade_notas_fiscais, d.quantidade_coletas, 'FINALIZADO' AS status
	FROM dados AS d
	INNER JOIN motorista AS m ON d.motorista = m.nome
	INNER JOIN veiculo AS v ON d.placa = v.placa;

--