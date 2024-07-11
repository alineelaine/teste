from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    alcadas = pd.read_excel('controle.xlsx', sheet_name='alcadas').to_html(index=False)
    email = pd.read_excel('controle.xlsx', sheet_name='email').to_html(index=False)
    comite = pd.read_excel('controle.xlsx', sheet_name='comite').to_html(index=False)
    ficticios = pd.read_excel('controle.xlsx', sheet_name='ficticios').to_html(index=False)
    ajustes = pd.read_excel('controle.xlsx', sheet_name='ajustes').to_html(index=False)

    return render_template('index.html', alcadas=alcadas, email=email, comite=comite, ficticios=ficticios, ajustes=ajustes)
@app.route('/pagina1')
def pagina1():
    return render_template('pagina1.html')

@app.route('/pagina2')
def pagina2():
    return render_template('pagina2.html')

@app.route('/pagina3')
def pagina3():
    return render_template('pagina3.html')

if __name__ == '__main__':
    app.run(debug=True)