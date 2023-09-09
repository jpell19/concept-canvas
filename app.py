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

node_cameras = {
    'default': {
        "up":
        {
            "x": 0,
            "y": 0,
            "z": 1
        },
        "center":
        {
            "x": 0.1313509086843572,
            "y": 0.06119199042311013,
            "z": -0.08314375641775484
        },
        "eye":
        {
            "x": -0.8985090181229138,
            "y": 0.384105514336745,
            "z": -1.1990396794105627
        },
        "projection":
        {
            "type": "perspective"
        }
    },
    "amused": {
        "up":
        {
            "x": 0,
            "y": 0,
            "z": 1
        },
        "center":
        {
            "x": -0.3940549172326568,
            "y": 0.06018752905346229,
            "z": -0.313671675742228
        },
        "eye":
        {
            "x": -0.38351981181917716,
            "y": 0.05878044573319162,
            "z": 0.02253411838149233
        },
        "projection":
        {
            "type": "perspective"
        }
    }, 
    "excited": {
        "up":
        {
            "x": 0.0008145105235970864,
            "y": 0.0005703571360708373,
            "z": 0.99999950563255
        },
        "center":
        {
            "x": -0.295436951152458,
            "y": 0.16090427399203583,
            "z": -1.3663015999900467
        },
        "eye":
        {
            "x": -0.21963866518870595,
            "y": 0.11065435647239227,
            "z": 0.19001747807673386
        },
        "projection":
        {
            "type": "perspective"
        }
    }, 
    "victorious": {
        "up":
        {
            "x": 0.772011896690834,
            "y": 0.6326520895284483,
            "z": 0.061228792108852514
        },
        "center":
        {
            "x": -0.6652079099533206,
            "y": -0.0047732610039649065,
            "z": -0.030811182839873903
        },
        "eye":
        {
            "x": -0.7675280686932903,
            "y": 0.11449313793222946,
            "z": 0.026976063962971652
        },
        "projection":
        {
            "type": "perspective"
        }
    },
    "surprised": {
        "up":
        {
            "x": 0.3232441508647179,
            "y": -0.7026925886613394,
            "z": 0.633826746652564
        },
        "center":
        {
            "x": -0.1983059024971446,
            "y": 0.1661144754322101,
            "z": -0.14020980799758623
        },
        "eye":
        {
            "x": 0.5401008476211808,
            "y": -0.08415202071292369,
            "z": -0.794246699238841
        },
        "projection":
        {
            "type": "perspective"
        }
    },
    "proud": {
        "up":
        {
            "x": 0.941159810077395,
            "y": 0.21572951056859027,
            "z": -0.2601518598144529
        },
        "center":
        {
            "x": -0.35976185848021536,
            "y": -0.31491307460019147,
            "z": -0.21397111266061922
        },
        "eye":
        {
            "x": -0.5127604839460738,
            "y": 0.2672281601197627,
            "z": -0.28474175274272506
        },
        "projection":
        {
            "type": "perspective"
        }
    }, 
    "cocky": {
        "up":
        {
            "x": -0.31337938443560337,
            "y": -0.9389265832821646,
            "z": -0.14216269769824894
        },
        "center":
        {
            "x": -0.039423857439160555,
            "y": -0.2762017774688248,
            "z": -0.0262126806344331
        },
        "eye":
        {
            "x": 0.3749358749579396,
            "y": -0.25474474253851276,
            "z": -1.0813303788534938
        },
        "projection":
        {
            "type": "perspective"
        }
    }, 
    "confident": {
        "up":
        {
            "x": -0.26544819452886953,
            "y": 0.7056349990327636,
            "z": 0.6569752690637564
        },
        "center":
        {
            "x": -0.04605405415693588,
            "y": -0.08994821112298428,
            "z": -0.42222160216471527
        },
        "eye":
        {
            "x": -0.4529698507691585,
            "y": -0.7193393403158349,
            "z": 0.08937352345122107
        },
        "projection":
        {
            "type": "perspective"
        }
    }, 
    "awestruck": {
        "up":
        {
            "x": 0.6560347445129442,
            "y": 0.5363557450679761,
            "z": -0.5309811001574467
        },
        "center":
        {
            "x": -0.1855880534998064,
            "y": -0.15611857735654178,
            "z": -0.06997796770925066
        },
        "eye":
        {
            "x": -0.7392832116142083,
            "y": 0.5829576969715674,
            "z": -0.00751897589608224
        },
        "projection":
        {
            "type": "perspective"
        }
    }
}

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

