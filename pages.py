from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from data import pendencias_all_data, historico_all_data, alcadas_all_data, transferencias_all_data
import pandas as pd


def pendencias_page():
    alcadas_data, email_data, comite_data, transferencias_data = pendencias_all_data()
    columns = [
    {"name": i, "id": i} for i in alcadas_data.columns if i != "RESPONDIDO"
] + [
    {"name": "RESPONDIDO", "id": "RESPONDIDO", "type": "text", "editable": True}
]
    columns_transf = [
    {"name": i, "id": i} for i in transferencias_data.columns if i != "RESPONDIDO"
] + [
    {"name": "RESPONDIDO", "id": "RESPONDIDO", "type": "text", "editable": True}
]
    columns_email = [
    {"name": i, "id": i} for i in email_data.columns if i != "CADASTRADO"
] + [
    {"name": "CADASTRADO", "id": "CADASTRADO", "type": "text", "editable": True}
]
    return html.Div([
        dbc.Row([
            dbc.Col(dbc.Card([
                html.H2("Pedidos de Alçadas:"),
                html.P(id="count1", children=str(len(alcadas_data))),
                html.Div(id="spark1")
            ], className="box box1 first-row-box"), width=2, className="mb-4 custom-margin"),
            dbc.Col(dbc.Card([
                html.H2("Aprovações E-mail:"),
                html.P(id="count2", children=str(len(email_data))),
                html.Div(id="spark2")
            ], className="box box2 first-row-box"), width=2, className="mb-4 custom-margin"),
            dbc.Col(dbc.Card([
                html.H2("Aprovações Comitê:"),
                html.P(id="count3", children=str(len(comite_data))),
                html.Div(id="spark3")
            ], className="box box3 first-row-box"), width=2, className="mb-4 custom-margin"),
            dbc.Col(dbc.Card([
                html.H2("Transferências:"),
                html.P(id="count4", children=str(len(transferencias_data))),
                html.Div(id="spark4")
            ], className="box box4 first-row-box"), width=2, className="mb-4 custom-margin"),
        ], className="row sparkboxes mt-4 mb-4"),
        dbc.Card(dbc.CardBody([
            html.H2("Tabela Alçadas", className="text-center"),
            dash_table.DataTable(
                data=alcadas_data.to_dict('records'), 
                id='alcadas', 
                columns=columns, 
                editable=True,
                style_table={
                    'margin': 'auto', 
                    'marginRight': 'auto',
                    'marginLeft': 'auto',
                    'overflowX': 'auto',
                },
                style_cell={
                    'textAlign': 'center',
                    'backgroundColor': 'white',
                    'color': 'black',
                    'border': '1px solid lightgray',
                    'border-left': 'none',
                    'border-right': 'none',
                },
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'border': '1px solid lightgray',
                    'border-left': 'none',
                    'border-right': 'none',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'white'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'white'
                    }
                ],
            ),
        html.Button("Salvar", id="save-button", className="btn btn-primary", style={"margin-left": "auto", "margin-top": "20px", "display": "block"}),
        html.Div(id='placeholder-div')  # Placeholder para mensagens de retorno
    ]), style={'marginLeft': '100px', 'marginTop': '100px'}),
        dbc.Card(dbc.CardBody([
        html.H2("Tabela Email", className="text-center"),
        dash_table.DataTable(
            data=email_data.to_dict('records'), 
            id='email', 
            columns=[
                {"name": i, "id": i, "editable": True if i in ["MESA", "CNPJ", "GRUPO"] else False} for i in email_data.columns
            ], 
            style_table={
                'margin': 'auto', 
                'marginRight': '45px',
                'overflowX': 'auto',
            },
            style_cell={
                'textAlign': 'center',
                'backgroundColor': 'white',
                'color': 'black',
                'border': '1px solid lightgray',
                'border-left': 'none',
                'border-right': 'none',
            },
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'border': '1px solid lightgray',
                'border-left': 'none',
                'border-right': 'none',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'white'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'white'
                }
            ]
        ), html.Button("Salvar", id="email-save-button", n_clicks=0, className="btn btn-primary", style={"margin-left": "auto", "margin-top": "20px", "display": "block"})
    ]), style={'marginLeft': '100px', 'marginTop': '50px'}),
        dbc.Card(dbc.CardBody([
            html.H2("Tabela Comitê", className="text-center"),
            dash_table.DataTable(
                data=comite_data.to_dict('records'), 
                id='comite', 
                columns=[
                {"name": i, "id": i, "editable": True if i in ["STATUS", "MESA", "CNPJ", "GRUPO"] else False} for i in comite_data.columns
            ], 
                style_table={
                    'margin': 'auto', 
                    'marginRight': '45px',
                    'overflowX': 'auto',
                },
                style_cell={
                    'textAlign': 'center',
                    'backgroundColor': 'white',
                    'color': 'black',
                    'border': '1px solid lightgray',
                    'border-left': 'none',
                    'border-right': 'none',
                },
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'border': '1px solid lightgray',
                    'border-left': 'none',
                    'border-right': 'none',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'white'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'white'
                    }
                ]
            ), html.Button("Salvar", id="save-button", n_clicks=0, className="btn btn-primary", style={"margin-left": "auto", "margin-top": "20px", "display": "block"})
        ]), style={'marginLeft': '100px', 'marginTop': '50px'}),
        dbc.Card(dbc.CardBody([
            html.H2("Tabela Transferências", className="text-center"),
            dash_table.DataTable(
                data=transferencias_data.to_dict('records'), 
                id='transferencias', 
                columns=columns_transf, 
                editable=True,
                style_table={
                    'margin': 'auto', 
                    'marginRight': 'auto',
                    'marginLeft': 'auto',
                    'overflowX': 'auto',
                },
                style_cell={
                    'textAlign': 'center',
                    'backgroundColor': 'white',
                    'color': 'black',
                    'border': '1px solid lightgray',
                    'border-left': 'none',
                    'border-right': 'none',
                },
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'border': '1px solid lightgray',
                    'border-left': 'none',
                    'border-right': 'none',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'white'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'white'
                    }
                ],
            ),
        html.Button("Salvar", id="transf-save-button", className="btn btn-primary", style={"margin-left": "auto", "margin-top": "20px", "display": "block"}),
        html.Div(id='transf-placeholder-div') 
    ]), style={'marginLeft': '100px', 'marginTop': '100px'})
    ])
   

