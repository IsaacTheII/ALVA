from dash import Dash, html, dash_table, dcc, Input, Output, State, callback, no_update, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_player as player
import os
import datetime

from vis_tool.vis_app import app
from vis_tool.components.video_player import video_player
from vis_tool.components.juxtaposition_components import render_keypoints, convert_keypoints_to_skeleton
from vis_tool.components.explicit_representation_components import render_tracked_keypoints
from vis_tool.components.timeline_components import render_timeline, update_abcs_coding, DURATION_IN_SECONDS
from structures.timeline_structure import Timeline
from structures.keypoints_structure import load_numpy_keypoints_bbox

from vis_tool.config.settings import VIS_TOOL_ASSETS_PATH, SCREEN_HEIGHT, abcs_code_colors, hf_color

# Get the list of video files in the assets directory



assets_folders = [f for f in os.listdir(VIS_TOOL_ASSETS_PATH)]


# load all dataframes and video info from all timelines in all assets
objects = {}
interactions = {}
abcs = {}
fps = {}
dur = {}
width = {}
height = {}
dur_sec = {}
for folder in assets_folders:
    timeline = Timeline()
    timeline.import_from_file(os.path.join(
        VIS_TOOL_ASSETS_PATH, folder, "timeline", folder + "_timeline.txt"))
    objects[folder] = timeline.get_objects()
    interactions[folder] = timeline.get_object_interactions()
    abcs[folder] = timeline.get_abcs_coding()
    fps[folder] = float(timeline.get_frame_rate())
    dur[folder] = float(timeline.get_duration())
    width[folder] = float(timeline.get_frame_width())
    height[folder] = float(timeline.get_frame_height())
    dur_sec[folder] = float(timeline.get_duration())


# convert start and end times to frames
for folder in assets_folders:
    objects[folder]["Start_Time"] = objects[folder]["Start_Time"].apply(
        lambda t: fps[folder] * sum(x * int(t) for x, t in zip([3600, 60, 1], t.split(":"))))
    objects[folder]["End_Time"] = objects[folder]["End_Time"].apply(
        lambda t: fps[folder] * sum(x * int(t) for x, t in zip([3600, 60, 1], t.split(":"))))

    interactions[folder]["Event_Time"] = interactions[folder]["Event_Time"].apply(
        lambda t: fps[folder] * sum(x * int(t) for x, t in zip([3600, 60, 1], t.split(":"))))

    abcs[folder]["Start_Time"] = abcs[folder]["Start_Time"].apply(
        lambda t: fps[folder] * sum(x * int(t) for x, t in zip([3600, 60, 1], t.split(":"))))
    abcs[folder]["End_Time"] = abcs[folder]["End_Time"].apply(
        lambda t: fps[folder] * sum(x * int(t) for x, t in zip([3600, 60, 1], t.split(":"))))


# load all the keypoints and bounding boxes from all assets
child = {}
therapist = {}
skeletal_child = {}
skeletal_therapist = {}
for folder in assets_folders:
    child_tmp, _ = load_numpy_keypoints_bbox(os.path.join(
        VIS_TOOL_ASSETS_PATH, folder, "juxtaposition"), "child")
    child_tmp[child_tmp == 0] = np.nan
    child_tmp[:, 1, :] = -child_tmp[:, 1, :]
    child[folder] = child_tmp

    therapist_tmp, _ = load_numpy_keypoints_bbox(os.path.join(
        VIS_TOOL_ASSETS_PATH, folder, "juxtaposition"), "therapist")
    therapist_tmp[therapist_tmp == 0] = np.nan
    therapist_tmp[:, 1, :] = -therapist_tmp[:, 1, :]
    therapist[folder] = therapist_tmp

for child_key, therapist_key in zip(child.keys(), therapist.keys()):
    skeletal_child[child_key] = convert_keypoints_to_skeleton(child[child_key])
    skeletal_therapist[therapist_key] = convert_keypoints_to_skeleton(therapist[therapist_key])

