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


    # Adicionando o HTML do botão de seleção como uma nova coluna nos dados
    for record in alcadas_data.to_dict('records'):
        record['Seleção'] = '<div class="form-check"> <input class="form-check-input" type="checkbox" value="" id="defaultCheck1"> <label class="form-check-label" for="defaultCheck1"> Checkbox padrão </label> </div>'
    
    # Adicionando a nova coluna à definição de colunas, com apresentação como markdown
    columns = [{"name": i, "id": i} for i in alcadas_data.columns] + [{"name": "Seleção", "id": "Seleção", "presentation": "markdown"}]
    
    # Agora, use a lista modificada de colunas na sua DataTable
    dash_table.DataTable(
        data=alcadas_data.to_dict('records'), 
        id='alcadas', 
        columns=columns,  # Use a lista modificada de colunas aqui
        markdown_options={"html": True},  # Permitir HTML no markdown
        # O restante da configuração da tabela permanece o mesmo
    )