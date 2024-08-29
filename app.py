from flask import Flask, render_template, request, jsonify
import psycopg2

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
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/cadastrar-motorista', methods=['GET', 'POST'])
def cadastro_motorista():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            nome_motorista = request.form['motorista']
            cur.execute("INSERT INTO motorista (nome) VALUES (%s)", (nome_motorista,))
            conn.commit()
            return jsonify({'mensagem': 'Motorista cadastrado com sucesso!'})
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

if __name__ == '__main__':
    app.run(debug=True)