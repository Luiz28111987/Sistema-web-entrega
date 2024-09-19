from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2 import errors

from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        database="trabalho_extensao",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    return conn
@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/cadastra_motorista', methods=['GET', 'POST'])
def cadastro_motorista():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            nome_motorista = request.form['motorista'].upper()

            # Verifica se o motorista já está cadastrado
            cur.execute("SELECT motorista_id FROM motorista WHERE nome = %s", (nome_motorista,))
            motorista_existente = cur.fetchone()

            if motorista_existente:
                # Se já existe, pega o próximo ID novamente e exibe o erro
                cur.execute("SELECT COALESCE(MAX(motorista_id), 0) + 1 FROM motorista")
                proximo_id = cur.fetchone()[0]
                return render_template('cadastra_motorista.html', 
                                       proximo_id=proximo_id, 
                                       erro="Motorista já cadastrado.")

            # Faz a inserção sem pegar o próximo ID manualmente
            cur.execute("INSERT INTO motorista (nome) VALUES (%s)", (nome_motorista,))
            conn.commit()
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard após cadastro
        
        except Exception as e:
            conn.rollback()
            return jsonify({'erro': str(e)})
        finally:
            cur.close()
            conn.close()

    try:
        # Obtenha o próximo ID para exibir na página (sem incrementar a sequência)
        cur.execute("SELECT COALESCE(MAX(motorista_id), 0) + 1 FROM motorista")
        proximo_id = cur.fetchone()[0]
    except Exception as e:
        proximo_id = None
        print(f"Erro ao buscar o próximo ID: {e}")
    finally:
        cur.close()
        conn.close()

    return render_template('cadastra_motorista.html', proximo_id=proximo_id)

@app.route('/cadastra_veiculo', methods=['GET', 'POST'])
def cadastra_veiculo():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            tipo_veiculo = request.form['tipo_veiculo'].upper()
            placa = request.form['placa'].upper()

            # Verifica se o veiculo já está cadastrado
            cur.execute("SELECT veiculo_id FROM veiculo WHERE placa = %s", (placa,))
            veiculo_existente = cur.fetchone()

            if veiculo_existente:
                # Se já existe, pega o próximo ID novamente e exibe o erro
                cur.execute("SELECT COALESCE(MAX(veiculo_id), 0) + 1 FROM veiculo")
                proximo_id = cur.fetchone()[0]
                return render_template('cadastra_veiculo.html', 
                                       proximo_id=proximo_id, 
                                       erro="Veículo já cadastrado.")

            # Faz a inserção sem pegar o próximo ID manualmente
            cur.execute("INSERT INTO veiculo (tipo_veiculo, placa) VALUES (%s,%s)", (tipo_veiculo, placa))
            conn.commit()
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard após cadastro
        
        except Exception as e:
            conn.rollback()
            return jsonify({'erro': str(e)})
        finally:
            cur.close()
            conn.close()

    try:
        # Obtenha o próximo ID para exibir na página (sem incrementar a sequência)
        cur.execute("SELECT COALESCE(MAX(veiculo_id), 0) + 1 FROM veiculo")
        proximo_id = cur.fetchone()[0]
    except Exception as e:
        proximo_id = None
        print(f"Erro ao buscar o último ID: {e}")
    finally:
        cur.close()
        conn.close()

    return render_template('cadastra_veiculo.html', proximo_id=proximo_id)

@app.route('/cadastra_regiao', methods=['GET', 'POST'])
def cadastra_regiao():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            regiao = request.form['regiao'].upper()

            # Verifica se o motorista já está cadastrado
            cur.execute("SELECT regiao_id FROM regiao WHERE nome = %s", (regiao,))
            regiao_existente = cur.fetchone()

            if regiao_existente:
                # Se já existe, pega o próximo ID novamente e exibe o erro
                cur.execute("SELECT COALESCE(MAX(regiao_id), 0) + 1 FROM regiao")
                proximo_id = cur.fetchone()[0]
                return render_template('cadastra_regiao.html', 
                                       proximo_id=proximo_id, 
                                       erro="Região já cadastrada.")

            # Faz a inserção sem pegar o próximo ID manualmente
            cur.execute("INSERT INTO regiao (nome) VALUES (%s)", (regiao,))
            conn.commit()
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard após cadastro
        
        
        except Exception as e:
            conn.rollback()
            return jsonify({'erro': str(e)})
        finally:
            cur.close()
            conn.close()

    try:
        # Obtenha o próximo ID para exibir na página (sem incrementar a sequência)
        cur.execute("SELECT COALESCE(MAX(regiao_id), 0) + 1 FROM regiao")
        proximo_id = cur.fetchone()[0]
    except Exception as e:
        proximo_id = None
        print(f"Erro ao buscar o último ID: {e}")
    finally:
        cur.close()
        conn.close()

    return render_template('cadastra_regiao.html', proximo_id=proximo_id)

