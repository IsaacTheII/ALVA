from dash import Dash, html, dash_table, dcc, Input, Output, State, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_player as player
import os

from vis_tool.vis_app import app
from vis_tool.components.video_player import video_player
from vis_tool.components.juxtaposition_components import render_keypoints
from structures.timeline_structure import Timeline
from structures.keypoints_structure import load_numpy_keypoints_bbox

# Get the list of video files in the assets directory

VIS_TOOL_PATH = os.path.dirname(os.path.abspath(__file__))

print(VIS_TOOL_PATH)

assets_folders = [f for f in os.listdir("vis_tool/assets")]

timeline = Timeline()

fps = 1

# load all the keypoints and bounding boxes from all assets
child = {}
therapist = {}
for folder in assets_folders:
    child_tmp, _ = load_numpy_keypoints_bbox(os.path.join("vis_tool/assets", folder, "juxtaposition"), "child")
    child_tmp[child_tmp == 0] = np.nan
    child_tmp[:, 1, :] = -child_tmp[:, 1, :]
    child[folder] = child_tmp

    therapist_tmp, _ = load_numpy_keypoints_bbox(os.path.join("vis_tool/assets", folder, "juxtaposition"), "therapist")
    therapist_tmp[therapist_tmp == 0] = np.nan
    therapist_tmp[:, 1, :] = -therapist_tmp[:, 1, :]
    therapist[folder] = therapist_tmp
    


# Create a Dash app layout
# +------------------------------------+
# | video conf     |   Vis Conf        |
# +----------------+-------------------+
# | Video          |   Visualization   |
# |                |                   |
# +----------------+-------------------+
# | VC     |   Timeline    | Vis_C     |
# +----------------+-------------------+
# Video conf: Select video
# Vis Conf: Skeletal Overlay, Isolate Child, Isolate Therapist, Track Keypoints
# Video: Original Video
# Visualization: Comparison Visualization
# VC: Video Controls
# Timeline: Timeline of the video
# Vis_C: Visualization Controls


app.layout = html.Div(
    [
        html.Div(
            [
                # Background
                html.Div( id="_",
                    style={"width": "100%", "height": "100%",
                           "background-color": "#ffffff"},
                ),
                html.H1("Observational Coding Tool", style={
                        "text-align": "center", "margin": "0px", "padding": "0px"}),
                # select video, Select visual comparison
                html.Div(children=[
                    html.Div(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div("Video Selection"),
                                        dcc.Dropdown(
                                            id="video-dropdown",
                                            options=[{"label": folder, "value": folder}
                                                     for folder in assets_folders],
                                            value=assets_folders[0],
                                        ),
                                    ],
                                    style={"width": "100%", "padding": "8px"},
                                ),
                            ],
                            className="mb-3",
                            style={"width": "80%",
                                   "padding": "0px", "margin": "0px"},
                        ),
                        style={"width": "50%",
                               "margin": "0px", "padding": "0px"},
                    ),
                    html.Div(
                        style={"width": "50%",
                               "margin": "0px", "padding": "0px"},
                        children=[
                            html.Div(
                                children=[
                                    html.Button("Skeletal Overlay",
                                                id="skeletal-overlay-button", style={"border-radius": "16px"}),
                                    html.Button("Isolate Child",
                                                id="isolated-child-button", style={"border-radius": "16px"}),
                                    html.Button("Isolate Therapist",
                                                id="isolated-therapist-button", style={"border-radius": "16px"}),
                                    html.Button("Track Keypoints",
                                                id="track-keypoints-button", style={"border-radius": "16px"}),
                                ],
                                style={
                                    "display": "flex",
                                    "flex-direction": "row",
                                    "justify-content": "space-evenly",
                                    "align-items": "center",
                                },
                            ),
                        ]
                    ),
                ],
                    style={"display": "flex", "flex-direction": "row",
                           "align-items": "center"},
                ),
                # Two main views, left is the original video, right is the comparison visualizations
                html.Div(children=[
                    dbc.Card(children=[
                        video_player(id="player_original", url="assets\Sirius_Intensiv_Spiel_1A_repetitive_0_anonymized_1_fps\Sirius_Intensiv_Spiel_1A_repetitive_0_anonymized_1_fps_ori.mp4",
                                     height="400px", style={"padding": "10px"}),
                    ],
                        style={"width": "50%"},
                    ),
                    dbc.Card(children=[
                        html.H1("Pleace select a visualization mode", id="vis-view-placeholder", style={
                                "text-align": "center", "margin": "0px", "padding-top": "100px"}),
                        html.Div(id="vis-view-overlay", hidden=True, children=[
                            video_player(id="player_vis_overlay", height="400px", style={"padding": "10px"})
                        ]),
                        html.Div(id="vis-view-isolated-child", hidden=True, children=[
                            dcc.Graph(id="graph-isolated-child",
                                      figure=go.Figure()
                                      ),
                            ]),
                        html.Div(id="vis-view-isolated-therapist", hidden=True, children=[
                            dcc.Graph(id="graph-isolated-therapist",
                                      figure=go.Figure()
                                      ),
                            ]),
                        html.Div(id="vis-view-track", hidden=True, children=[
                            html.Div("Track View"),
                            ]),
                    ],
                        style={"width": "50%"},
                    ),
                ],
                    style={"display": "flex", "flex-direction": "row"}
                ),

                # Video Controls, Timeline, Visualization Controls
                html.Div(children=[
                    html.Div(children=[
                        dcc.Slider(0.1, 2, 0.5, value=1, id="speed-slider"),
                        dcc.Slider(0, 1, 0.5, value=0.5, id="volume-slider"),
                    ],
                        style={
                        "width": "25%",
                        "height": "100px",
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "space-between",
                        "align-items": "center",
                        "flex-grow": "10",
                    },
                    ),
                    html.Div(style={"width": "50%"},
                             children=[
                                 html.P(id="current-time"),

                    ],
                    ),
                    html.Div(style={"width": "25%"},
                             children=[
                        html.Button("Skeletal Overlay",
                                    id="skeletal-button"),
                        html.Button("Isolate Child",
                                    id="child-button"),
                        html.Button("Isolate Therapist",
                                    id="therapist-button"),
                        html.Button("Track Keypoints",
                                    id="track-button"),
                    ]
                    )
                ],
                    style={"display": "flex", "flex-direction": "row",
                           "align-items": "center"},
                ),

            ],
            style={
                "display": "flex",
                "flex-direction": "column",
            },
        ),
    ]
)