# because dash is a stateless framework, we need to account for all possible states of the app
# it is possible that the video-dorpdown value prop is None, dealing with this in the callbacks is costly.
# Therefore, as a workaround, we set the None "state" of the video-dropdown to the first folder in the assets folder
# this way, all inter mediate callbacks between old and new video-dropdown values have a valid value to execute
child[None] = child[assets_folders[0]]
therapist[None] = therapist[assets_folders[0]]
fps[None] = fps[assets_folders[0]]
dur[None] = dur[assets_folders[0]]
width[None] = width[assets_folders[0]]
height[None] = height[assets_folders[0]]


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
                html.H1("Observational Coding Tool", style={
                        "textAlign": "center", "margin": "0px", "padding": "0px"}),
                # select video, Select visual comparison
                html.Div(children=[
                    html.Div(
                        dbc.Card([
                            dbc.CardBody([
                                html.Div("Video Selection"),
                                dcc.Dropdown(
                                    id="video-dropdown",
                                    options=[{"label": folder, "value": folder}
                                             for folder in assets_folders],
                                    value=None,
                                ),
                            ],
                                style={"width": "100%", "padding": "0px"},
                            ),
                        ],
                            style={"width": "70%", "padding": "8px",
                                   "margin": "8px", "alignSelf": "center"},
                        ),
                        style={"width": "50%",
                               "display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center"},
                    ),
                    html.Div(
                        style={"width": "50%",
                               "margin": "0px", "padding": "0px"},
                        children=[
                            html.Div(
                                children=[
                                    html.Button("Skeletal Overlay",
                                                id="skeletal-overlay-button", style={"borderRadius": "30px", "fontSize": "25px", "padding": "5px", "margin": "5px"}),
                                    html.Button("Isolate Child",
                                                id="isolated-child-button", style={"borderRadius": "30px", "fontSize": "25px", "padding": "5px", "margin": "5px"}),
                                    html.Button("Isolate Therapist",
                                                id="isolated-therapist-button", style={"borderRadius": "30px", "fontSize": "25px", "padding": "5px", "margin": "5px"}),
                                    html.Button("Track Keypoints",
                                                id="track-keypoints-button", style={"borderRadius": "30px", "fontSize": "25px", "padding": "5px", "margin": "5px"}),
                                ],
                                style={
                                    "display": "flex",
                                    "flexDirection": "row",
                                    "justifyContent": "center",
                                    "alignItems": "center",
                                    "spacing": "10px",
                                },
                            ),
                        ]
                    ),
                ],
                    style={"display": "flex", "flexDirection": "row",
                           "alignItems": "center", "justify_content": "center"},
                ),
                # Two main views, left is the original video, right is the comparison visualizations
                html.Div(children=[
                    dbc.Card(children=[
                        html.H1("Please select a video", id="video-placeholder", hidden=False,
                                style={"textAlign": "center", "margin": "0px", "padding": "%dpx 0px"%(int(SCREEN_HEIGHT/4) - 24)}),
                        html.Div(id="video-player-visability", hidden=True, children=[
                            player.DashPlayer(id="player_original",
                                            playing=False,
                                            controls=False,
                                            intervalCurrentTime=400,
                                            width="100%",
                                            height="%dpx"%(int(SCREEN_HEIGHT/2)), 
                                            style={"padding": "10px"})
                            #video_player(id="player_original", height="%dpx"%(int(SCREEN_HEIGHT/2)), style={"padding": "10px"}), 
                        ]),
                    ],
                        style={"width": "50%", 'padding': '10px', 'margin': '5px'},
                    ),
                    dbc.Card(children=[
                        html.H1("Pleace select a visualization mode", id="vis-view-placeholder", hidden=False,
                               style={"textAlign": "center", "margin": "0px", "padding": "%dpx 0px"%(int(SCREEN_HEIGHT/4) - 24)}),
                        html.Div(id="vis-view-overlay", hidden=True, children=[
                            player.DashPlayer(id="player_vis_overlay",
                                              playing=False,
                                              controls=False,
                                              muted=True,
                                                intervalCurrentTime=1000,
                                                width="100%",
                                              height="%dpx"%(int(SCREEN_HEIGHT/2)), 
                                              style={"padding": "10px"})
                            #video_player(id="player_vis_overlay", height="%dpx"%(int(SCREEN_HEIGHT/2)), muted=True, style={
                            #             "padding": "10px"})
                        ]),
                        html.Div(id="vis-view-isolated-child", hidden=True, children=[
                            dcc.Graph(id="graph-isolated-child",
                                      figure=go.Figure()),
                        ]),
                        html.Div(id="vis-view-isolated-therapist", hidden=True, children=[
                            dcc.Graph(id="graph-isolated-therapist",
                                      figure=go.Figure()),
                        ]),
                        html.Div(id="vis-view-track", hidden=True, children=[
                            dcc.Graph(id="graph-track", figure=go.Figure()),
                        ]),
                    ],
                        style={"width": "50%", 'padding': '10px', 'margin': '5px'},
                    ),
                ],
                    style={"display": "flex", "flexDirection": "row"}
                ),

                # Video Controls, Timeline, Visualization Controls
                html.Div(children=[
                    html.Div(
                        style={"width": "25%", "padding": "0px"},
                        children=[
                            dbc.Card([
                                html.P("Main Video Controls:", style={
                                       "textAlign": "center"}),
                                html.P("Volume:", style={
                                       "textAlign": "center", "marginBottom": "0px", "paddingBottom": "0px"}),
                                dcc.Slider(
                                    id="volume-slider",
                                    min=0,
                                    max=1,
                                    value=0.5,
                                    step=0.05,
                                    updatemode="drag",
                                    marks={0: "0%", 0.5: "50%", 1: "100%"},
                                ),
                                html.P("Playback Speed:", style={
                                    "textAlign": "center", "marginBottom": "0px", "paddingBottom": "0px"}),
                                dcc.Slider(
                                    id="speed-slider",
                                    min=-3,
                                    max=3,
                                    value=0,
                                    step=None,
                                    updatemode="drag",
                                    marks={
                                        i: str(2**i) + "x" for i in range(-3, 4)},
                                ),
                                html.Div(
                                    children=[
                                        html.Button(
                                            "Play", id="play-button", style={"margin": "8px", "marginBottom": "2px", "paddingLeft": "5px", "paddingRight": "5px", "fontWeight": "bold"}),
                                        html.Button(
                                            "Pause", id="pause-button", style={"margin": "8px", "marginBottom": "2px", "fontWeight": "bold"}),
                                    ],
                                    style={
                                        "width": "100%",
                                        "display": "flex",
                                        "flexDirection": "row",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                    },
                                ),
                                dcc.Slider(
                                    id="seek-bar-slider",
                                    min=0,
                                    max=1,
                                    value=0,
                                    step=1,
                                    marks={0: str(datetime.timedelta(seconds=0)), 1: str(
                                        datetime.timedelta(seconds=60))},
                                    updatemode="drag",
                                ),
                            ],
                                style={"margin": "8px"},)
                        ],
                    ),

                    html.Div(style={"width": "50%"},
                             children=[
                                 dbc.Card([
                                     dcc.Graph(
                                         id="timeline-graph", style={"height": "200px"}, figure=go.Figure()),
                                 ],
                                     style={"margin": "8px", "padding": "5px"},
                                 ),
                                 dbc.Card([
                                     html.Div(id="abcs-controls",
                                                 children=[
                                                     html.Div([
                                                         html.Button(
                                                             "Expression of Wishes", id="ew-button", 
                                                             style={"borderRadius": "30px", "fontSize": "25px", "padding": "5px", "background": abcs_code_colors["EW"]}),
                                                         html.Button(
                                                             "Unscorable", id="un-button", 
                                                             style={"borderRadius": "30px", "fontSize": "25px", "padding": "5px 20px 5px 20px", "background": abcs_code_colors["UN"]}),
                                                     ], style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "flex-end"}),
                                                     html.Button(
                                                         "Other", id="ot-button", 
                                                         style={"borderRadius": "30px", "fontSize": "25px", "padding": "30px 5px 30px 5px", "background": abcs_code_colors["OT"]}),
                                                     html.Div([
                                                         html.Button(
                                                             "Repetitive Behaviour", id="rb-button", 
                                                             style={"borderRadius": "30px", "fontSize": "25px", "padding": "5px", "background": abcs_code_colors["RB"]}),
                                                         html.Button(
                                                             "Functional Play", id="fp-button", 
                                                             style={"borderRadius": "30px", "fontSize": "25px", "padding": "5px", "background": abcs_code_colors["FP"]}),
                                                     ], style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "flex-start"}),
                                                 ],
                                              style={"textAlign": "center", "display": "flex", "flexDirection": "row", "justifyContent": "center", "alignItems": "center", "paddingTop": "-5px"}),
                                 ],
                                     style={"margin": "8px","marginTop": "-5px", "padding": "5px"},
                                 ),
                    ],
                    ),
                    html.Div(style={"width": "25%"},
                             children=[
                                 dbc.Card([
                                     html.P("Visualization Controls:",
                                            style={"textAlign": "center"}),
                                     html.Div("Please select a visualization mode", id="control-placeholder", hidden=False,
                                              style={"textAlign": "center", "paddingBottom": "100px"}),
                                     html.Div(id="Overlay-Controls", hidden=True, children=[
                                         html.Div("Rendering skeleton on video.", style={
                                                  "textAlign": "center"}),
                                         html.Div("Synching overlay with main video.", style={
                                                  "textAlign": "center"})
                                     ],
                                         style={"width": "100%", "padding": "0px", "margin": "0px",
                                                "alignItems": "center", "paddingBottom": "100px"},
                                     ),
                                     html.Div(id="Isolate-Controls", hidden=True,
                                              children=[
                                                  html.P("Isolate Controls", style={
                                                      "textAlign": "center"}),
                                                  dcc.Checklist(
                                                      id="bool-props-isolate",
                                                      options=[
                                                          { "label": html.Div(['Right Hand'], 
                                                          style={'background': hf_color["RH"], 'fontSize': 18, 'fontWeight': 'bold', 'color': 'black', 'padding':'8px', 'borderRadius': '20px'}),
                                                            "value": "right hand",
                                                            },
                                                            { "label": html.Div(['Left Hand'], 
                                                            style={'background': hf_color["LH"], 'fontSize': 18, 'fontWeight': 'bold', 'color': 'black', 'padding':'8px', 'borderRadius': '20px'}),
                                                            "value": "left hand",
                                                            },
                                                            { "label": html.Div(['Right Foot'], 
                                                            style={'background': hf_color["RF"], 'fontSize': 18, 'fontWeight': 'bold', 'color': 'black', 'padding':'8px', 'borderRadius': '20px'}),
                                                            "value": "right foot",
                                                            },
                                                            { "label": html.Div(['Left Foot'], 
                                                            style={'background': hf_color["LF"], 'fontSize': 18, 'fontWeight': 'bold', 'color': 'black', 'padding':'8px', 'borderRadius': '20px'}),
                                                            "value": "left foot",
                                                            },
                                                      ],
                                                      value=[],
                                                      inline=True,
                                                      style={"width": "100%", "display": "flex", "flexDirection": "row",
                                                             "justifyContent": "space-evenly", "alignItems": "center", "paddingBottom": "20px",},
                                                  ),
                                              ]
                                              ),
                                     html.Div(id="Track-Controls", hidden=True,
                                              children=[
                                                  html.P("Track Controls", style={
                                                      "textAlign": "center"}),
                                                  dcc.Checklist(
                                                      id="bool-props-track",
                                                      options=[
                                                          { "label": html.Div(['Right Hand'], 
                                                          style={'background': hf_color["RH"], 'fontSize': 18, 'fontWeight': 'bold', 'color': 'black', 'padding':'8px', 'borderRadius': '20px'}),
                                                            "value": "right hand",
                                                            },
                                                            { "label": html.Div(['Left Hand'], 
                                                            style={'background': hf_color["LH"], 'fontSize': 18, 'fontWeight': 'bold', 'color': 'black', 'padding':'8px', 'borderRadius': '20px'}),
                                                            "value": "left hand",
                                                            },
                                                            { "label": html.Div(['Right Foot'], 
                                                            style={'background': hf_color["RF"], 'fontSize': 18, 'fontWeight': 'bold', 'color': 'black', 'padding':'8px', 'borderRadius': '20px'}),
                                                            "value": "right foot",
                                                            },
                                                            { "label": html.Div(['Left Foot'], 
                                                            style={'background': hf_color["LF"], 'fontSize': 18, 'fontWeight': 'bold', 'color': 'black', 'padding':'8px', 'borderRadius': '20px'}),
                                                            "value": "left foot",
                                                            },
                                                      ],
                                                      value=[],
                                                      inline=True,
                                                      style={"width": "100%", "display": "flex", "flexDirection": "row",
                                                             "justifyContent": "space-evenly", "alignItems": "center", "paddingBottom": "20px"},
                                                  ),
                                              ],
                                              style={"width": "100%", "display": "flex", "flexDirection": "column",
                                                     "justifyContent": "flex-start", "alignItems": "center",},
                                              ),
                                 ],
                                     style={ "display": "flex",
                                            "flexDirection": "column", "margin": "8px", "padding": "5px"},
                                 ),
                    ]
                    )
                ],
                    style={"display": "flex", "flexDirection": "row",
                           "alignItems": "flex-start"},
                ),

            ],
            style={
                "display": "flex",
                "flexDirection": "column",
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
    Output("control-placeholder", "hidden"),
    Output("Overlay-Controls", "hidden"),
    Output("Isolate-Controls", "hidden"),
    Output("Track-Controls", "hidden"),
    Input("skeletal-overlay-button", "n_clicks"),
    Input("isolated-child-button", "n_clicks"),
    Input("isolated-therapist-button", "n_clicks"),
    Input("track-keypoints-button", "n_clicks"),
)
def update_vis_view(_so, _ic, _it, _tk):
    ctx = callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "skeletal-overlay-button":
        return True, False, True, True, True, True, False, True, True
    elif button_id == "isolated-child-button":
        return True, True, False, True, True, True, True, False, True
    elif button_id == "isolated-therapist-button":
        return True, True, True, False, True, True, True, False, True
    elif button_id == "track-keypoints-button":
        return True, True, True, True, False, True, True, True, False
    else:
        return False, True, True, True, True, False, True, True, True


