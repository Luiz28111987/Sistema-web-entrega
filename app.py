from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/cadastra_motorista', methods=['GET', 'POST'])
def cadastro_motorista():
    return render_template('cadastra_motorista.html')

if __name__ == '__main__':
    app.run(debug=True)