@app.callback(
    Output("vis-view-placeholder", "hidden"),
    Output("vis-view-overlay", "hidden"),
    Output("vis-view-isolated-child", "hidden"),
    Output("vis-view-isolated-therapist", "hidden"),
    Output("vis-view-track", "hidden"),
    Input("skeletal-overlay-button", "n_clicks"),
    Input("isolated-child-button", "n_clicks"),
    Input("isolated-therapist-button", "n_clicks"),
    Input("track-keypoints-button", "n_clicks"),
)
def update_vis_view(_so, _ic, _it, _tk):
    ctx = callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "skeletal-overlay-button":
        return True, False, True, True, True
    elif button_id == "isolated-child-button":
        return True, True, False, True, True
    elif button_id == "isolated-therapist-button":
        return True, True, True, False, True
    elif button_id == "track-keypoints-button":
        return True, True, True, True, False
    else:
        return False, True, True, True, True
    


@app.callback(
    Output("player_vis_overlay", "playing"),
    Input("player_original", "playing"),
)
def update_vis_view(playing):
    return  playing


@app.callback(
    Output("current-time", "children"),
    Input("player_original", "currentTime"),
)
def update_current_time(current_time):
    return current_time


@app.callback(
    Output("player_original", "url"),
    Output("player_vis_overlay", "url"),
    Input("video-dropdown", "value"),
)
def update_video(value):
    print(value)
    print(f"assets/{value}/{value}_original.mp4")
    print(f"assets/{value}/superposition/{value}_openpose.mp4")
    return f"assets/{value}/{value}_original.mp4", f"assets/{value}/superposition/{value}_openpose.mp4"


@app.callback(
    Output("graph-isolated-child", "figure"),
    Input("player_original", "currentTime"),
    State("video-dropdown", "value"),
)
def update_vis_view_isolated(current_time, value_folder):
    current_time = 0 if current_time is None else current_time
    return render_keypoints(child[value_folder], int(current_time * fps))

@app.callback(
    Output("graph-isolated-therapist", "figure"),
    Input("player_original", "currentTime"),
    State("video-dropdown", "value"),
)
def update_vis_view_isolated(current_time, value_folder):
    current_time = 0 if current_time is None else current_time
    return render_keypoints(therapist[value_folder], int(current_time * fps))


if __name__ == "__main__":
    app.run_server(debug=True, port=1729)
