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
    if active_cell and active_cell['column_id'] == 'RESPONDIDO':
        row = active_cell['row']
        value = rows[row].get('RESPONDIDO', "Não Respondido")
        rows[row]['RESPONDIDO'] = "Respondido" if value != "Respondido" else "Não Respondido"
    return rows

@app.callback(
    Output('placeholder-div', 'children'),  
    [Input('save-button', 'n_clicks')],  
    [State('alcadas', 'data')]
)
def salvar_respondidos(n_clicks, rows):
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
        else:
            return "Clique no botão Salvar para atualizar."