from dash import dcc, html
from app_instance import app
from layout import sidebar, content 
import callbacks


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([sidebar, content], style={'display': 'flex'})
])

if __name__ == '__main__':
    app.run_server(debug=True)