def historico_page():
    historico_data = historico_all_data()
    transf_data = transferencias_all_data()
    alcadas_data = alcadas_all_data()

    return html.Div([
        dbc.Container([
            dbc.Card([
                dbc.CardBody([
                    html.H1("Histórico dos Cadastros", className="mt-5 mb-4 text-center"),
                    dash_table.DataTable(
                        id='historico',
                        columns=[
                            {"name": "Data de Aprovação", "id": "DataAprovacao", "presentation": "input"},
                            {"name": "CNPJ", "id": "CNPJ"},
                            {"name": "Emissor", "id": "Emissor"},
                            {"name": "Grupo", "id": "Grupo"},
                            {"name": "Evento", "id": "Evento"},
                            {"name": "Mesa", "id": "Mesa"},
                            {"name": "Data de Cadastro", "id": "DataCadastro"},
                            {"name": "Aprovação", "id": "Aprovacao"}
                        ],
                        data=historico_data.to_dict('records'),
                        filter_action='native',
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable="single",
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current=0,
                        page_size=10,
                        style_table={
                            'margin': 'auto', 
                            'marginRight': '45px',
                            'overflowX': 'auto',
                        },
                        style_cell={
                            'textAlign': 'center',
                            'backgroundColor': 'white',
                            'color': 'black',
                            'border': '1px solid lightgray',
                            'border-left': 'none',
                            'border-right': 'none',
                        },
                        style_cell_conditional=[
                            {'if': {'column_id': c}, 'textAlign': 'left'} for c in ['Emissor', 'Grupo', 'Evento', 'Mesa']
                        ],
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold',
                            'border': '1px solid lightgray',
                            'border-left': 'none',
                            'border-right': 'none',
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'white'
                            },
                            {
                                'if': {'row_index': 'even'},
                                'backgroundColor': 'white'
                            }
                        ]
                    )
                ])
            ])
        ], fluid=True),
        dbc.Container([
            dbc.Card([
                dbc.CardBody([
                    html.H1("Histórico Alçadas", className="mt-5 mb-4 text-center"),
                    dash_table.DataTable(
                        id='HistAlcadas',
                        columns=[
                            {"name": "DATA", "id": "DATA", "presentation": "input"},
                            {"name": "HORA", "id": "HORA"},
                            {"name": "REMETENTE", "id": "REMETENTE"},
                            {"name": "ASSUNTO", "id": "ASSUNTO"},
                            {"name": "EMISSOR", "id": "EMISSOR"},
                            {"name": "RESPONDIDO", "id": "RESPONDIDO"},
                            {"name": "RESPONDIDO EM", "id": "DataResposta"}
                        ],
                        data=alcadas_data.to_dict('records'),
                        filter_action='native',
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable="single",
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current=0,
                        page_size=10,
                        style_table={
                            'margin': 'auto', 
                            'marginRight': '45px',
                            'overflowX': 'auto',
                        },
                        style_cell={
                            'textAlign': 'center',
                            'backgroundColor': 'white',
                            'color': 'black',
                            'border': '1px solid lightgray',
                            'border-left': 'none',
                            'border-right': 'none',
                        },
                        style_cell_conditional=[
                            {'if': {'column_id': c}, 'textAlign': 'left'} for c in ['Emissor', 'Grupo', 'Evento', 'Mesa', 'ATA']
                        ],
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold',
                            'border': '1px solid lightgray',
                            'border-left': 'none',
                            'border-right': 'none',
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'white'
                            },
                            {
                                'if': {'row_index': 'even'},
                                'backgroundColor': 'white'
                            }
                        ]
                    )
                ])
            ])
        ], fluid=True),dbc.Container([
            dbc.Card([
                dbc.CardBody([
                    html.H1("Histórico Transferências", className="mt-5 mb-4 text-center"),
                    dash_table.DataTable(
                        id='HistTransf',
                        columns=[
                            {"name": "DATA", "id": "DATA", "presentation": "input"},
                            {"name": "HORA", "id": "HORA"},
                            {"name": "REMETENTE", "id": "REMETENTE"},
                            {"name": "ASSUNTO", "id": "ASSUNTO"},
                            {"name": "EMISSOR", "id": "EMISSOR"},
                            {"name": "RESPONDEU", "id": "QueRespondeu"},
                            {"name": "RESPONDIDO EM", "id": "DataResposta"}
                        ],
                        data=transf_data.to_dict('records'),
                        filter_action='native',
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable="single",
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current=0,
                        page_size=10,
                        style_table={
                            'margin': 'auto', 
                            'marginRight': '45px',
                            'overflowX': 'auto',
                        },
                        style_cell={
                            'textAlign': 'center',
                            'backgroundColor': 'white',
                            'color': 'black',
                            'border': '1px solid lightgray',
                            'border-left': 'none',
                            'border-right': 'none',
                        },
                        style_cell_conditional=[
                            {'if': {'column_id': c}, 'textAlign': 'left'} for c in ['Emissor', 'Grupo', 'Evento', 'Mesa', 'ATA']
                        ],
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold',
                            'border': '1px solid lightgray',
                            'border-left': 'none',
                            'border-right': 'none',
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'white'
                            },
                            {
                                'if': {'row_index': 'even'},
                                'backgroundColor': 'white'
                            }
                        ]
                    )
                ])
            ])
        ], fluid=True),
    ])
    

def ajustes_page():
    return html.Div([
    html.Button('Relatório Diário', id='btn-diario', className="btn", style={"background-color": "#f8f9fa", "border-color": "#6c757d", "margin-right": "10px", "margin-left": "300px", "margin-top": "50px"}),
    html.Button('Ratings Divergentes', id='btn-ratings', className="btn", style={"background-color": "#f8f9fa", "border-color": "#6c757d", "margin-right": "10px", "margin-top": "50px"}),
    html.Button('Limite Meta', id='btn-meta', className="btn", style={"background-color": "#f8f9fa", "border-color": "#6c757d", "margin-top": "50px"}),
    html.Div(id='conteudo-tabela')
])