@app.route('/inserir_entrega', methods=['GET', 'POST'])
def inserir_entrega():
    if request.method == 'POST':
        # Capturar os dados inseridos pelo usuário
        numero_entrega = request.form['numero_entrega']
        motorista = request.form['motorista']
        placa = request.form['placa']
        veiculo = request.form['veiculo']
        km_inicial = request.form['km_inicial']
        num_notas = request.form['num_notas']
        #regioes = request.form['regioes_input']
        regioes = request.form.get('regioes', '')  # Use .get() para evitar KeyError

        print(f"numero_notas{num_notas}, regioes{regioes}")

        data_entrega = datetime.now().strftime('%Y/%m/%d')
        hora_saida = datetime.now().strftime('%H:%M:%S')
        km_final = '0'
        quantidade_coletas = '0'
        status = 'AGUARDANDO RETORNO'

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Buscar o ID do motorista pelo nome
            cur.execute("SELECT motorista_id FROM motorista WHERE nome = %s", (motorista,))
            motorista_id_result = cur.fetchone()
            if not motorista_id_result:
                return render_template('inserir_entrega.html', error_message="Motorista não encontrado", numero_entrega=numero_entrega, motorista=motorista, placa=placa, veiculo=veiculo, km_inicial=km_inicial, num_notas=num_notas, regioes=regioes)
            motorista_id = motorista_id_result[0]

            # Buscar o ID do veículo pela placa
            cur.execute("SELECT veiculo_id FROM veiculo WHERE placa = %s", (placa,))
            veiculo_id_result = cur.fetchone()
            if not veiculo_id_result:
                return render_template('inserir_entrega.html', error_message="Veículo não encontrado", numero_entrega=numero_entrega, motorista=motorista, placa=placa, veiculo=veiculo, km_inicial=km_inicial, num_notas=num_notas, regioes=regioes)
            veiculo_id = veiculo_id_result[0]

            # Inserir a entrega no banco de dados
            cur.execute('''
                INSERT INTO entrega (numero_entrega, data_entrega, hora_saida, km_inicial, km_final, motorista_id, veiculo_id, quantidade_notas_fiscais, quantidade_coletas, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING entrega_id
            ''', (numero_entrega, data_entrega, hora_saida, km_inicial, km_final, motorista_id, veiculo_id, num_notas, quantidade_coletas, status))

            # Agora buscamos o ID da entrega recém-inserida
            entrega_id = cur.fetchone()[0]

            # Processar as regiões inseridas
            regioes_list = [regiao.strip() for regiao in regioes.split('/')]
            for regiao in regioes_list:
                print(regiao)
                # Buscar o ID da região pelo nome
                cur.execute("SELECT regiao_id FROM regiao WHERE nome = %s", (regiao,))
                regiao_id_result = cur.fetchone()

                if not regiao_id_result:
                    return render_template('inserir_entrega.html', error_message=f"Região '{regiao}' não encontrada", numero_entrega=numero_entrega, motorista=motorista, placa=placa, veiculo=veiculo, km_inicial=km_inicial, num_notas=num_notas, regioes=regioes)
                
                regiao_id = regiao_id_result[0]
                print(f'regiao id {regiao_id}')

                # Inserir na tabela entrega_regiao
                cur.execute('''
                    INSERT INTO entrega_regiao (entrega_id, regiao_id)
                    VALUES (%s, %s)
                ''', (entrega_id, regiao_id))

            # Fazer o commit das alterações no banco de dados
            conn.commit()

        except Exception as e:
            print(f"Erro ao inserir entrega: {e}")
            return render_template('inserir_entrega.html', error_message="Ocorreu um erro ao inserir a entrega.", numero_entrega=numero_entrega, motorista=motorista, placa=placa, veiculo=veiculo, km_inicial=km_inicial, num_notas=num_notas, regioes=regioes)
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('dashboard'))

    return render_template('inserir_entrega.html')

