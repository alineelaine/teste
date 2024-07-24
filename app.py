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
def ajuste():
    df_grupoSetor = pd.read_excel('grupoSetor.xlsx', sheet_name='grupoSetor')
    df_criCra = pd.read_excel('criCra.xlsx', sheet_name='criCra')
    df_ratingsDiv = pd.read_excel('ratingsDiv.xlsx', sheet_name='ratingsDiv')
    df_limMeta = pd.read_excel('limMeta.xlsx', sheet_name='limMeta')
    grupoSetor_data = df_grupoSetor.to_dict(orient='records')
    criCra_data = df_criCra.to_dict(orient='records')
    ratingsDiv_data = df_ratingsDiv.to_dict(orient='records')
    limMeta_data = df_limMeta.to_dict(orient='records')
    grupoSetor_table = df_grupoSetor.to_html(index=False, classes='table table-striped')
    criCra_table = df_criCra.to_html(index=False, classes='table table-striped')
    ratingsDiv_table = df_ratingsDiv.to_html(index=False, classes='table table-striped')
    limMeta_table = df_limMeta.to_html(index=False, classes='table table-striped')

    return render_template('ajuste.html', df_grupoSetor=grupoSetor_data, df_criCra=criCra_data, df_ratingsDiv=ratingsDiv_data, 
                           grupoSetor_table=grupoSetor_table, criCra_table=criCra_table, ratingsDiv_table=ratingsDiv_table,
                           limMeta_table=limMeta_table, limMeta_data=limMeta_data, df_limMeta=limMeta_data)    


@app.route('/dados')
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

    # Passar ambas as tabelas para o template
    return render_template('dados.html', resumo_alcadas_table=resumo_alcadas_table, resumo_transf_table=resumo_transf_table)


if __name__ == '__main__':
    app.run(debug=True)