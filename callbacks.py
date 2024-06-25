from dash import html, Input, Output, State
from app_instance import app
from pages import pendencias_page, historico_page, ajustes_page


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return pendencias_page()
    elif pathname == '/historico':
        return historico_page()
    elif pathname == '/ajustes':
        return ajustes_page()


