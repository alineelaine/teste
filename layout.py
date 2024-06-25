from dash import html
import dash_bootstrap_components as dbc
import pandas as pd 

def load_data(sheet_name):
    return pd.read_excel('controle.xlsx', sheet_name=sheet_name)

sidebar = dbc.Nav(
    [
        html.Img(src="/assets/logo.png", height="auto", width="175px", className='nav-link'),
        dbc.NavLink("Pendências", href="/", active="exact", style={"color": "#999999"}, className='nav-link'),
        dbc.NavLink("Histórico", href="/historico", active="exact", style={"color": "#999999"}, className='nav-link'),
        dbc.NavLink("Ajustes", href="/ajustes", active="exact", style={"color": "#999999"}, className='nav-link'),
        dbc.NavLink("Controles", href="/controles", active="exact", style={"color": "#999999"}, className='nav-link'),
        dbc.NavLink("Dados", href="/dados", active="exact", style={"color": "#999999"}, className='nav-link'),
    ],
    vertical=True,
    pills=True,
    className='sidebar-wrapper'
)

content = html.Div(id="page-content")