import os
import pandas as pd
from datetime import datetime
from dash import html, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from app_instance import app
from pages import pendencias_page, historico_page, ajustes_page
from app import app

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return pendencias_page()
    elif pathname == '/historico':
        return historico_page()
    elif pathname == '/ajustes':
        return ajustes_page()

@app.callback(
    Output('alcadas', 'data'),
    [Input('alcadas', 'active_cell')],
    [State('alcadas', 'data')]
)
def update_respondido(active_cell, rows):
    print("Callback update_respondido chamado.")  # Log de impressão adicionado
    if active_cell and active_cell['column_id'] == 'RESPONDIDO':
        row = active_cell['row']
        value = rows[row]['RESPONDIDO']
        rows[row]['RESPONDIDO'] = "Respondido" if value != "Respondido" else "Não Respondido"
    return rows

@app.callback(
    Output('placeholder-div', 'children'),  
    [Input('save-button', 'n_clicks')],  # Certifique-se de que o ID do botão salvar seja único
    [State('alcadas', 'data')]
)
def salvar_respondidos(n_clicks, rows):
    if n_clicks and n_clicks > 0:
        respondidos = [row for row in rows if row.get('RESPONDIDO') == "Respondido"]
        if respondidos:
            caminho_historico = 'historico.xlsx'
            try:
                historico_df = pd.read_excel(caminho_historico, sheet_name='HistAlcadas')
            except FileNotFoundError:
                historico_df = pd.DataFrame()

            for row in respondidos:
                row['DataResposta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            novo_historico_df = pd.concat([historico_df, pd.DataFrame(respondidos)])
            with pd.ExcelWriter(caminho_historico, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                novo_historico_df.to_excel(writer, sheet_name='HistAlcadas', index=False)

            caminho_controle = 'controle.xlsx'
            controle_df = pd.read_excel(caminho_controle)
            controle_df = controle_df[~controle_df['ID'].isin([row['ID'] for row in respondidos])]
            controle_df.to_excel(caminho_controle, index=False)

            return "Dados salvos com sucesso!"
        else:
            return "Nenhuma alteração para salvar."
    return "Clique no botão Salvar para atualizar."
    