word_2_idx = {node_ids[idx]: idx-1 for idx in range(1, node_count)}

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
            height=550,
            hovermode='closest',
            template=template,
            autosize=True
        )

data=[edge_trace, node_trace]

fig=go.Figure(data=data, layout=layout)

fig.update_layout(clickmode='event+select')

fig.update_traces(textposition='top left')

fig.update_layout(scene_camera=node_cameras['default'])

fig.update_traces(
    hoverinfo="none",
    hovertemplate=None,
)

app.layout = dbc.Container([
    
    dcc.Store(id='memory-store', storage_type='memory', data={'scale_factor': 0, 'word_2_idx': word_2_idx, 'node_cameras': node_cameras}),
    
    dbc.Row(
        dbc.Col(
            
            html.H1(
                    "David's gaze after defeating Goliath",
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
                xs=12, sm=12, md=12, lg=4, xl=4
            )
        ],
        align='bottom',
        justify='evenly'
    
    ),

    dbc.Row(
    
        [

            dbc.Col(
                [
                    dcc.Graph(
                        id='concept-canvas',
                        figure=fig,
                    )
                ],# width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=12, md=12, lg=7, xl=7
            ),

            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardImg(
                                src=app.get_asset_url('david.jpeg'),
                                bottom=True,
                                id='img-preview-card',
                                #style={'height':'85%', 'width':'85%'}
                            ),
                        ],
                    )
                
                ], #width={'size':5, 'offset':0, 'order':2},
                xs=12, sm=12, md=12, lg=4, xl=4,
            ),

        ], 
        align='center', 
        justify='evenly',
        className="mb-5"
    ),

    dbc.Collapse(
        dbc.Row([
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                html.P("smug", className="text-center"),
                            ),
                            dbc.CardImg(
                                src=app.get_asset_url('smug_0_proud.png'),
                                bottom=True,
                                id='from_img'
                            ),
                        ]
                    )
                ], #width={'size':5, 'offset':1},
                xs=1, sm=1, md=1, lg=1, xl=1,
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
                           html.P("smug", className="text-center", id='to_img_title'),
                        ),
                        dbc.CardImg(
                            src=app.get_asset_url('smug_0_proud.png'),
                            bottom=True,
                            id='to_img'
                        )
                    ]
                )
            ], #width={'size':5, 'offset':1},
            xs=1, sm=1, md=1, lg=1, xl=1
            )
        ], align="center", justify="evenly"), id="slider-collapse", is_open=False
    )
], fluid=True)


@app.callback(
    Output("img-preview-card", "src", allow_duplicate=True),
    Output("prompt", "children", allow_duplicate=True),
    Output('concept-canvas', 'figure', allow_duplicate=True),
    Input("concept-canvas", "hoverData"),
    State('concept-canvas', 'figure'),
    State('memory-store', 'data')
)
def display_hover(hoverData, figure, data):
    if hoverData is None:
        return no_update, no_update, no_update

    # demo only shows the first point, but other points may also be available
    hover_data = hoverData["points"][0]

    word_2_idx = data.get('word_2_idx', {})

    edge_colors = ['#555']*(len(word_2_idx)*3)

    custom_data = hover_data.get("customdata", None)

    if data.get('selected_id', None) is None and custom_data and custom_data["isNode"]:
        
        node_id = hover_data['id']

        prompt =  f'Prompt: Make his face more {node_id}'

        if node_id == 'smug':

            img_name = f'smug_0_proud.png'

            figure["data"][0]["line"]["color"] = edge_colors

        else:
            
            img_name = f'smug_100_{node_id}.png'

            word_idx = word_2_idx[node_id]

            edge_colors[word_idx*3] = '#fff'

            edge_colors[word_idx*3+1] = '#fff'
            
            figure["data"][0]["line"]["color"] = edge_colors

        return app.get_asset_url(img_name), prompt, figure
    
    else:

        return no_update, no_update, no_update

    
