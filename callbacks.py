import pandas as pd
from datetime import datetime
from dash import html, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from app_instance import app
from pages import pendencias_page, historico_page, ajustes_page
from app import app
from data import toggle_respondido, salvar_respondidos_excel, update_transf_respondido, salvar_transf_respondidos_excel, update_email_cadastrado, salvar_email_cadastrados_excel

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


@app.callback(
    Output('transferencias', 'data'),
    [Input('transferencias', 'active_cell')],
    [State('transferencias', 'data')]
)
def update_transf_respondido_callback(active_cell, rows):
  
    return update_transf_respondido(active_cell, rows)


@app.callback(
    Output('transf-placeholder-div', 'children'),
    [Input('transf-save-button', 'n_clicks')],  
    [State('transferencias', 'data')]
)
def salvar_transf_respondidos_callback(n_clicks, rows):
    
    return salvar_transf_respondidos_excel(n_clicks, rows)


@app.callback(
    Output('email', 'data'),
    [Input('email', 'active_cell')],
    [State('email', 'data')]
)
def update_email_cadastrado_callback(active_cell, rows):
  
    return update_email_cadastrado(active_cell, rows)


@app.callback(
    Output('email-placeholder-div', 'children'),
    [Input('email-save-button', 'n_clicks')],  
    [State('email', 'data')]
)
def salvar_email_cadastrados_callback(n_clicks, rows):
    
    return salvar_email_cadastrados_excel(n_clicks, rows)
