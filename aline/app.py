from flask import Flask, render_template, jsonify, request
import pandas as pd
from pandas import DataFrame
from datetime import datetime

app = Flask(__name__)

def load_data():
    global df_alcadas, df_email, df_comite, df_transferencias
    df_alcadas = pd.read_excel('controleAlcadas.xlsx', sheet_name='alcadas')
    df_transferencias = pd.read_excel('controleTransf.xlsx', sheet_name='transferencias')
    df_email = pd.read_excel('controleEmail.xlsx', sheet_name='email')
    df_comite = pd.read_excel('controleComite.xlsx', sheet_name='comite')


@app.route('/')
def dados():
    # Dados de Alçadas
    df_historico_alcadas = pd.read_excel('historico.xlsx', sheet_name='HistAlcadas')
    df_historico_alcadas['DATA'] = pd.to_datetime(df_historico_alcadas['DATA'], format='%d/%m/%Y')
    df_historico_alcadas['DataResposta'] = pd.to_datetime(df_historico_alcadas['DataResposta'], format='%Y-%m-%d %H:%M:%S')
    df_historico_alcadas['TempoResposta'] = (df_historico_alcadas['DataResposta'] - df_historico_alcadas['DATA']).dt.days
    df_historico_alcadas['Mês'] = df_historico_alcadas['DATA'].dt.to_period('M')

    resumo_alcadas = df_historico_alcadas.groupby('Mês').agg(
        Solicitações=('DATA', 'count'),
        TempoRespostaMédio=('TempoResposta', 'mean')
    ).reset_index()

    resumo_alcadas_table = resumo_alcadas.to_html(index=False, classes='table table-striped')

    # Dados de Transferências
    df_historico_transf = pd.read_excel('historico.xlsx', sheet_name='HistTransf')
    df_historico_transf['DATA'] = pd.to_datetime(df_historico_transf['DATA'], format='%d/%m/%Y')
    df_historico_transf['DataResposta'] = pd.to_datetime(df_historico_transf['DataResposta'], format='%Y-%m-%d %H:%M:%S')
    df_historico_transf['TempoResposta'] = (df_historico_transf['DataResposta'] - df_historico_transf['DATA']).dt.days
    df_historico_transf['Mês'] = df_historico_transf['DATA'].dt.to_period('M')

    resumo_transf = df_historico_transf.groupby('Mês').agg(
        Solicitações=('DATA', 'count'),
        TempoRespostaMédio=('TempoResposta', 'mean')
    ).reset_index()

    resumo_transf_table = resumo_transf.to_html(index=False, classes='table table-striped')

    # Dados para o gráfico
    alcadas_por_tempo_resposta = df_historico_alcadas.groupby('TempoResposta').size().reset_index(name='Quantidade')

    # Passar ambas as tabelas e os dados do gráfico para o template
    return render_template('dados.html', resumo_alcadas_table=resumo_alcadas_table, resumo_transf_table=resumo_transf_table, alcadas_por_tempo_resposta=alcadas_por_tempo_resposta.to_dict(orient='list'))


if __name__ == '__main__':
    app.run(debug=True)