import pandas as pd

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