@app.callback(
   Output(component_id='slider-collapse', component_property='is_open', allow_duplicate=True),
   Output(component_id='selector', component_property='value'),
   Output("prompt", "children", allow_duplicate=True),
   Output(component_id='to_img', component_property='src', allow_duplicate=True),
   Output(component_id='to_img_title', component_property='children', allow_duplicate=True),
   Output("img-preview-card", "src", allow_duplicate=True),
   Output('my-slider', 'value', allow_duplicate=True),
   Output('concept-canvas', 'figure', allow_duplicate=True),
   Output('concept-canvas', 'clickData', allow_duplicate=True),
   Output('memory-store', 'data', allow_duplicate=True),
   Input('concept-canvas', 'clickData'),
   State('concept-canvas', 'figure'),
   State('memory-store', 'data'),
   prevent_initial_call=True
)
def click_node(clickData, figure, data):

    print(clickData)

    if clickData is None or clickData["points"][0].get("customdata", None) is None or not clickData["points"][0]["customdata"]["isNode"]:
         
         return False, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    point = clickData["points"][0]
    #custom_data = clickData["points"][0]["customdata"]

    data = data or {}

    word_2_idx = data.get('word_2_idx', {})

    edge_colors = ['#555']*(len(word_2_idx)*3)

    if data.get("selected_id", None) is None or point["id"] != data["selected_id"]:
       
        # Something new clicked
        node_id = point["id"]
        
        data["selected_id"] = node_id
        
        prompt =  f'Prompt: Make his face more {node_id}'

        if node_id == 'smug':
            
            img_name = f'smug_0_proud.png'

            img = app.get_asset_url(img_name)

            data['scale_factor'] = 0

            figure["data"][0]["line"]["color"] = edge_colors
            
            return False, node_id, prompt, img, node_id, img, 0, figure, no_update, data
        
        else:
            
            scale_factor = data.get('scale_factor', 100) or 100

            slider_img = app.get_asset_url( f'smug_100_{node_id}.png')
            
            preview_img = app.get_asset_url( f'smug_{scale_factor}_{node_id}.png')

            #print(f'click_update: smug_{scale_factor}_{node_id}.png')

            word_idx = word_2_idx[node_id]

            edge_colors[word_idx*3] = '#fff'

            edge_colors[word_idx*3+1] = '#fff'
            
            figure["data"][0]["line"]["color"] = edge_colors
            
            return True, node_id, prompt, slider_img, node_id, preview_img, no_update, figure, no_update, data
    else:

        # Same point clicked
        prompt =  f'Prompt: Make his face more smug'
        data["selected_id"] = None
        data['scale_factor'] = 0
        img = app.get_asset_url(f'smug_0_proud.png')

        figure["data"][0]["line"]["color"] = edge_colors

        return False, 'smug', prompt, img, 'smug', img, 0, figure, None, data
    
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
    Output('concept-canvas', 'figure', allow_duplicate=True),
    Output('memory-store', 'data', allow_duplicate=True),
    Input('selector', 'value'),
    State('concept-canvas', 'figure'),
    State('memory-store', 'data')
)
def dropdown_update(selected_word, figure, data):
    
    data = data or {}

    word_2_idx = data.get('word_2_idx', {})

    edge_colors = ['#555']*(len(word_2_idx)*3)

    if data.get("selected_id", None) is None or selected_word != data["selected_id"]:
        # Something new clicked
        data["selected_id"] = selected_word

        if selected_word == 'smug':
            
            prompt =  f'Prompt: Make his face more {selected_word}'

            img_name = f'smug_0_proud.png'

            img = app.get_asset_url(img_name)

            figure["data"][0]["line"]["color"] = edge_colors

            figure["layout"]["scene"]["camera"] = data['node_cameras']['default']
            
            return False, prompt, img, img, selected_word, 0, figure, data
        
        elif selected_word == 'david':

            prompt =  f'No Prompt: Original David Image'
            
            img_name = f'david.jpeg'

            img = app.get_asset_url(img_name)

            figure["data"][0]["line"]["color"] = edge_colors

            figure["layout"]["scene"]["camera"] = data['node_cameras']['default']
            
            return False, prompt, img, img, selected_word, 0, figure, data
    
        else:
            
            prompt =  f'Prompt: Make his face more {selected_word}'

            scale_factor = data.get('scale_factor', 100) or 100

            slider_img = app.get_asset_url( f'smug_100_{selected_word}.png')
            
            preview_img = app.get_asset_url( f'smug_{scale_factor}_{selected_word}.png')

            word_idx = word_2_idx[selected_word]

            edge_colors[word_idx*3] = '#fff'

            edge_colors[word_idx*3+1] = '#fff'

            figure["data"][0]["line"]["color"] = edge_colors

            figure["layout"]["scene"]["camera"] = data['node_cameras'][selected_word]

            return True, prompt, preview_img, slider_img, selected_word, no_update, figure, data

        
    
    else:

        # Same point clicked
        #data["selected_id"] = None
        #img = app.get_asset_url(f'smug_0_proud.png')

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
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
