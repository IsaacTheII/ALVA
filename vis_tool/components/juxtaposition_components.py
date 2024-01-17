import plotly.graph_objs as go
import numpy as np
from vis_tool.config.settings import hf_color


def render_keypoints(keypoints, RH, LH, RF, LF, frame_num, x_max, y_max, scr_height=600):
    fig = go.Figure()

    fig.update_layout(margin=dict(l=10, r=10, b=10, t=10),
                      showlegend=False,
                      xaxis=dict(range=[0, x_max], showgrid=False, zeroline=False,
                                 mirror=True, showline=True, showticklabels=False),
                      yaxis=dict(range=[-y_max, 0], showgrid=False, zeroline=False,
                                 mirror=True, showline=True, showticklabels=False, scaleanchor="x"),
                      height=scr_height
                      )
    
    fig.add_trace(go.Scatter(x=keypoints[:, 0, frame_num],
                             y=keypoints[:, 1, frame_num],))

    if RH:
        fig.add_trace(go.Scatter(x=[keypoints[7, 0, frame_num]],
                                 y=[keypoints[7, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['RH']), marker_line_width=2))
    if LH:
        fig.add_trace(go.Scatter(x=[keypoints[16, 0, frame_num]],
                                 y=[keypoints[16, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['LH']), marker_line_width=2))
    if RF:
        fig.add_trace(go.Scatter(x=[keypoints[28, 0, frame_num]],
                                 y=[keypoints[28, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['RF']), marker_line_width=2))
    if LF:
        fig.add_trace(go.Scatter(x=[keypoints[43, 0, frame_num]],
                                 y=[keypoints[43, 1, frame_num]],
                                 mode='markers', marker=dict(size=15, color=hf_color['LF']), marker_line_width=2))

    return fig


def convert_keypoints_to_skeleton(keypoints):
    keypoints_size = keypoints[0, :, :].shape
    div = np.full(keypoints_size, None)
    skeleton = np.stack([           #keypoints[0, :, :], keypoints[1, :, :], div,
                                    keypoints[1, :, :], keypoints[2, :, :],
                               div, keypoints[2, :, :], keypoints[3, :, :],
                               div, keypoints[3, :, :], keypoints[4, :, :],
                               div, keypoints[1, :, :], keypoints[5, :, :],
                               div, keypoints[5, :, :], keypoints[6, :, :],
                               div, keypoints[6, :, :], keypoints[7, :, :],
                               div, keypoints[1, :, :], keypoints[8, :, :],
                               div, keypoints[8, :, :], keypoints[9, :, :],
                               div, keypoints[9, :, :], keypoints[10, :, :],
                               div, keypoints[10, :, :], keypoints[11, :, :],
                               div, keypoints[11, :, :], keypoints[24, :, :],
                               div, keypoints[11, :, :], keypoints[22, :, :],
                               #div, keypoints[22, :, :], keypoints[23, :, :],
                               div, keypoints[8, :, :], keypoints[12, :, :],
                               div, keypoints[12, :, :], keypoints[13, :, :],
                               div, keypoints[13, :, :], keypoints[14, :, :],
                               div, keypoints[14, :, :], keypoints[21, :, :],
                               div, keypoints[14, :, :], keypoints[19, :, :]])
                               #div, keypoints[19, :, :], keypoints[20, :, :]])
                               #div, keypoints[0, :, :], keypoints[15, :, :],
                               #div, keypoints[15, :, :], keypoints[17, :, :],
                               #div, keypoints[0, :, :], keypoints[16, :, :],
                               #div, keypoints[16, :, :], keypoints[18, :, :]])
    return skeleton
