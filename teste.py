import pandas as pd
from dash import Dash, html, dcc, Input, Output, dash_table
from data import pendencias_data, historico_all_data, alcadas_all_data, transferencias_all_data

# Instância do aplicativo Dash
app = Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.Button('Relatório Diário', id='btn-diario'),
    html.Button('Ratings Divergentes', id='btn-ratings'),
    html.Button('Limite Meta', id='btn-meta'),
    html.Div(id='conteudo-tabela')
])

# Callback para o botão "Relatório Diário"
@app.callback(
    Output('conteudo-tabela', 'children'),
    [Input('btn-diario', 'n_clicks'),
     Input('btn-ratings', 'n_clicks'),
     Input('btn-meta', 'n_clicks')]
)
def exibir_tabela(btn_diario, btn_ratings, btn_meta):
    ctx = dash.callback_context

    if not ctx.triggered:
        aba_nome = 'diario'
    else:
        botao_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if botao_id == 'btn-diario':
            df = pendencias_data('diario')
        elif botao_id == 'btn-ratings':
            df = alcadas_all_data()
        elif botao_id == 'btn-meta':
            df = transferencias_all_data()

    return dash_table.DataTable(data=df.to_dict('records'), columns=[{'name': i, 'id': i} for i in df.columns])

# Executa o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)

def pendencias_page():
    alcadas_data, email_data, comite_data, transferencias_data = pendencias_all_data()
    # Simplifique o HTML para teste
    simple_checkbox_html = '<input type="checkbox">'
    # Adicione o HTML simplificado como uma nova coluna
    alcadas_data['Seleção'] = simple_checkbox_html
    # Atualize a definição de colunas para incluir a nova coluna com apresentação markdown
    columns = [{"name": i, "id": i} for i in alcadas_data.columns] + [{"name": "Seleção", "id": "Seleção", "presentation": "markdown"}]

    return html.Div([
        dbc.Card(dbc.CardBody([
            html.H2("Tabela Alçadas", className="text-center"),
            dash_table.DataTable(
                data=alcadas_data.to_dict('records'), 
                id='alcadas', 
                columns=columns,  # Use a lista modificada de colunas aqui
                markdown_options={"html": True},  # Permitir HTML no markdown
                style_table={
                    'height': '300px', 'overflowY': 'auto'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                    'whiteSpace': 'normal'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                fixed_rows={'headers': True},
                page_action='none',
                sort_action='native',
                filter_action='native',
                editable=True,
                column_selectable="single",
                row_selectable="multi",
                selected_columns=[],
                selected_rows=[],
                page_current= 0,
                page_size= 10,
            ), html.Button("Salvar", id="save-button", n_clicks=0, className="btn btn-primary", style={"margin-top": "20px"})
        ]), style={'marginLeft': '100px', 'marginTop': '100px'}),
    ])