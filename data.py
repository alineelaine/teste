import pandas as pd
from datetime import datetime


# Funções de formatação de colunas
def format_date_columns(data, date_columns):
    for column in date_columns:
        if column in data.columns:
            data[column] = pd.to_datetime(data[column], errors='coerce').dt.strftime('%d/%m/%Y')
    return data

def format_time_columns(data, time_columns, time_format=None):
    for column in time_columns:
        if column in data.columns:
            data[column] = pd.to_datetime(data[column], format=time_format, errors='coerce').dt.strftime('%H:%M')
    return data

# Função para ler e processar dados de pendências
def pendencias_data(sheet_name, date_columns=None, time_columns=None, time_format=None):
    file_path = './controle.xlsx'
    data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    
    if date_columns is None:
        date_columns = ['DATA']
    if time_columns is None:
        time_columns = []
    
    data = format_date_columns(data, date_columns)
    data = format_time_columns(data, time_columns, time_format)
    
    return data

# Função para consolidar todos os dados de pendências
def pendencias_all_data():
    alcadas_data = pendencias_data('alcadas', date_columns=['DATA'], time_columns=['HORA'], time_format='%H:%M:%S')
    email_data = pendencias_data('email', date_columns=['DATA'])
    comite_data = pendencias_data('comite', date_columns=['DATA'])
    transferencias_data = pendencias_data('transferencias', date_columns=['DATA'])
    
    return alcadas_data, email_data, comite_data, transferencias_data

# Função para ler e processar o histórico completo
def historico_all_data():
    file_path = './historico.xlsx'
    historico_data = pd.read_excel(file_path, sheet_name='historico', engine='openpyxl')
    date_columns = ['DataAprovacao', 'DataCadastro']
    historico_data = format_date_columns(historico_data, date_columns)
    
    return historico_data

# Função para ler e processar todos os dados de alcadas
def alcadas_all_data():
    file_path = './historico.xlsx'
    alcadas_data = pd.read_excel(file_path, sheet_name='HistAlcadas', engine='openpyxl')
    date_columns = ['DATA', 'DataResposta']
    alcadas_data = format_date_columns(alcadas_data, date_columns)
    
    return alcadas_data

# Função para ler e processar todos os dados de transferências
def transferencias_all_data():
    file_path = './historico.xlsx'
    transf_data = pd.read_excel(file_path, sheet_name='HistTransf', engine='openpyxl')
    date_columns = ['DATA', 'DataResposta']
    transf_data = format_date_columns(transf_data, date_columns)
    
    return transf_data


def toggle_respondido(active_cell, rows):
    if active_cell and active_cell['column_id'] == 'RESPONDIDO':
        row = active_cell['row']
        value = rows[row].get('RESPONDIDO', "Não Respondido")
        rows[row]['RESPONDIDO'] = "Respondido" if value != "Respondido" else "Não Respondido"
    return rows

def salvar_respondidos_excel(n_clicks, rows):
    n_clicks = 1 if n_clicks == 0 else n_clicks
    if n_clicks and n_clicks > 0:
        respondidos = [row for row in rows if row.get('RESPONDIDO') == "Respondido"]
        if respondidos:
            caminho_controle = 'controle.xlsx'
            caminho_historico = 'historico.xlsx'
            try:
                controle_df = pd.read_excel(caminho_controle, sheet_name='alcadas')
                controle_df = controle_df[~controle_df.index.isin([rows.index(row) for row in respondidos])]
                with pd.ExcelWriter(caminho_controle, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    controle_df.to_excel(writer, sheet_name='alcadas', index=False)
                try:
                    historico_df = pd.read_excel(caminho_historico, sheet_name='HistAlcadas')
                except FileNotFoundError:
                    historico_df = pd.DataFrame()
                for row in respondidos:
                    row['DataResposta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                historico_df = pd.concat([historico_df, pd.DataFrame(respondidos)])
                with pd.ExcelWriter(caminho_historico, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    historico_df.to_excel(writer, sheet_name='HistAlcadas', index=False)

            except FileNotFoundError as e:
                return f"Arquivo não encontrado: {e.filename}"
            return "Dados salvos com sucesso!"


def update_transf_respondido(active_cell, rows):
    if active_cell and active_cell['column_id'] == 'RESPONDIDO':
        row = active_cell['row']
        value = rows[row].get('RESPONDIDO', "Não Respondido")
        rows[row]['RESPONDIDO'] = "Respondido" if value != "Respondido" else "Não Respondido"
    return rows


def salvar_transf_respondidos_excel(n_clicks, rows):
    n_clicks = 1 if n_clicks == 0 else n_clicks
    if n_clicks and n_clicks > 0:
        respondidos = [row for row in rows if row.get('RESPONDIDO') == "Respondido"]
        if respondidos:
            caminho_controle = 'controle.xlsx'
            caminho_historico = 'historico.xlsx'
            try:
                controle_df = pd.read_excel(caminho_controle, sheet_name='transferencias')
                controle_df = controle_df[~controle_df.index.isin([rows.index(row) for row in respondidos])]
                with pd.ExcelWriter(caminho_controle, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    controle_df.to_excel(writer, sheet_name='transferencias', index=False)
                try:
                    historico_df = pd.read_excel(caminho_historico, sheet_name='HistTransf')
                except FileNotFoundError:
                    historico_df = pd.DataFrame()
                for row in respondidos:
                    row['DataResposta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                historico_df = pd.concat([historico_df, pd.DataFrame(respondidos)])
                with pd.ExcelWriter(caminho_historico, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    historico_df.to_excel(writer, sheet_name='HistTransf', index=False)

            except FileNotFoundError as e:
                return f"Arquivo não encontrado: {e.filename}"
            return "Dados salvos com sucesso!"
        else:
            return "Nenhum dado para salvar"