@app.route('/numero_entrega', methods=['GET'])
def numero_entrega():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Lógica GET: Buscar o próximo número de entrega
        cur.execute("SELECT MAX(numero_entrega) FROM entrega")
        ultimo_id = cur.fetchone()[0]
        if ultimo_id is None:
            ultimo_id = 0
        proximo_id = ultimo_id + 1
    finally:
        cur.close()
        conn.close()

    return jsonify(proximo_id=proximo_id)

@app.route('/finalizar_entrega', methods=['GET'])
def finalizar_entrega():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Consulta para obter os dados
    cur.execute("""SELECT e.numero_entrega, e.data_entrega, e.hora_saida, e.km_inicial, e.km_final,
    m.nome, v.tipo_veiculo, v.placa, e.quantidade_notas_fiscais, e.quantidade_coletas,
    STRING_AGG(r.nome, ', ') AS regioes, e.status
FROM 
    entrega AS e
INNER JOIN motorista AS m ON e.motorista_id = m.motorista_id
INNER JOIN veiculo AS v ON e.veiculo_id = v.veiculo_id
INNER JOIN entrega_regiao AS er ON e.entrega_id = er.entrega_id
INNER JOIN regiao AS r ON er.regiao_id = r.regiao_id
WHERE
    e.status = 'AGUARDANDO RETORNO'
GROUP BY
    e.numero_entrega, e.data_entrega, e.hora_saida, e.km_inicial, e.km_final,
    m.nome, v.tipo_veiculo, v.placa, e.quantidade_notas_fiscais, e.quantidade_coletas,
    e.status""")
    resultados = cur.fetchall()  # Usar fetchall() para obter todos os resultados
    
    cur.close()
    conn.close()
    
    if not resultados:
        return render_template('finalizar_entrega.html', dados=resultados)
    
    return render_template('finalizar_entrega.html', dados=resultados)

