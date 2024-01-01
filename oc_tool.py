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
from vis_tool.components.juxtaposition_components import render_keypoints
from vis_tool.components.explicit_representation_components import render_tracked_keypoints
from vis_tool.components.timeline_components import render_timeline
from structures.timeline_structure import Timeline
from structures.keypoints_structure import load_numpy_keypoints_bbox

# Get the list of video files in the assets directory

VIS_TOOL_PATH = os.path.dirname(os.path.abspath(__file__))

print(VIS_TOOL_PATH)

assets_folders = [f for f in os.listdir("vis_tool/assets")]


# load all dataframes and video info from all timelines in all assets
objects = {}
interactions = {}
abcs = {}
fps = {}
dur_sec = {}
for folder in assets_folders:
    timeline = Timeline()
    timeline.import_from_file(os.path.join(
        "vis_tool/assets", folder, "timeline", folder + "_timeline.txt"))
    objects[folder] = timeline.get_objects()
    interactions[folder] = timeline.get_object_interactions()
    abcs[folder] = timeline.get_abcs_coding()
    fps[folder] = float(timeline.get_frame_rate())
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
for folder in assets_folders:
    child_tmp, _ = load_numpy_keypoints_bbox(os.path.join(
        "vis_tool/assets", folder, "juxtaposition"), "child")
    child_tmp[child_tmp == 0] = np.nan
    child_tmp[:, 1, :] = -child_tmp[:, 1, :]
    child[folder] = child_tmp

    therapist_tmp, _ = load_numpy_keypoints_bbox(os.path.join(
        "vis_tool/assets", folder, "juxtaposition"), "therapist")
    therapist_tmp[therapist_tmp == 0] = np.nan
    therapist_tmp[:, 1, :] = -therapist_tmp[:, 1, :]
    therapist[folder] = therapist_tmp

# because dash is a stateless framework, we need to account for all possible states of the app
# it is possible that the video-dorpdown value prop is None, dealing with this in the callbacks is costly.
# Therefore, as a workaround, we set the None "state" of the video-dropdown to the first folder in the assets folder
# this way, all inter mediate callbacks between old and new video-dropdown values have a valid value to execute
child[None] = child[assets_folders[0]]
therapist[None] = therapist[assets_folders[0]]
fps[None] = fps[assets_folders[0]]


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