@app.callback(
    Output("player_original", "url"),
    Output("player_vis_overlay", "url"),
    Output("video-placeholder", "hidden"),
    Output("video-player-visability", "hidden"),
    Input("video-dropdown", "value"),
)
def update_video(value):
    if value is None:
        return no_update, no_update, False, True
    ori_vid = f"assets/video_assets/{value}/{value}_original.mp4"
    vis_vid = f"assets/video_assets/{value}/superposition/{value}_openpose.mp4"
    return ori_vid, vis_vid, True, False


@app.callback(
    Output("graph-isolated-child", "figure"),
    Input("player_original", "currentTime"),
    Input("bool-props-isolate", "value"),
    State("video-dropdown", "value"),
    State("graph-isolated-child", "figure"),
    State("vis-view-isolated-child", "hidden"),
)
def update_vis_view_isolated(current_time, val_list, value_folder, fig, hidden):
    if hidden:
        return no_update
    #print(fig['data'])
    current_time = 0 if current_time is None else current_time
    return render_keypoints(skeletal_child[value_folder], 
                            "right hand" in val_list, 
                            "left hand" in val_list, 
                            "right foot" in val_list, 
                            "left foot" in val_list,
                            int(current_time * fps[value_folder]) - 1, 
                            width[value_folder], height[value_folder], 
                            int(SCREEN_HEIGHT/2))


