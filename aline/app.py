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
def pendencias(): 
    load_data()
    alcadas_data = df_alcadas.to_dict('records')
    transferencias_data = df_transferencias.to_dict('records')
    email_table = df_email.to_html(index=False, classes='table table-striped')
    comite_table = df_comite.to_html(index=False, classes='table table-striped')
    transferencias_table = df_transferencias.to_html(index=False, classes='table table-striped')
    alcadas_count = len(alcadas_data)
    email_count = len(df_email)
    comite_count = len(df_comite)
    transferencias_count = len(transferencias_data)
    return render_template('pendencias.html', alcadas_data=alcadas_data, transferencias_data=transferencias_data, 
                           email_table=email_table, comite_table=comite_table, transferencias_table=transferencias_table, 
                           alcadas_count=alcadas_count, email_count=email_count, comite_count=comite_count, 
                           transferencias_count=transferencias_count)


@app.route('/update_Alcadasrespondidas', methods=['POST'])
def update_Alcadasrespondidas():
    data = request.get_json()
    if data is None:
        return({'message': 'Nenhum dado recebido'}), 400
    
    row_index = data.get('row_index')
    if row_index is None or row_index < 0 or row_index >= len(df_alcadas):
        return({'message': 'Índice de linha inválido'}), 400
    
    alcadas_data = pd.read_excel('./controleAlcadas.xlsx', sheet_name='alcadas', engine='openpyxl')
    alcadas_data.loc[row_index, 'RESPONDIDO'] = 'Respondido'if alcadas_data.loc[row_index, 'RESPONDIDO'] != 'Respondido' else 'Não Respondido'
    alcadas_data.to_excel('./controleAlcadas.xlsx', sheet_name='alcadas', index=False, engine='openpyxl')
    return jsonify({'message': 'Atualizado com sucesso'})

@app.route('/salvar_Alcadasrespondidas', methods=['POST'])
def salvar_Alcadasrespondidas():
    try:
        xls = pd.ExcelFile('controleAlcadas.xlsx')
        df_alcadas = pd.read_excel(xls, 'alcadas')

        try:
            df_histAlcadas = pd.read_excel('historico.xlsx', sheet_name='histAlcadas')
        except FileNotFoundError:
            df_histAlcadas = pd.DataFrame(columns=['DATA', 'HORA', 'REMETENTE', 'ASSUNTO', 'EMISSOR', 'DataResposta'])  
    
        mask = df_alcadas['RESPONDIDO'] == 'Respondido'
        alcadas_respondidas = df_alcadas[mask]

        if alcadas_respondidas.empty:
            return jsonify({'message': 'Nenhuma alcada respondida'}), 400
        
        alcadas_respondidas['DataResposta'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        df_histAlcadas = pd.concat([df_histAlcadas, alcadas_respondidas], ignore_index=True)
        df_alcadas = df_alcadas[~mask]

        with pd.ExcelWriter('historico.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_histAlcadas.to_excel(writer, sheet_name='histAlcadas', index=False)

        with pd.ExcelWriter('controleAlcadas.xlsx', engine='openpyxl', mode='w') as writer:
            df_alcadas.to_excel(writer, sheet_name='alcadas', index=False)
            for sheet in xls.sheet_names:
                if sheet != 'alcadas':
                    df_other_sheet = pd.read_excel(xls, sheet)
                    df_other_sheet.to_excel(writer, sheet_name=sheet, index=False)
        return jsonify({'message': 'Salvo com sucesso'})
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)