SCREEN_HEIGHT = 1080    # ajust big or small depending of the avalable vertical screen space


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Observational Coding Tool", style={
                        "text-align": "center", "margin": "0px", "padding": "0px"}),
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
                                   "margin": "8px", "align-self": "center"},
                        ),
                        style={"width": "50%",
                               "display": "flex", "flex-direction": "column", "justify-content": "center", "align-items": "center"},
                    ),
                    html.Div(
                        style={"width": "50%",
                               "margin": "0px", "padding": "0px"},
                        children=[
                            html.Div(
                                children=[
                                    html.Button("Skeletal Overlay",
                                                id="skeletal-overlay-button", style={"border-radius": "30px", "font-size": "25px", "padding": "5px", "margin": "5px"}),
                                    html.Button("Isolate Child",
                                                id="isolated-child-button", style={"border-radius": "30px", "font-size": "25px", "padding": "5px", "margin": "5px"}),
                                    html.Button("Isolate Therapist",
                                                id="isolated-therapist-button", style={"border-radius": "30px", "font-size": "25px", "padding": "5px", "margin": "5px"}),
                                    html.Button("Track Keypoints",
                                                id="track-keypoints-button", style={"border-radius": "30px", "font-size": "25px", "padding": "5px", "margin": "5px"}),
                                ],
                                style={
                                    "display": "flex",
                                    "flex-direction": "row",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "spacing": "10px",
                                },
                            ),
                        ]
                    ),
                ],
                    style={"display": "flex", "flex-direction": "row",
                           "align-items": "center", "justify_content": "center"},
                ),
                # Two main views, left is the original video, right is the comparison visualizations
                html.Div(children=[
                    dbc.Card(children=[
                        html.H1("Please select a video", id="video-placeholder", hidden=False,
                                style={"text-align": "center", "margin": "0px", "padding": "%dpx 0px"%(int(SCREEN_HEIGHT/4) - 24)}),
                        html.Div(id="video-player-visability", hidden=True, children=[
                            video_player(id="player_original", height="%dpx"%(int(SCREEN_HEIGHT/2)), style={
                                "padding": "10px"}),
                        ]),
                    ],
                        style={"width": "50%"},
                    ),
                    dbc.Card(children=[
                        html.H1("Pleace select a visualization mode", id="vis-view-placeholder", hidden=False,
                               style={"text-align": "center", "margin": "0px", "padding": "%dpx 0px"%(int(SCREEN_HEIGHT/4) - 24)}),
                        html.Div(id="vis-view-overlay", hidden=True, children=[
                            video_player(id="player_vis_overlay", height="%dpx"%(int(SCREEN_HEIGHT/2)), muted=True, style={
                                         "padding": "10px"})
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
                        style={"width": "50%"},
                    ),
                ],
                    style={"display": "flex", "flex-direction": "row"}
                ),

                # Video Controls, Timeline, Visualization Controls
                html.Div(children=[
                    html.Div(
                        style={"width": "25%", "padding": "0px"},
                        children=[
                            dbc.Card([
                                html.P("Main Video Controls:", style={
                                       "text-align": "center"}),
                                html.P("Volume:", style={
                                       "text-align": "center", "margin-bottom": "0px", "padding-bottom": "0px"}),
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
                                    "text-align": "center", "margin-bottom": "0px", "padding-bottom": "0px"}),
                                dcc.Slider(
                                    id="speed-slider",
                                    min=0.1,
                                    max=2,
                                    value=1,
                                    step=None,
                                    updatemode="drag",
                                    marks={
                                        i: str(i) + "x" for i in [0.1, 0.5, 1, 1.5, 2]},
                                ),
                                html.Div(
                                    children=[
                                        html.Button(
                                            "Play", id="play-button", style={"margin": "8px", "margin-bottom": "2px", "padding-left": "5px", "padding-right": "5px", "font-weight": "bold"}),
                                        html.Button(
                                            "Pause", id="pause-button", style={"margin": "8px", "margin-bottom": "2px", "font-weight": "bold"}),
                                    ],
                                    style={
                                        "width": "100%",
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "justify-content": "center",
                                        "align-items": "center",
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
                                                             "Expression of Wishes", id="ew-button", style={"border-radius": "30px", "font-size": "25px", "padding": "5px"}),
                                                         html.Button(
                                                             "Unscorable", id="un-button", style={"border-radius": "30px", "font-size": "25px", "padding": "5px", "padding-left": "20px", "padding-right": "20px"}),
                                                     ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "align-items": "flex-end"}),
                                                     html.Button(
                                                         "Other", id="ot-button", style={"border-radius": "30px", "font-size": "25px", "padding": "5px", "padding-top": "30px", "padding-bottom": "30px"}),
                                                     html.Div([
                                                         html.Button(
                                                             "Repetitive Behaviour", id="rb-button", style={"border-radius": "30px", "font-size": "25px", "padding": "5px"}),
                                                         html.Button(
                                                             "Functional Play", id="fp-button", style={"border-radius": "30px", "font-size": "25px", "padding": "5px"})
                                                     ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "align-items": "flex-start"}),
                                                 ],
                                              style={"text-align": "center", "display": "flex", "flex-direction": "row", "justify-content": "center", "align-items": "center"}),
                                 ],
                                     style={"margin": "8px", "padding": "5px"},
                                 ),
                    ],
                    ),
                    html.Div(style={"width": "25%"},
                             children=[
                                 dbc.Card([
                                     html.P("Visualization Controls:",
                                            style={"text-align": "center"}),
                                     html.Div("Please select a visualization mode", id="control-placeholder", hidden=False,
                                              style={"text-align": "center", "padding-bottom": "100px"}),
                                     html.Div(id="Overlay-Controls", hidden=True, children=[
                                         html.Div("Rendering skeleton on video.", style={
                                                  "text-align": "center"}),
                                         html.Div("Synching overlay with main video.", style={
                                                  "text-align": "center"})
                                     ],
                                         style={"width": "100%", "padding": "0px", "margin": "0px",
                                                "align-items": "center", "padding-bottom": "100px"},
                                     ),
                                     html.Div(id="Isolate-Controls", hidden=True,
                                              children=[
                                                  html.P("Isolate Controls", style={
                                                      "text-align": "center"}),
                                                  dcc.Checklist(
                                                      id="bool-props-isolate",
                                                      options=[
                                                          {"label": val.capitalize(),
                                                           "value": val}
                                                          for val in [
                                                              "right hand",
                                                              "left hand",
                                                              "right foot",
                                                              "left foot",
                                                          ]
                                                      ],
                                                      value=[],
                                                      inline=True,
                                                      style={"width": "100%", "display": "flex", "flex-direction": "row",
                                                             "justify-content": "space-evenly", "align-items": "center"},
                                                  ),
                                              ]
                                              ),
                                     html.Div(id="Track-Controls", hidden=True,
                                              children=[
                                                  html.P("Track Controls", style={
                                                      "text-align": "center"}),
                                                  dcc.Checklist(
                                                      id="bool-props-track",
                                                      options=[
                                                          {"label": val.capitalize(),
                                                           "value": val}
                                                          for val in [
                                                              "right hand",
                                                              "left hand",
                                                              "right foot",
                                                              "left foot",
                                                          ]
                                                      ],
                                                      value=[],
                                                      inline=True,
                                                      style={"width": "100%", "display": "flex", "flex-direction": "row",
                                                             "justify-content": "space-evenly", "align-items": "center"},
                                                  ),
                                              ],
                                              style={"width": "100%", "display": "flex", "flex-direction": "column",
                                                     "justify-content": "flex-start", "align-items": "center"},
                                              ),
                                 ],
                                     style={"width": "100%", "display": "flex",
                                            "flex-direction": "column"}
                                 ),
                    ]
                    )
                ],
                    style={"display": "flex", "flex-direction": "row",
                           "align-items": "flex-start"},
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
    Output("current-time", "children"),
    Input("player_original", "currentTime"),
)
def update_current_time(current_time):
    return current_time


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
    ori_vid = f"assets/{value}/{value}_original.mp4"
    vis_vid = f"assets/{value}/superposition/{value}_openpose.mp4"
    return ori_vid, vis_vid, True, False