@app.callback(
    Output("graph-isolated-therapist", "figure"),
    Input("player_original", "currentTime"),
    Input("bool-props-isolate", "value"),
    State("video-dropdown", "value"),
    State("vis-view-isolated-therapist", "hidden"),
)
def update_vis_view_isolated(current_time, val_list, value_folder, hidden):
    if hidden:
        return no_update
    current_time = 0 if current_time is None else current_time
    return render_keypoints(skeletal_therapist[value_folder], 
                            "right hand" in val_list, 
                            "left hand" in val_list, 
                            "right foot" in val_list, 
                            "left foot" in val_list,
                            int(current_time * fps[value_folder]) - 1, 
                            width[value_folder], height[value_folder], 
                            int(SCREEN_HEIGHT/2))


@app.callback(
    Output("graph-track", "figure"),
    Input("player_original", "currentTime"),
    Input("bool-props-track", "value"),
    State("video-dropdown", "value"),
    State("vis-view-track", "hidden"),
)
def update_vis_view_isolated(current_time, val_list, value_folder, hidden):
    if hidden:
        return no_update
    track_dict = {"RH": "right hand" in val_list, "LH": "left hand" in val_list,
                  "RF": "right foot" in val_list, "LF": "left foot" in val_list}
    duration = int(10 * fps[value_folder])
    current_time = 0 if current_time is None else current_time
    return render_tracked_keypoints(
        child[value_folder], 
        track_dict, 
        duration, int(current_time * fps[value_folder]) - 1, 
        width[value_folder],
        height[value_folder],
        int(SCREEN_HEIGHT/2))

