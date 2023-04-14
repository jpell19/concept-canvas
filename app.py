from dash import Dash, dcc, html, no_update, State
import dash_daq as daq
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

concepts = pd.read_csv('concepts_reduced.csv', index_col='idx')

# Node Positions
Xn= list(concepts['x']) # x-coordinates of nodes
Yn= list(concepts['y']) # y-coordinates
Zn= list(concepts['z']) # z-coordinates

# Hub and spoke for edges - centered around concept to be tweaked
Xe = [x for i in range(1,11) for x in (concepts['x'][0], concepts['x'][i], None)]# x-coordinates of edge ends
#Ye = [concepts_reduced[0][1], concepts_reduced[i][1], None for i in range(1,11)]# y-coordinates of edge ends
Ye = [y for i in range(1,11) for y in (concepts['y'][0], concepts['y'][i], None)]
Ze = [z for i in range(1,11) for z in (concepts['z'][0], concepts['z'][i], None)]

colors = list(concepts['color'])

prompts = list(concepts['prompt'])

node_ids = list(concepts['word']) 

edge_ids = [f'{concepts["word"][0]}_{concepts["word"][i]}' for i in range(1,11)]

node_flag = [{'isNode': True, 'node_idx': i} for i in range(11)]

edge_flag = [{'isNode': False, 'source_idx': 0, 'target_idx': i} for i in range(1,11)]

slider_scale = 2.5

app = Dash(
        __name__, 
        external_stylesheets=[dbc.themes.CYBORG], 
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
    )   

sizes = [91] + [55]*10

edge_trace =    go.Scatter3d(x=Xe, y=Ye, z=Ze,
                    mode='lines',
                    ids=edge_ids,
                    customdata= edge_flag,
                    line=dict(color='rgb(125,125,125)', width=12),
                    hoverinfo='none'
                )

node_trace =    go.Scatter3d( x=Xn, y=Yn, z=Zn,
                    mode='markers',
                    name='concepts',
                    customdata= node_flag,
                    marker= dict (
                                symbol='circle',
                                size=sizes,
                                color=colors,
                                colorscale='Viridis',
                                line=dict(color='rgb(50,50,50)', width=5)
                            ),
                    text=prompts,
                    ids=node_ids,
                    hoverinfo='text'
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
            title="Concepts surrounding smugness",
            width=1000,
            height=1000,
            showlegend=False,
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
            ),
            margin=dict(
                t=100
            ),
            hovermode='closest',
            annotations=[
                dict(
                showarrow=False,
                    text="Hello world",
                    xref='paper',
                    yref='paper',
                    x=0,
                    y=0.1,
                    xanchor='left',
                    yanchor='bottom',
                    font=dict(
                        size=14
                    )
                )
            ],    
        )

data=[edge_trace, node_trace]
fig=go.Figure(data=data, layout=layout)

fig.update_layout(clickmode='event+select')

fig.update_traces(
    hoverinfo="none",
    hovertemplate=None,
)

app.layout = dbc.Container([

    dcc.Store(id='memory-store'),
    
    dcc.Graph(
        id='concept-canvas',
        figure=fig
    ),

    dcc.Tooltip(
        id="graph-tooltip", 
        direction='bottom'
    ),

    html.Div(id= 'slider-div',
        children=daq.Slider(min=0, max=1, step=0.2,
                marks={0: '0', .2: '20%', .4: '40%', .6: '60%', .8: '80%', 1: '100%'},
                value=0.0,
                updatemode='drag',
                id='my-slider'
        ), style={'display': 'none', 'transform': f'scale({slider_scale})', 'padding-left': '35%'}
    )
])

@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("concept-canvas", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    # demo only shows the first point, but other points may also be available
    hover_data = hoverData["points"][0]
    bbox = hover_data["bbox"]
    num = hover_data["pointNumber"]
    custom_data = hover_data.get("customdata", None)

    if custom_data and custom_data["isNode"]:
        
        #im_matrix = images[num]
        #im_url = np_image_to_base64(im_matrix)
        children = [
            html.Div([
                html.Img(
                    src=app.get_asset_url('david.jpeg'),
                    style={"width": "250px", 'display': 'block', 'margin': '0 auto'},
                ),
                html.P("Prompt: " + hover_data["text"], style={'font-weight': 'bold'})
            ])
        ]

        return True, bbox, children
    
    else:

        return False, no_update, no_update
    
@app.callback(
   Output(component_id='slider-div', component_property='style'),
   Output('memory-store', 'data'),
   Input('concept-canvas', 'clickData'),
   State('memory-store', 'data')
)
def show_hide_slider(clickData, data):

    if clickData is None or clickData["points"][0].get("customdata", None) is None:
         
         return {'display': 'none', 'transform': f'scale({slider_scale})', 'padding-left': '35%'}, no_update
    
    point = clickData["points"][0]
    #custom_data = clickData["points"][0]["customdata"]

    data = data or {}

    if data.get("last_clicked_data", None) is None or point["id"] != data["last_clicked_data"]["id"]:
        # Something new clicked
        data["last_clicked_data"] = point
        return {'display': 'block', 'transform': f'scale({slider_scale})', 'padding-left': '35%'}, data
    else:

        # Same point clicked
        data["last_clicked_data"] = None
        return {'display': 'none', 'transform': f'scale({slider_scale})', 'padding-left': '35%'}, data

   
if __name__ == '__main__':
    app.run_server(debug=True)
