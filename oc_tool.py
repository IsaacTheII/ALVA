from dash import Dash, html, dash_table, dcc, Input, Output, State, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_player as player
import os

from vis_tool.vis_app import app
from vis_tool.components.video_player import video_player
from structures.timeline_structure import Timeline

# Get the list of video files in the assets directory

VIS_TOOL_PATH = os.path.dirname(os.path.abspath(__file__))

print(VIS_TOOL_PATH)

video_files = [f for f in os.listdir("vis_tool/assets")]

timeline = Timeline()

vis_mode = "skeletal_overlay"

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
                                            options=[{"label": file, "value": file}
                                                     for file in video_files],
                                            value=video_files[0],
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
                        video_player(id="player_original", url="assets/rep_arm.mp4",
                                     height="400px", style={"padding": "10px"}),
                    ],
                        style={"width": "50%"},
                    ),
                    dbc.Card(children=[
                        html.Div(id="vis-view"),
                    ],
                        style={"width": "50%"},
                    ),
                ],
                    style={"display": "flex", "flex-direction": "row"},
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
                        html.Button("Osolate Therapist",
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
    Output("vis-view", "children"),
    Input("skeletal-overlay-button", "n_clicks"),
    Input("isolated-child-button", "n_clicks"),
    Input("isolated-therapist-button", "n_clicks"),
    Input("track-keypoints-button", "n_clicks"),
    Input("player_original", "url"),
)
def update_vis_view(skeletal_clicks, child_clicks, therapist_clicks, track_clicks, url):
    ctx = callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    vis_view = "Please select a visualization"

    if button_id == "skeletal-overlay-button":
        vis_view = video_player(
            id="player_vis_overlay", url=url, height="400px", style={"padding": "10px"})
        #sync_vis_view(current_time)
    elif button_id == "isolated-child-button":
        vis_view = html.P("Isolate Child", id="isolated-child-view")
    elif button_id == "isolated-therapist-button":
        vis_view = html.P("Isolate Therapist")
    elif button_id == "track-keypoints-button":
        vis_view = html.P("Track Keypoints")

    return vis_view


# Sync the video when switching to player_vis_overlay
""" @app.callback(
    Output("player_vis_overlay", "seekTo"),
    Input("_", "children"),
)
def sync_vis_view(current_time):
    return current_time """

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
    Input("video-dropdown", "value"),
)
def update_video(value):
    return f"assets/{value}/{value}.mp4"


if __name__ == "__main__":
    app.run_server(debug=True, port=1729)
