from flask import Flask, render_template, jsonify, request
import pandas as pd
from pandas import DataFrame
from datetime import datetime

app = Flask(__name__)


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

    return render_template('dados.html', resumo_alcadas_table=resumo_alcadas_table, resumo_transf_table=resumo_transf_table)

@app.route('/dados_grafico')
def dados_grafico():
    df_historico_alcadas = pd.read_excel('historico.xlsx', sheet_name='HistAlcadas')
    df_historico_alcadas['DATA'] = pd.to_datetime(df_historico_alcadas['DATA'], format='%d/%m/%Y')
    df_historico_alcadas['Mês'] = df_historico_alcadas['DATA'].dt.to_period('M')

    resumo_alcadas = df_historico_alcadas.groupby('Mês').agg(
        Solicitações=('DATA', 'count')
    ).reset_index()

    dados = {
        'meses': resumo_alcadas['Mês'].astype(str).tolist(),
        'solicitacoes': resumo_alcadas['Solicitações'].tolist()
    }

    return jsonify(dados)

@app.route('/dados_grafico_transf')
def dados_grafico_transf():
    df_historico_transf = pd.read_excel('historico.xlsx', sheet_name='HistTransf')
    df_historico_transf['DATA'] = pd.to_datetime(df_historico_transf['DATA'], format='%d/%m/%Y')
    df_historico_transf['Mês'] = df_historico_transf['DATA'].dt.to_period('M')

    resumo_transf = df_historico_transf.groupby('Mês').agg(
        Solicitações=('DATA', 'count')
    ).reset_index()

    dados = {
        'meses': resumo_transf['Mês'].astype(str).tolist(),
        'solicitacoes': resumo_transf['Solicitações'].tolist()
    }

    return jsonify(dados)


if __name__ == '__main__':
    app.run(debug=True)