"""
@app.callback(
    Output("timeline-graph", "figure"),
    Input("player_original", "currentTime"),
    Input("video-dropdown", "value"),
)
def update_timeline(current_time, value_folder):
    if current_time is None or value_folder is None:
        return no_update
    return render_timeline(objects[value_folder], interactions[value_folder], abcs[value_folder], dur_sec[value_folder], fps[value_folder], int(current_time * fps[value_folder]))
"""

@app.callback(
    Output("player_original", "volume"),
    Input("volume-slider", "value"),
)
def update_volume(volume):
    return volume


@app.callback(
    Output("player_original", "playbackRate"),
    Output("player_vis_overlay", "playbackRate"),
    Input("speed-slider", "value"),
)
def update_speed(speed):
    speed = 2**speed
    return speed, speed


@app.callback(
    Output("player_original", "playing"),
    Output("player_vis_overlay", "playing"),
    Output("play-button", "n_clicks"),
    Input("play-button", "n_clicks"),
    Input("pause-button", "n_clicks"),
    Input("video-dropdown", "value"),
)
def update_play(play, pause, value):
    ctx = callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "play-button":
        if play % 2 == 1:
            return True, True, play
        else:
            return False, False, play
    elif button_id == "pause-button":
        if play % 2 == 0:
            return False, False, play
        return False, False, play + 1
    elif button_id == "dropdown":
        return False, False, play
    else:
        return False, False, play


