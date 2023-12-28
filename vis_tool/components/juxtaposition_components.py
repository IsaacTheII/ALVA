import plotly.graph_objs as go
import numpy as numpy


def render_keypoints(keypoints, frame_num):
    fig = go.Figure()

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), showlegend=False,
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
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
    
    return fig