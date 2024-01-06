import plotly.graph_objs as go
import numpy as numpy
from vis_tool.config.settings import hf_color


def render_keypoints(keypoints, RH, LH, RF, LF, frame_num, scr_height=600):
    fig = go.Figure()

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), showlegend=False,
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      height=scr_height
    )

    x_min = numpy.nanmin(keypoints[:, 0, :])
    x_max = numpy.nanmax(keypoints[:, 0, :])
    y_min = numpy.nanmin(keypoints[:, 1, :])
    y_max = numpy.nanmax(keypoints[:, 1, :])

    
    # Set fixed minimum and maximum values for x and y axes
    fig.update_xaxes(range=[x_min, x_max])
    fig.update_yaxes(range=[y_min, y_max])

    fig.add_trace(go.Scatter(x=keypoints[:, 0, frame_num], 
                             y=keypoints[:, 1, frame_num],
                             mode='markers',))
    
    if RH:
        fig.add_trace(go.Scatter(x=[keypoints[4, 0, frame_num]], 
                                 y=[keypoints[4, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['RH']), marker_line_width=2))
    if LH:
        fig.add_trace(go.Scatter(x=[keypoints[7, 0, frame_num]], 
                                 y=[keypoints[7, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['LH']), marker_line_width=2))
    if RF:
        fig.add_trace(go.Scatter(x=[keypoints[11, 0, frame_num]], 
                                 y=[keypoints[11, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['RF']), marker_line_width=2))
    if LF:
        fig.add_trace(go.Scatter(x=[keypoints[14, 0, frame_num]], 
                                 y=[keypoints[14, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['LF']), marker_line_width=2))
    
    return fig