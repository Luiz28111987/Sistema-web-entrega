-- Consulta regiões
SELECT  DISTINCT regiao FROM dados
	ORDER BY regiao
	;

-- Padronizar regiões
UPDATE dados
SET regiao = 'NUCLEO BANDEIRANTE'
WHERE regiao = 'NUCLEO'
;

--
UPDATE dados
SET regiao = 'VICENTE PIRES'
WHERE regiao = 'VICENTE'
;

-- Inserindo motoristas
INSERT INTO motorista(nome)
	SELECT  DISTINCT motorista FROM dados
	ORDER BY motorista
	;

--Inserindo regiões
INSERT INTO regiao(nome)
	SELECT  DISTINCT regiao FROM dados
	ORDER BY regiao
	;

--Inserindo veiculos
INSERT INTO veiculo(tipo_veiculo, placa)
	SELECT tipo_veiculo, placa FROM dados
	GROUP BY tipo_veiculo, placa
	;

--Inserindo entregas
INSERT INTO entrega(
	numero_entrega, data_entrega, hora_saida, km_inicial, km_final, 
    motorista_id, veiculo_id, quantidade_notas_fiscais, quantidade_coletas, status
)
SELECT DISTINCT d.numero_entrega, d.data_entrega, d.hora_saida, d.km_inicial, d.km_final, 
m.motorista_id, v.veiculo_id, d.quantidade_notas_fiscais, d.quantidade_coletas, 'FINALIZADO' AS status
	FROM dados AS d
	INNER JOIN motorista AS m ON d.motorista = m.nome
	INNER JOIN veiculo AS v ON d.placa = v.placa
	;

--Inserindo relacionamento entrega / regiao
INSERT INTO entrega_regiao (entrega_id, regiao_id)
	SELECT e.entrega_id, r.regiao_id
	FROM dados AS d
	INNER JOIN entrega AS e ON d.numero_entrega = e.numero_entrega
	INNER JOIN regiao AS r ON d.regiao = r.nome
	;

--Dropando a tabela dados para que seja inserido novo arquivo de dados de combustivel
DROP TABLE dados;

--inserindo dados de combustivel
INSERT INTO combustivel(veiculo_id, data_abastecimento, tipo_combustivel, quantidade_combustivel, valor_abastecido)
	SELECT v.veiculo_id, d.data_abastecimento, d.tipo_combustivel, d.quantidade_combustivel, d.valor_abastecido 
	FROM dados AS d
	INNER JOIN veiculo AS v ON v.placa = d.placa
	;

--Dropando tabela dados para limpar banco de tabelas desnecessarias
DROP TABLE dados;