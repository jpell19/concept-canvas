from dash import Dash, dcc, html, no_update, State
import dash_daq as daq
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

template = 'cyborg'
load_figure_template(template)

concepts = pd.read_csv('concepts_reduced.csv', index_col='idx')

colors = list(concepts['color'])

prompts = list(concepts['prompt'])

node_ids = list(concepts['word']) 

node_count = len(node_ids)

# Node Positions
Xn= list(concepts['x']) # x-coordinates of nodes
Yn= list(concepts['y']) # y-coordinates
Zn= list(concepts['z']) # z-coordinates

# Hub and spoke for edges - centered around concept to be tweaked
Xe = [x for i in range(1, node_count) for x in (concepts['x'][0], concepts['x'][i], None)]# x-coordinates of edge ends
#Ye = [concepts_reduced[0][1], concepts_reduced[i][1], None for i in range(1,11)]# y-coordinates of edge ends
Ye = [y for i in range(1, node_count) for y in (concepts['y'][0], concepts['y'][i], None)]
Ze = [z for i in range(1, node_count) for z in (concepts['z'][0], concepts['z'][i], None)]


edge_ids = [f'{concepts["word"][0]}_{concepts["word"][i]}' for i in range(1, node_count)]

node_flag = [{'isNode': True, 'node_id': node_ids[i]} for i in range(node_count)]

edge_flag = [{'isNode': False, 'source_idx': 0, 'target_idx': i} for i in range(1, node_count)]

slider_scale = 2.5

app = Dash(
        __name__, 
        external_stylesheets=[dbc.themes.CYBORG], 
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
        prevent_initial_callbacks="initial_duplicate"
    )   

sizes = [91] + [55]*10

edge_trace =    go.Scatter3d(x=Xe, y=Ye, z=Ze,
                    mode='lines',
                    ids=edge_ids,
                    customdata= edge_flag,
                    line=dict(color='#555', width=18),
                    hoverinfo='none'
                )

node_trace =    go.Scatter3d( x=Xn, y=Yn, z=Zn,
                    mode='markers+text',
                    name='concepts',
                    customdata= node_flag,
                    marker= dict (
                                symbol='circle',
                                size=sizes,
                                color=colors,
                                colorscale='Portland',
                                line=dict(color='#000', width=7)
                                
                            ),
                    text=node_ids,
                    ids=node_ids,
                    hoverinfo='text',
                    textposition='middle center',
                    #textfont=dict(color='#FFFFFF')
                    textfont=dict(size=18)
                )

axis=   dict(
            showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            showspikes=False,
            title=''
        )

layout = go.Layout(
            showlegend=False,
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
            ),
            height=700,
            hovermode='closest',
            template=template,
            autosize=True
        )

data=[edge_trace, node_trace]

camera = {
    "up":
        {
            "x": -0.024489069863641164,
            "y": -0.014382190213957199,
            "z": 0.9995966376803512
        },
    "center":
        {
            "x": 0.26506081515583996,
            "y": -0.3615636825121116,
            "z": 0.09348678715599934
        },
    "eye":
        {
            "x": -0.7540745830626792,
            "y": 0.5436253433931509,
            "z": -0.9218211738970644
        },
    "projection":
        {
            "type": "perspective"
        }
}

fig=go.Figure(data=data, layout=layout)

fig.update_layout(clickmode='event+select')

fig.update_traces(textposition='top left')

fig.update_layout(scene_camera=camera)

fig.update_traces(
    hoverinfo="none",
    hovertemplate=None,
)

