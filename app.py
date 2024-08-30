from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
from psycopg2 import errors

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

            # Verifica o próximo ID antes de tentar a inserção
            cur.execute("SELECT MAX(motorista_id) FROM motorista")
            ultimo_id = cur.fetchone()[0]
            if ultimo_id is None:
                ultimo_id = 0
            proximo_id = ultimo_id + 1

            # Tenta inserir os dados
            cur.execute("INSERT INTO motorista (nome) VALUES (%s)", (nome_motorista,))
            conn.commit()
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard após cadastro
        
        except errors.UniqueViolation:
            conn.rollback()
            # Verifica o próximo ID novamente em caso de erro
            cur.execute("SELECT MAX(motorista_id) FROM motorista")
            ultimo_id = cur.fetchone()[0]
            if ultimo_id is None:
                ultimo_id = 0
            proximo_id = ultimo_id + 1

            return render_template('cadastra_motorista.html', proximo_id=proximo_id, erro="Motorista já cadastrado.")
        except Exception as e:
            conn.rollback()
            return jsonify({'erro': str(e)})
        finally:
            cur.close()
            conn.close()

    try:
        cur.execute("SELECT MAX(motorista_id) FROM motorista")
        ultimo_id = cur.fetchone()[0]
        if ultimo_id is None:
            ultimo_id = 0
        proximo_id = ultimo_id + 1
    except Exception as e:
        proximo_id = None
        print(f"Erro ao buscar o último ID: {e}")
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

            # Verifica o próximo ID antes de tentar a inserção
            cur.execute("SELECT MAX(veiculo_id) FROM veiculo")
            ultimo_id = cur.fetchone()[0]
            if ultimo_id is None:
                ultimo_id = 0
            proximo_id = ultimo_id + 1

            # Tenta inserir dados
            cur.execute("INSERT INTO veiculo (tipo_veiculo, placa) VALUES (%s,%s)", (tipo_veiculo, placa))
            conn.commit()
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard após cadastro
        
        except errors.UniqueViolation:
            conn.rollback()
            # Verifica o próximo ID novamente em caso de erro
            cur.execute("SELECT MAX(veiculo_id) FROM veiculo")
            ultimo_id = cur.fetchone()[0]
            if ultimo_id is None:
                ultimo_id = 0
            proximo_id = ultimo_id + 1

            # Mensagem personalizada para duplicação de placa
            return render_template('cadastra_veiculo.html', proximo_id=proximo_id, erro="Placa já cadastrada.")        
        except Exception as e:
            conn.rollback()
            return jsonify({'erro': str(e)})
        finally:
            cur.close()
            conn.close()

    try:
        cur.execute("SELECT MAX(veiculo_id) FROM veiculo")
        ultimo_id = cur.fetchone()[0]
        if ultimo_id is None:
            ultimo_id = 0
        proximo_id = ultimo_id + 1
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

            # Verifica o próximo ID antes de tentar a inserção
            cur.execute("SELECT MAX(regiao_id) FROM regiao")
            ultimo_id = cur.fetchone()[0]
            if ultimo_id is None:
                ultimo_id = 0
            proximo_id = ultimo_id + 1

            # Tentar isnerir dados
            cur.execute("INSERT INTO regiao (nome) VALUES (%s)", (regiao,))
            conn.commit()
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard após cadastro
        
        except errors.UniqueViolation:
            conn.rollback()
            # Verifica o próximo ID novamente em caso de erro
            cur.execute("SELECT MAX(regiao_id) FROM regiao")
            ultimo_id = cur.fetchone()[0]
            if ultimo_id is None:
                ultimo_id = 0
            proximo_id = ultimo_id + 1

            return render_template('cadastra_regiao.html', proximo_id=proximo_id, erro="Regiao já cadastrada.")
        except Exception as e:
            conn.rollback()
            return jsonify({'erro': str(e)})
        finally:
            cur.close()
            conn.close()

    try:
        cur.execute("SELECT MAX(regiao_id) FROM regiao")
        ultimo_id = cur.fetchone()[0]
        if ultimo_id is None:
            ultimo_id = 0
        proximo_id = ultimo_id + 1
    except Exception as e:
        proximo_id = None
        print(f"Erro ao buscar o último ID: {e}")
    finally:
        cur.close()
        conn.close()

    return render_template('cadastra_regiao.html', proximo_id=proximo_id)

if __name__ == '__main__':
    app.run(debug=True)