@app.callback(
    Output("player_original", "seekTo"),
    Output("player_vis_overlay", "seekTo"),
    Output("seek-bar-slider", "max"),
    Output("seek-bar-slider", "marks"),
    Output("seek-bar-slider", "value"),
    Input("seek-bar-slider", "drag_value"),
    Input("player_original", "currentTime"),
    State("video-dropdown", "value")
)
def update_seek_bar(drag_value, current_time, folder_value):
    duration = int(dur[folder_value]) if dur[folder_value] is not None else 1
    value = int(drag_value) if drag_value is not None else 0
    ctx = callback_context
    input_trigger = ctx.triggered[0]["prop_id"]
    if input_trigger == "seek-bar-slider.value":
        # marks = {0: str(datetime.timedelta(seconds=0)), value: str(datetime.timedelta(seconds=value)), duration: str(datetime.timedelta(seconds=duration))}
        marks = {value: str(datetime.timedelta(seconds=value))}
        return value, value, duration, marks, no_update
    elif input_trigger == "seek-bar-slider.drag_value":
        # marks = {0: str(datetime.timedelta(seconds=0)), drag_value: str(datetime.timedelta(seconds=drag_value)), duration: str(datetime.timedelta(seconds=duration))}
        marks = {drag_value: str(datetime.timedelta(seconds=drag_value))}
        return drag_value, drag_value, duration, marks, no_update
    elif input_trigger == "player_original.duration":
        marks = {0: str(datetime.timedelta(seconds=0)), duration: str(
            datetime.timedelta(seconds=duration))}
        return value, value, duration, marks, no_update
    elif input_trigger == "player_original.currentTime":
        value = int(current_time) if current_time is not None else 0
        marks = {value: str(datetime.timedelta(seconds=value))}
        return no_update, no_update, duration, marks, value
    else:
        marks = {0: str(datetime.timedelta(seconds=0)), duration: str(
            datetime.timedelta(seconds=duration))}
        return no_update, no_update, duration, marks, current_time if current_time is not None else 0


