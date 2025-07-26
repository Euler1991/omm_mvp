from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from PIL import Image, ImageDraw, ImageFont
import user_validation as uv

validation_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Validación", className="card-title"),
                dbc.Stack([
                    dbc.Input(placeholder="Ingresa aquí tu CURP para validarla.",
                              id='curp_input',
                              type="text"),
                    dbc.Button("Validar",
                               id='validation_button',
                               color="info",
                               n_clicks=0)],
                    gap=2)
            ]
        ),
        dbc.CardFooter(dbc.Alert(id='validation_result',
                                 color='light'))
    ]
)

download_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Descarga", className="card-title"),
                dbc.Stack([
                    html.P("Este botón se habilita al ingresar una CURP válida.",
                           className="card-text"),
                    dbc.Button("Descargar",
                               id='download_button',
                               color='success',
                               n_clicks=0)],
                    gap=2)
            ]
        ),
        dbc.CardFooter(dbc.Alert(id='download_result',
                                 color='light'))
    ]
)

cards = dbc.Row(
    [
        dbc.Col(validation_card,
                width={"size": 4, "offset": 2}),
        dbc.Col(download_card,
                width=4),
    ]
)

app = Dash(__name__,external_stylesheets=[dbc.themes.JOURNAL])
server = app.server
app.layout = html.Div([html.H1('Olimpiada Mexicana de Matemáticas',
                               style={'textAlign': 'center'}),
                       html.H2('Sistema de acceso y descarga de reconocimientos',
                               style={'textAlign': 'center'}),
                       cards,
                       dcc.Download(id='download_diploma'),
                       dcc.Store(id='name_level')
                       ])

#---------------------------------------------------------------------------------------------------

@app.callback(
    [Output("validation_result", "children"),
     Output("validation_result", "color"),
     Output("name_level", "data")],
    Input("validation_button", "n_clicks"),
    [State("curp_input",'value')]
)
def validation_click(n,curp_text):
    if n == 0:
        return '', 'light', {'nombre':'','nivel':''}
    else:
        user_validation = uv.valid_user(curp_text)
        if user_validation[0]:
            return ['La CURP {} es válida, ahora puedes descargar el reconocimiento.'.format(curp_text),
                    'info',
                    {'name':user_validation[1],
                     'level':user_validation[2],
                     'score':user_validation[3]}]
        else:
            return ['La CURP {} es inválida, revisa que los datos sean correctos.'.format(curp_text),
                    'danger',
                    {'name':user_validation[1],
                     'level':user_validation[2],
                     'score':user_validation[3]}]

@app.callback(
    Output("download_button", "disabled"),
    Input("validation_result", "color"),
    State("name_level", "data")
)
def personalize_diploma(vr, nombre_nivel_data):
    if vr != 'info':
        return True
    else:
        diploma_name = './diploma_templates/' + nombre_nivel_data['level'] + '.jpg'
        imagen = Image.open(diploma_name)
        I1 = ImageDraw.Draw(imagen)
        #myFont = ImageFont.truetype('Canterbury.ttf', 67)
        I1.text((591, 475),
                nombre_nivel_data['name'],
                #font=myFont,
                font_size=67,
                anchor='mm',
                align='center',
                fill=(0, 0, 0))
        imagen.save("./diploma_templates/Reconocimiento.jpg")
        return False

@app.callback(
    [Output("download_diploma", "data"),
     Output("download_result", "children"),
     Output("download_result", "color")],
    Input("download_button", "n_clicks"),
    State("name_level", "data")
)
def download_click(n, name_level_data):
    if n == 0:
        return None, '', 'light'
    else:
        return [dcc.send_file("./diploma_templates/Reconocimiento.jpg"),
                html.P(['Se descargó el reconocimiento del alumno {}!'.format(name_level_data['name']),
                        html.Br(),
                        'Calificación obtenida: {}'.format(name_level_data['score'])]),
                'success']

#---------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
