import pandas as pd
from datetime import datetime
from dash import html, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from app_instance import app
from pages import pendencias_page, historico_page, ajustes_page
from app import app
from data import toggle_respondido, salvar_respondidos_excel, update_transf_respondido, salvar_transf_respondidos_excel

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
    return toggle_respondido(active_cell, rows)

@app.callback(
    Output('placeholder-div', 'children'),  
    [Input('save-button', 'n_clicks')],  
    [State('alcadas', 'data')]
)
def salvar_respondidos(n_clicks, rows):
    return salvar_respondidos_excel(n_clicks, rows)

# Definição do callback para atualizar as transferências respondidas
@app.callback(
    Output('transferencias', 'data'),
    [Input('transferencias', 'active_cell')],
    [State('transferencias', 'data')]
)
def update_transf_respondido_callback(active_cell, rows):
    # Chama a função importada de data.py
    return update_transf_respondido(active_cell, rows)

# Definição do callback para salvar as transferências respondidas
@app.callback(
    Output('transf-placeholder-div', 'children'),
    [Input('transf-save-button', 'n_clicks')],  
    [State('transferencias', 'data')]
)
def salvar_transf_respondidos_callback(n_clicks, rows):
    # Chama a função importada de data.py
    return salvar_transf_respondidos_excel(n_clicks, rows)