app.layout = dbc.Container([
    
    dcc.Store(id='memory-store', storage_type='memory', data={'scale_factor': 0}),
    
    dbc.Row(
        dbc.Col(
            
            html.H1(
                    "Facial Expressions Surrounding 'Smug'",
                    className='text-center text-primary mb-4'
            ), width={"size": 8, "offset": 2}
        )
    ),

    dbc.Row(
    
        [
            dbc.Col(
                dcc.Dropdown(id='selector', multi=False, value='smug',
                                options=['david'] + node_ids
                ), #width={'size':5, 'offset':0, 'order':2},
                xs=12, sm=12, md=12, lg=7, xl=7
            ),

            dbc.Col(
                html.Div(
                    html.P(
                        children="Prompt: Make his face more smug",
                        id='prompt'
                    ), className="font-weight-bold", 
                    style={'font-size': '20px'}
                ),
                xs=12, sm=12, md=12, lg=5, xl=5
            )
        ],
        align='center',
        justify='center'
    
    ),

    dbc.Row(
    
        [

            dbc.Col(
                [
                    dcc.Graph(
                        id='concept-canvas',
                        figure=fig
                    )
                ],# width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=12, md=12, lg=7, xl=7,
                style={"height": "100%"}
            ),

            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardImg(
                                src=app.get_asset_url('david.jpeg'),
                                bottom=True,
                                id='img-preview-card'
                            ),
                        ],
                    )
                
                ], #width={'size':5, 'offset':0, 'order':2},
                xs=12, sm=12, md=12, lg=5, xl=5,
                style={"height": "100%"}
            ),

        ], 
        align='center', 
        justify='center',
        className="mb-5"
    ),

    dbc.Collapse(
        dbc.Row([
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                html.H4("Smug", className="card-title text-center"),
                            ),
                            dbc.CardImg(
                                src=app.get_asset_url('smug_0_proud.png'),
                                bottom=True,
                                id='from_img'
                            ),
                        ]
                    )
                ], #width={'size':5, 'offset':1},
                xs=2, sm=2, md=2, lg=2, xl=2,
                style={"height": "100%"}
            ),

            dbc.Col(
                [
                    dbc.Form(
                        [
                            html.Div(
                                [
                                    dbc.Label("Adjust the proportions of concepts:", html_for="range-slider"),
                                    daq.Slider(min=0, max=100, step=10,
                                        marks={0: '0%', 10: '10%', 20: '20%', 30: '30%', 40: '40%', 
                                               50: '50%', 60: '60%', 70: '70%', 80: '80%', 90: '90%', 100: '100%'},
                                        value=0.0,
                                        size=440,
                                        updatemode='drag',
                                        id='my-slider'
                                    )

                                ], id= 'slider-div', style={'transform': 'scale(2.5)', 'padding-left': '30%'}
                            )
                        ], class_name="form-control-range"
                    )
                ], #width={'size':5, 'offset':1},
                xs=8, sm=8, md=8, lg=8, xl=8,
                style={"height": "100%"}
            ),

            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody(
                           html.H4("Smug", className="card-title text-center", id='to_img_title'),
                        ),
                        dbc.CardImg(
                            src=app.get_asset_url('smug_0_proud.png'),
                            bottom=True,
                            id='to_img'
                        )
                    ]
                )
            ], #width={'size':5, 'offset':1},
            xs=2, sm=2, md=2, lg=2, xl=2
            )
        ], align="center", justify="center", className="h-auto"), id="slider-collapse", is_open=False
    )
], fluid=True)


