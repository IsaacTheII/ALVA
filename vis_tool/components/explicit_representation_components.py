import plotly.graph_objs as go
import numpy as numpy
from vis_tool.config.settings import hf_color




def render_tracked_keypoints(skeleton, dict_track, duration, frame_num,  x_max, y_max, scr_height=600):
    fig = go.Figure()

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), showlegend=False,
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    height=scr_height
    )

    
    # Set fixed minimum and maximum values for x and y axes
    fig.update_xaxes(range=[0, x_max])
    fig.update_yaxes(range=[-y_max, 0])

    # traces and higlighted points for each True value in dict_track
    if dict_track['RH']:
        traces_x = []
        traces_y = []
        for frame in range(frame_num - duration if frame_num - duration >= 0 else 0, frame_num + 1):
            traces_x.append(skeleton[4, 0, frame])
            traces_y.append(skeleton[4, 1, frame])
        fig.add_trace(go.Scatter(x=traces_x, y=traces_y, mode='lines', marker=dict(color=hf_color['RH'], opacity=0.5), line=dict(width=3)))
        fig.add_trace(go.Scatter(x=[skeleton[4, 0, frame_num]], 
                                 y=[skeleton[4, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['RH']), marker_line_width=2))
    if dict_track['LH']:
        traces_x = []
        traces_y = []
        for frame in range(frame_num - duration if frame_num - duration >= 0 else 0, frame_num + 1):
            traces_x.append(skeleton[7, 0, frame])
            traces_y.append(skeleton[7, 1, frame])
        fig.add_trace(go.Scatter(x=traces_x, y=traces_y, mode='lines', marker=dict(color=hf_color['LH'], opacity=0.5), line=dict(width=3)))
        fig.add_trace(go.Scatter(x=[skeleton[7, 0, frame_num]], 
                                 y=[skeleton[7, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['LH']), marker_line_width=2))
    if dict_track['RF']:
        traces_x = []
        traces_y = []
        for frame in range(frame_num - duration if frame_num - duration >= 0 else 0, frame_num + 1):
            traces_x.append(skeleton[11, 0, frame])
            traces_y.append(skeleton[11, 1, frame])
        fig.add_trace(go.Scatter(x=traces_x, y=traces_y, mode='lines', marker=dict(color=hf_color['RF'], opacity=0.5), line=dict(width=3)))
        fig.add_trace(go.Scatter(x=[skeleton[11, 0, frame_num]], 
                                 y=[skeleton[11, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['RF']), marker_line_width=2))
    if dict_track['LF']:
        traces_x = []
        traces_y = []
        for frame in range(frame_num - duration if frame_num - duration >= 0 else 0, frame_num + 1):
            traces_x.append(skeleton[14, 0, frame])
            traces_y.append(skeleton[14, 1, frame])
        fig.add_trace(go.Scatter(x=traces_x, y=traces_y, mode='lines', marker=dict(color=hf_color['LF'], opacity=0.5), line=dict(width=3)))
        fig.add_trace(go.Scatter(x=[skeleton[14, 0, frame_num]], 
                                 y=[skeleton[14, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['LF']), marker_line_width=2))
   
    return fig