@app.callback(
    Output("graph-isolated-child", "figure"),
    Input("player_original", "currentTime"),
    Input("bool-props-isolate", "value"),
    State("video-dropdown", "value"),
)
def update_vis_view_isolated(current_time, val_list, value_folder):
    highlight_dict = {"RH": "right hand" in val_list, "LH": "left hand" in val_list,
                      "RF": "right foot" in val_list, "LF": "left foot" in val_list}
    current_time = 0 if current_time is None else current_time
    return render_keypoints(child[value_folder], highlight_dict, int(current_time * fps[value_folder]) - 1, int(SCREEN_HEIGHT/2))


@app.callback(
    Output("graph-isolated-therapist", "figure"),
    Input("player_original", "currentTime"),
    Input("bool-props-isolate", "value"),
    State("video-dropdown", "value"),
)
def update_vis_view_isolated(current_time, val_list, value_folder):
    highlight_dict = {"RH": "right hand" in val_list, "LH": "left hand" in val_list,
                      "RF": "right foot" in val_list, "LF": "left foot" in val_list}
    current_time = 0 if current_time is None else current_time
    return render_keypoints(therapist[value_folder], highlight_dict, int(current_time * fps[value_folder]) - 1, int(SCREEN_HEIGHT/2))


@app.callback(
    Output("graph-track", "figure"),
    Input("player_original", "currentTime"),
    Input("bool-props-track", "value"),
    State("video-dropdown", "value"),
)
def update_vis_view_isolated(current_time, val_list, value_folder):
    track_dict = {"RH": "right hand" in val_list, "LH": "left hand" in val_list,
                  "RF": "right foot" in val_list, "LF": "left foot" in val_list}
    duration = int(10 * fps[value_folder])
    current_time = 0 if current_time is None else current_time
    return render_tracked_keypoints(child[value_folder], track_dict, duration, int(current_time * fps[value_folder]) - 1, int(SCREEN_HEIGHT/2))


@app.callback(
    Output("timeline-graph", "figure"),
    Input("player_original", "currentTime"),
    Input("video-dropdown", "value"),
)
def update_timeline(current_time, value_folder):
    if current_time is None or value_folder is None:
        return no_update
    return no_update
    # return render_timeline(objects[value_folder], interactions[value_folder], abcs[value_folder], dur_sec[value_folder], fps[value_folder], int(current_time * fps[value_folder]))


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
    Input("seek-bar-slider", "value"),
    Input("player_original", "duration"),
    Input("player_original", "currentTime"),
)
def update_seek_bar(value, duration, current_time):
    duration = int(duration) if duration is not None else 1
    value = int(value) if value is not None else 0
    ctx = callback_context
    input_trigger = ctx.triggered[0]["prop_id"]
    if input_trigger == "seek-bar-slider.value":
        # marks = {0: str(datetime.timedelta(seconds=0)), value: str(datetime.timedelta(seconds=value)), duration: str(datetime.timedelta(seconds=duration))}
        marks = {value: str(datetime.timedelta(seconds=value))}
        return value, value, duration, marks, no_update
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


if __name__ == "__main__":
    app.run_server(debug=True, port=1729)