@app.route('/editar_entrega/<int:id>', methods=['GET'])
def editar_entrega(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT numero_entrega, data_entrega, km_inicial, km_final, quantidade_coletas FROM entrega WHERE numero_entrega = %s", (id,))
    entrega = cur.fetchone()
    cur.close()
    conn.close()
    
    if entrega:
        return render_template('editar_entrega.html', entrega=entrega)
    else:
        return "Entrega não encontrada", 404

@app.route('/atualizar_entrega', methods=['POST'])
def atualizar_entrega():
    numero_entrega = request.form['numero_entrega']
    km_final = request.form['km_final']
    quantidade_coletas = request.form['quantidade_coletas']
    
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE entrega
            SET km_final = %s, quantidade_coletas = %s, status = 'FINALIZADO'
            WHERE numero_entrega = %s
        """, (km_final, quantidade_coletas, numero_entrega))
        conn.commit()
    except Exception as e:
        print(f"Erro ao atualizar entrega: {str(e)}")
        return render_template('error.html', message='Ocorreu um erro ao atualizar a entrega.')
    finally:
        cur.close()
        conn.close()
    
    return redirect('/finalizar_entrega')  # Redireciona de volta para a lista de entregas

@app.route('/cadastra_combustivel', methods=['GET', 'POST'])
def cadastra_combustivel():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            # Captura os dados do formulário
            placa = request.form['placa'].upper()
            data_abastecimento = request.form['data-abastecimento']
            tipo_combustivel = request.form['tipo-combustivel'].upper()
            quantidade_combustivel = request.form['quantidade-combustivel']
            valor_abastecimento = request.form['valor-abastecido']  # Corrigido para 'valor-abastecido'

            # Verifica se o veículo já está cadastrado
            cur.execute("SELECT veiculo_id FROM veiculo WHERE placa = %s", (placa,))
            veiculo_id = cur.fetchone()

            if veiculo_id:
                veiculo_id = veiculo_id[0]  # Extraímos o valor do fetchone() corretamente

                # Faz a inserção dos dados de combustível
                cur.execute("""INSERT INTO combustivel (veiculo_id, data_abastecimento, tipo_combustivel, 
                                quantidade_combustivel, valor_abastecido) 
                            VALUES (%s, %s, %s, %s, %s)""",
                            (veiculo_id, data_abastecimento, tipo_combustivel, quantidade_combustivel, valor_abastecimento))
                conn.commit()

                return redirect(url_for('dashboard'))  # Redireciona para o dashboard após cadastro
            else:
                return jsonify({'erro': 'Veículo não encontrado no sistema. Cadastre o veículo primeiro.'})

        except Exception as e:
            conn.rollback()
            return jsonify({'erro': str(e)})
        finally:
            cur.close()
            conn.close()

    try:
        # Obtenha o próximo ID para exibir na página (sem incrementar a sequência)
        cur.execute("SELECT COALESCE(MAX(veiculo_id), 0) + 1 FROM veiculo")
        proximo_id = cur.fetchone()[0]
    except Exception as e:
        proximo_id = None
        print(f"Erro ao buscar o próximo ID: {e}")
    finally:
        cur.close()
        conn.close()

    return render_template('cadastra_combustivel.html', proximo_id=proximo_id)

# Logica de sugestõeS
@app.route('/sugestoes_placas', methods=['GET'])
def sugestoes_placas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT placa FROM veiculo ORDER BY placa")
    placas = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([placa[0] for placa in placas])

@app.route('/get-tipo-veiculo', methods=['GET'])
def get_tipo_veiculo():
    placa = request.args.get('placa')
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Consulta para obter o tipo de veículo com base na placa
    cur.execute("SELECT tipo_veiculo FROM veiculo WHERE placa = %s", (placa,))
    tipo_veiculo = cur.fetchone()
    
    cur.close()
    conn.close()
    
    # Verifica se encontrou o tipo de veículo, caso contrário retorna uma mensagem
    if tipo_veiculo:
        return jsonify(tipo_veiculo=tipo_veiculo[0])
    else:
        return jsonify({"error": "Tipo de veículo não encontrado"}), 404

@app.route('/sugestoes_motoristas', methods=['GET'])
def sugestoes_motoristas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT nome FROM motorista ORDER BY nome")
    motoristas = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([motorista[0] for motorista in motoristas])

@app.route('/sugestoes_regioes', methods=['GET'])
def sugestoes_regioes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT nome FROM regiao ORDER BY nome")
    regioes = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([regiao[0] for regiao in regioes])

# logica dos relatorio
@app.route('/menu_relatorios', methods=['GET'])
def menu_relatorios():
    return render_template('menu_relatorios.html')

@app.route('/relatorio_km_rodados', methods=['GET', 'POST'])
def relatorio_km_rodados():
    if request.method == 'GET':
        return render_template('relatorio_km_rodados.html')
    
    if request.method == 'POST':
        motorista = request.form['motorista']
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta para obter os resultados filtrados
        query = """
            SELECT TO_CHAR(e.data_entrega, 'DD/MM/YYYY') AS data_formatada,
                m.nome, v.placa, v.tipo_veiculo, SUM(e.km_rodado) AS km_rodado_total_por_data
            FROM
                entrega AS e
            INNER JOIN motorista AS m ON e.motorista_id = m.motorista_id
	        INNER JOIN veiculo AS v ON e.veiculo_id = v.veiculo_id
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
		        e.data_entrega, m.nome, v.placa,v.tipo_veiculo
	        ORDER BY
		        e.data_entrega, m.nome
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
    
@app.route('/km_rodado_entrega', methods=['GET', 'POST'])
def km_rodado_entrega():
    if request.method == 'GET':
        return render_template('km_rodado_entrega.html')
    
    if request.method == 'POST':
        motorista = request.form['motorista']
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta para obter os resultados filtrados
        query = """
            SELECT e.numero_entrega, TO_CHAR(e.data_entrega, 'DD/MM/YYYY') AS data_formatada, 
	            m.nome, v.placa, v.tipo_veiculo, MAX(e.km_rodado) AS km_rodado_maximo,
	            STRING_AGG(r.nome, ', ') AS regioes
	        FROM 
		        entrega AS e
            INNER JOIN motorista AS m ON e.motorista_id = m.motorista_id
            INNER JOIN veiculo AS v ON e.veiculo_id = v.veiculo_id
            INNER JOIN entrega_regiao AS er ON e.entrega_id = er.entrega_id
            INNER JOIN regiao AS r ON r.regiao_id = er.regiao_id
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
                e.numero_entrega, e.data_entrega, m.nome, v.placa, v.tipo_veiculo
            ORDER BY
                e.numero_entrega
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
    
@app.route('/entrega_regiao', methods=['GET', 'POST'])
def entrega_regiao():
    if request.method == 'GET':
        return render_template('entrega_regiao.html')
    
    if request.method == 'POST':
        regiao = request.form['regiao']
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta para obter os resultados filtrados
        query = """
            SELECT r.nome, COUNT(e.numero_entrega) AS total_entregas
                FROM 
                    entrega AS e
                INNER JOIN entrega_regiao AS er ON e.entrega_id = er.entrega_id
                INNER JOIN regiao AS r ON r.regiao_id = er.regiao_id
                WHERE 
                    e.status = 'FINALIZADO'
        """

        # Filtros
        conditions = []
        params = []

        if regiao:
            conditions.append("r.nome = %s")
            params.append(regiao)
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
                r.nome
            ORDER BY
                total_entregas DESC
        """

        cur.execute(query, tuple(params))
        results = cur.fetchall()

        # Consulta para calcular a soma de entregas com os mesmos filtros
        query_total_entregas = """
            SELECT COUNT(e.numero_entrega) AS total_entregas
            FROM 
                entrega AS e
            INNER JOIN entrega_regiao AS er ON e.entrega_id = er.entrega_id
            INNER JOIN regiao AS r ON r.regiao_id = er.regiao_id
            WHERE 
                e.status = 'FINALIZADO'
        """

        if conditions:
            query_total_entregas += " AND " + " AND ".join(conditions)

        cur.execute(query_total_entregas, tuple(params))
        total_entregas = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({'resultados': results, 'total_entregas': total_entregas})
    
@app.route('/entrega_motorista', methods=['GET', 'POST'])
def entrega_motorista():
    if request.method == 'GET':
        return render_template('entrega_motorista.html')
    
    if request.method == 'POST':
        motorista = request.form['motorista']
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta para obter os resultados filtrados
        query = """
            SELECT m.nome, COUNT(e.numero_entrega) AS total_entregas
            FROM 
                entrega AS e
            INNER JOIN motorista AS m ON e.motorista_id = m.motorista_id
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
                m.nome
            ORDER BY
                total_entregas DESC
        """

        cur.execute(query, tuple(params))
        results = cur.fetchall()

        # Consulta para calcular a soma de entregas com os mesmos filtros
        query_total_entregas = """
            SELECT COUNT(e.numero_entrega) AS total_entregas
            FROM 
                entrega AS e
            INNER JOIN motorista AS m ON e.motorista_id = m.motorista_id
            WHERE 
                e.status = 'FINALIZADO'
        """

        if conditions:
            query_total_entregas += " AND " + " AND ".join(conditions)

        cur.execute(query_total_entregas, tuple(params))
        total_entregas = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({'resultados': results, 'total_entregas': total_entregas})
    
@app.route('/consumo_combustivel', methods=['GET', 'POST'])
def consumo_combustivel():
    if request.method == 'GET':
        return render_template('consumo_combustivel.html')

    if request.method == 'POST':
        motorista = request.form['motorista']
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta para obter os resultados filtrados
        query = """
            WITH entregas_por_veiculo AS (
                SELECT veiculo_id, SUM(km_rodado) AS total_km
                FROM entrega
                GROUP BY veiculo_id
            ),
            combustivel_por_veiculo AS (
                SELECT veiculo_id, SUM(quantidade_combustivel) AS total_litros
                FROM combustivel
                GROUP BY veiculo_id
            )
            SELECT DISTINCT
                m.nome, 
                v.placa, 
                v.tipo_veiculo,
                e.total_km, 
                c.total_litros, 
                CASE 
                    WHEN c.total_litros = 0 THEN NULL -- Evita divisão por zero
                    ELSE e.total_km / c.total_litros 
                END AS km_por_litro
            FROM entrega AS ent
            INNER JOIN motorista AS m ON ent.motorista_id = m.motorista_id
            INNER JOIN veiculo AS v ON ent.veiculo_id = v.veiculo_id
            INNER JOIN entregas_por_veiculo e ON ent.veiculo_id = e.veiculo_id
            INNER JOIN combustivel_por_veiculo c ON ent.veiculo_id = c.veiculo_id
            WHERE ent.status = 'FINALIZADO'
        """

        # Filtros
        conditions = []
        params = []

        if motorista:
            conditions.append("m.nome = %s")
            params.append(motorista)
        if data_inicial:
            conditions.append("ent.data_entrega >= %s")
            params.append(data_inicial)
        if data_final:
            conditions.append("ent.data_entrega <= %s")
            params.append(data_final)

        # Aplicar condições extras ao WHERE existente
        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += """
            GROUP BY m.nome, v.placa, v.tipo_veiculo, e.total_km, c.total_litros
            ORDER BY km_por_litro DESC
        """

        # Executa a consulta
        cur.execute(query, tuple(params))
        results = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({'resultados': results})

if __name__ == '__main__':
    app.run(debug=True)