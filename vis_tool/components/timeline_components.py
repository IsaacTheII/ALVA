import plotly.graph_objs as go
import time
import numpy as numpy
import pandas as pd
from vis_tool.config.settings import abcs_code_colors as abcs_color_codes

DURATION_IN_SECONDS = 60        # timespan of the timeline view in seconds
NUM_TRACKS = 7                  # number of tracks on the timeline


def render_timeline(object, interactions, abcs, duration, fps, frame_num):
    fig = go.Figure()

    total_frames = int(duration * fps)
    tick_num = numpy.arange(0, total_frames, fps * 10)
    tick_text = [time.strftime("%H:%M:%S", time.gmtime(f / fps)) for f in tick_num]
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), showlegend=False,
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      xaxis=dict(showgrid=False, 
                                 zeroline=False, 
                                 tickmode='array',
                                 tickvals=tick_num,
                                 ticktext=tick_text
                      )
                      )
    
    fig.update_yaxes(range=[-0.1, NUM_TRACKS + .1])
    fig.update_xaxes(range=[frame_num - DURATION_IN_SECONDS * fps * .5, frame_num + DURATION_IN_SECONDS * fps * .5], tickformat="%H:%M:%S s")

    # draw grid
    for i in range(0, NUM_TRACKS+2):
        fig.add_shape(type="line", x0=0, y0=i, x1=total_frames,
                      y1=i, line=dict(color="grey", width=1, dash="dot"))

    # draw objects
    for index, row in object.iterrows():
        #if row["End_Time"] < frame_num - DURATION_IN_SECONDS * fps * .5 or row["Start_Time"] > frame_num + DURATION_IN_SECONDS * fps * .5:
        #    continue
        y_off = (index) % (NUM_TRACKS - 2)
        fig.add_shape(type="rect", x0=row["Start_Time"], y0=NUM_TRACKS - y_off - 1, x1=row["End_Time"], y1=NUM_TRACKS - y_off,
                      fillcolor="cornflowerblue")
        fig.add_annotation(x=row["Start_Time"], xanchor="left", y=NUM_TRACKS - y_off - 0.5,
                           text=row["Object_Name"], showarrow=False, font=dict(size=15))
        
    # draw interactions
    for index, row in interactions.iterrows():
        #if row["Event_Time"] < frame_num - DURATION_IN_SECONDS * fps * .5 or row["Event_Time"] > frame_num + DURATION_IN_SECONDS * fps * .5:
        #    continue
        fig.add_shape(type="rect", x0=row["Event_Time"], y0=1, x1=row["Event_Time"] + 0.5 * fps, y1=2,
                      fillcolor="plum", line_color="plum")
        fig.add_annotation(x=row["Event_Time"], xanchor="left", y=2 - index % 4*0.251,
                           text=row["Event_Description"], showarrow=False, font=dict(size=10))
        
    # draw abcs
    for index, row in abcs.iterrows():
        #if row["End_Time"] < frame_num - DURATION_IN_SECONDS * fps * .5 or row["Start_Time"] > frame_num + DURATION_IN_SECONDS * fps * .5:
        #    continue
        fig.add_shape(type="rect", x0=row["Start_Time"], y0=0, x1=row["End_Time"], y1=1,
                      line=dict(color="green", width=2), fillcolor=abcs_color_codes[row["ABCS_Variable"]], opacity=0.5,)
        fig.add_annotation(x=row["Start_Time"], xanchor="left", y=0.5,
                           text=row["ABCS_Variable"], showarrow=False, font=dict(size=15))

    """ # draw current time
    fig.add_shape(type="line", x0=frame_num, y0=0, x1=frame_num,
                  y1=NUM_TRACKS+1, line=dict(color="red", width=2)) """
    
    return fig
""" 
    # draw objects 
    def draw_obj(row, y_off):
        y_pos = NUM_TRACKS
        fig.add_shape(type="rect", x0=row["Start_Time"], y0=y_pos - y_off, x1=row["End_Time"], y1=y_pos + 1 - y_off,
                      line=dict(color="blue", width=2), fillcolor="blue", opacity=0.5,)
        x_off = int(DURATION_IN_SECONDS * fps)
        for i in range(0, int(row["Start_Time"] - row["End_Time"]) % x_off + 1):
            fig.add_annotation(x=row["Start_Time"] + i * x_off, xanchor="left", y=y_pos + 0.5 - y_off,
                           text=row["Object_Name"], showarrow=False, font=dict(size=10))
    time = []
    for index, row in object.iterrows():
        if time == []:
            draw_obj(row, 0)
            time.append([row["Start_Time"], row["End_Time"], 1])
        new = True
        for trip in time:
            if trip[1] > row["Start_Time"] and trip[0] < row["End_Time"]:
                draw_obj(row, trip[2])
                trip = [min(trip[0], row["Start_Time"]), max(trip[1], row["End_Time"]), trip[2] + 1]
                new = False
                break
        if new:
            draw_obj(row, 0)
            time.append([row["Start_Time"], row["End_Time"], 1])

    # draw objects
    start_end  = []
    for index, row in object.iterrows():
        start_end.append(('start', row["Start_Time"]))
        start_end.append(('end', row["End_Time"]))
    start_end.sort(key=lambda x: x[1])
    count = 0
    max_count = 0
    start_off = []
    for time in start_end:
        if time[0] == 'start':
            start_off.append((time[1], count))
            count += 1
        else:
            count -= 1
        if count > max_count:
            max_count = count
    y_pos = NUM_TRACKS
    for _, row in object.iterrows():        
        _, y_off = start_off.pop(start_off.index([e for e in start_off if e[0] == row["Start_Time"]][0]))
        fig.add_shape(type="rect", x0=row["Start_Time"], y0=y_pos - y_off, x1=row["End_Time"], y1=y_pos + 1 - y_off,
                      line=dict(color="blue", width=2), fillcolor="blue", opacity=0.5,)
        x_off = int(DURATION_IN_SECONDS * fps)
        for i in range(0, int(row["Start_Time"] - row["End_Time"]) % x_off + 1):
            fig.add_annotation(x=row["Start_Time"] + i * x_off, xanchor="left", y=y_pos + 0.5 - y_off,
                           text=row["Object_Name"], showarrow=False, font=dict(size=10))
    """

def update_abcs_coding(abcs, frame_num, code):
    for index, row in abcs.iterrows():
        if row["End_Time"] >= frame_num:
            return abcs
    if abcs.empty:
        abcs.loc[len(abcs)] = [0, frame_num, code, ""]
    else:
        abcs.loc[len(abcs)] = [abcs.iloc[-1]["End_Time"] + 1, frame_num, code, ""]
    return abcs