@app.callback(
    Output("timeline-graph", "figure", allow_duplicate=True),
    Input("ew-button", "n_clicks"),
    Input("un-button", "n_clicks"),
    Input("ot-button", "n_clicks"),
    Input("rb-button", "n_clicks"),
    Input("fp-button", "n_clicks"),
    Input("video-dropdown", "value"),
    State("player_original", "currentTime"),
    State("timeline-graph", "figure"),
    prevent_initial_call='initial_duplicate'
)
def update_coding(_ew, _un, _ot, _rb, _fp, value_folder, current_time, fig):
    if current_time is None:
        current_time = 0
    if value_folder is None:
        return no_update
    ctx = callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "ew-button":
        update_abcs_coding(abcs[value_folder], int(current_time * fps[value_folder]) - 1, "EW")
    elif button_id == "un-button":
        update_abcs_coding(abcs[value_folder], int(current_time * fps[value_folder]) - 1, "UN")
    elif button_id == "ot-button":
        update_abcs_coding(abcs[value_folder], int(current_time * fps[value_folder]) - 1, "OT")
    elif button_id == "rb-button":
        update_abcs_coding(abcs[value_folder], int(current_time * fps[value_folder]) - 1, "RB")
    elif button_id == "fp-button":
        update_abcs_coding(abcs[value_folder], int(current_time * fps[value_folder]) - 1, "FP")
    elif button_id == "video-dropdown":
        pass
    else:
        return no_update
    return render_timeline(objects[value_folder], interactions[value_folder], abcs[value_folder], dur_sec[value_folder], fps[value_folder], (current_time) * fps[value_folder])


@app.callback(
    Output("timeline-graph", "figure", allow_duplicate=True),
    Input("video-dropdown", "value"),
    Input("player_original", "currentTime"),
    State("timeline-graph", "figure"),
    prevent_initial_call='initial_duplicate'
)
def update_timeline(value_folder, current_time, fig):
    if current_time is None or value_folder is None:
        return no_update
    fig['layout']['xaxis']['range'] = [int(current_time * fps[value_folder]) - DURATION_IN_SECONDS * fps[value_folder] * .5,
                                        int(current_time * fps[value_folder]) + DURATION_IN_SECONDS * fps[value_folder] * .5]
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=1729)
    #app.run_server(debug=True, port=8050)

