from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

app = Dash(__name__,external_stylesheets=[dbc.themes.JOURNAL])
server = app.server
app.layout = html.Div([html.H1('Olimpiada Mexicana de Matemáticas',
                               style={'textAlign': 'center'}),
                       html.H2('Sistema de acceso y descarga de reconocimientos',
                               style={'textAlign': 'center'}),
                       dcc.Download(id='download_diploma'),
                       dcc.Store(id='name_level')
                       ])

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
