@app.route('/consulta_relatorio', methods=['GET', 'POST'])
def consultar_relatorio():
    if request.method == 'GET':
        return render_template('consulta_relatorio.html')
    
    if request.method == 'POST':
        motorista = request.form['motorista']
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta para obter os resultados filtrados
        query = """
            SELECT m.nome, v.placa, 
                STRING_AGG(r.nome, ', ') AS regioes,
                e.data_entrega, v.tipo_veiculo, 
                e.km_rodado, e.quantidade_notas_fiscais, e.quantidade_coletas
            FROM 
                entrega AS e
            INNER JOIN motorista AS m ON e.motorista_id = m.motorista_id
            INNER JOIN veiculo AS v ON e.veiculo_id = v.veiculo_id
            INNER JOIN entrega_regiao AS er ON e.entrega_id = er.entrega_id
            INNER JOIN regiao AS r ON er.regiao_id = r.regiao_id
            WHERE
                e.status = 'FINALIZADO'
        """

        # Filtros
        conditions = []
        params = []

        if motorista:
            conditions.append("m.nome = %s")
            params.append(motorista)
        if data_inicial:
            conditions.append("e.data_entrega >= %s")
            params.append(data_inicial)
        if data_final:
            conditions.append("e.data_entrega <= %s")
            params.append(data_final)

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += """
            GROUP BY
                e.numero_entrega, e.data_entrega, m.nome, v.tipo_veiculo, v.placa, 
                e.quantidade_notas_fiscais, e.quantidade_coletas, e.km_rodado
        """

        cur.execute(query, tuple(params))
        results = cur.fetchall()

        # Consulta para calcular a soma de km rodado com os mesmos filtros
        query_total_km = """
            SELECT SUM(e.km_rodado)
            FROM entrega AS e
            INNER JOIN motorista AS m ON e.motorista_id = m.motorista_id
            WHERE e.status = 'FINALIZADO'
        """

        if conditions:
            query_total_km += " AND " + " AND ".join(conditions)

        cur.execute(query_total_km, tuple(params))
        total_km = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({'resultados': results, 'total_km': total_km})