@app.callback(
    Output("img-preview-card", "src", allow_duplicate=True),
    Output("prompt", "children", allow_duplicate=True),
    Input("concept-canvas", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return no_update, no_update

    # demo only shows the first point, but other points may also be available
    hover_data = hoverData["points"][0]

    custom_data = hover_data.get("customdata", None)

    if custom_data and custom_data["isNode"]:
        
        node_id = hover_data['id']

        prompt =  f'Prompt: Make his face more {node_id}'

        if node_id == 'smug':

            img_name = f'smug_0_proud.png'

        else:
            
            img_name = f'smug_100_{node_id}.png'

        return app.get_asset_url(img_name), prompt
    
    else:

        return no_update, no_update

    
@app.callback(
   Output(component_id='slider-collapse', component_property='is_open', allow_duplicate=True),
   Output(component_id='selector', component_property='value'),
   Output("prompt", "children", allow_duplicate=True),
   Output(component_id='to_img', component_property='src', allow_duplicate=True),
   Output(component_id='to_img_title', component_property='children', allow_duplicate=True),
   Output("img-preview-card", "src", allow_duplicate=True),
   Output('my-slider', 'value', allow_duplicate=True),
   Output('memory-store', 'data', allow_duplicate=True),
   Input('concept-canvas', 'clickData'),
   State('memory-store', 'data'),
   prevent_initial_call=True
)
def click_node(clickData, data):

    if clickData is None or clickData["points"][0].get("customdata", None) is None:
         
         return False, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    point = clickData["points"][0]
    #custom_data = clickData["points"][0]["customdata"]

    data = data or {}

    if data.get("selected_id", None) is None or point["id"] != data["selected_id"]:
       
        # Something new clicked
        node_id = point["id"]
        
        data["selected_id"] = node_id
        
        prompt =  f'Prompt: Make his face more {node_id}'

        if node_id == 'smug':
            
            img_name = f'smug_0_proud.png'

            img = app.get_asset_url(img_name)

            data['scale_factor'] = 0
            
            return False, node_id, prompt, img, node_id, img, 0, data
        
        else:
            
            scale_factor = data.get('scale_factor', 100) or 100

            slider_img = app.get_asset_url( f'smug_100_{node_id}.png')
            
            preview_img = app.get_asset_url( f'smug_{scale_factor}_{node_id}.png')

            print(f'click_update: smug_{scale_factor}_{node_id}.png')
            
            return True, node_id, prompt, slider_img, node_id, preview_img, no_update, data
    else:

        # Same point clicked
        prompt =  f'Prompt: Make his face more smug'
        data["selected_id"] = None
        data['scale_factor'] = 0
        img = app.get_asset_url(f'smug_0_proud.png')
        return False, 'smug', prompt, img, 'smug', img, 0, data
    
@app.callback(
    Output("img-preview-card", "src" , allow_duplicate=True),
    Output('memory-store', 'data', allow_duplicate=True),
    Input('my-slider', 'value'),
    State('memory-store', 'data')
)
def slider_update(value, data):
    
    if data and data.get("selected_id", None):
        # Something new clicked
        selected_word = data["selected_id"]

        if selected_word == "smug":
            img_name = f'smug_0_proud.png'
        elif selected_word == "david":
            img_name = f'david.jpeg'
        else:
            img_name = f'smug_{int(value)}_{selected_word}.png'
        
        #print(img_name)
        img = app.get_asset_url(img_name)

        data['scale_factor'] = value

        return img, data
    
    else:

        return no_update, no_update


@app.callback(
    Output(component_id='slider-collapse', component_property='is_open', allow_duplicate=True),
    Output(component_id='prompt', component_property='children', allow_duplicate=True),
    Output("img-preview-card", "src" , allow_duplicate=True),
    Output(component_id='to_img', component_property='src', allow_duplicate=True),
    Output(component_id='to_img_title', component_property='children', allow_duplicate=True),
    Output('my-slider', 'value', allow_duplicate=True),
    Output('memory-store', 'data', allow_duplicate=True),
    Input('selector', 'value'),
    State('memory-store', 'data')
)
def dropdown_update(selected_word, data):
    
    data = data or {}

    if data.get("selected_id", None) is None or selected_word != data["selected_id"]:
        # Something new clicked
        data["selected_id"] = selected_word

        if selected_word == 'smug':
            
            prompt =  f'Prompt: Make his face more {selected_word}'

            img_name = f'smug_0_proud.png'

            img = app.get_asset_url(img_name)
            
            return False, prompt, img, img, selected_word, 0, data
        
        elif selected_word == 'david':

            prompt =  f'No Prompt: Original David Image'
            
            img_name = f'david.jpeg'

            img = app.get_asset_url(img_name)
            
            return False, prompt, img, img, selected_word, 0, data
    
        else:
            
            prompt =  f'Prompt: Make his face more {selected_word}'

            scale_factor = data.get('scale_factor', 100) or 100

            slider_img = app.get_asset_url( f'smug_100_{selected_word}.png')
            
            preview_img = app.get_asset_url( f'smug_{scale_factor}_{selected_word}.png')

            print( f'dropdown-update: smug_{scale_factor}_{selected_word}.png')

            return True, prompt, preview_img, slider_img, selected_word, no_update, data

        
    
    else:

        # Same point clicked
        #data["selected_id"] = None
        #img = app.get_asset_url(f'smug_0_proud.png')

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
@app.callback(
    Output('memory-store', 'data', allow_duplicate=True),    
    Input("concept-canvas", "relayoutData"),
    State('memory-store', 'data')
)
def display_hover(relayoutData, data):
    print(relayoutData)
    data = data or {}
    data['relayout'] = relayoutData
    return data
   
if __name__ == '__main__':
    app.run_server(debug=True)
