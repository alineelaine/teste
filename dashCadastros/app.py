from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def pendencias():
	df_alcadas = pd.read_excel('controle.xlsx', sheet_name='alcadas')
	alcadas_table = df_alcadas.to_html(index=False, classes='table table-striped')
	return render_template('pendencias.html', html_table=alcadas_table)


if __name__ == '__main__':
	app.run(debug=True)