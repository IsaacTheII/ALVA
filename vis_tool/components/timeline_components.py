import plotly.graph_objs as go
import time
import numpy as numpy




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

    DURATION_IN_SECONDS = 60        # timespan of the timeline view in seconds
    NUM_TRACKS = 7     # number of tracks on the timeline
    """ 
    lower_bound = frame_num - DURATION_IN_SECONDS * .5 * fps
    upper_bound = frame_num + DURATION_IN_SECONDS * .5 * fps
    if lower_bound < 0:
        lower_bound = 0
        upper_bound = DURATION_IN_SECONDS * fps
    if upper_bound > total_frames:
        upper_bound = total_frames
        lower_bound = total_frames - DURATION_IN_SECONDS * fps
    if lower_bound < 0:
        lower_bound = 0
        upper_bound = total_frames

    fig.update_xaxes(range=[lower_bound - 10, upper_bound + 10]) 
    """
    fig.update_yaxes(range=[-0.1, NUM_TRACKS + .1])
    fig.update_xaxes(range=[frame_num - DURATION_IN_SECONDS * fps * .5, frame_num + DURATION_IN_SECONDS * fps * .5], tickformat="%H:%M:%S s")

    # draw grid
    for i in range(0, NUM_TRACKS+2):
        fig.add_shape(type="line", x0=0, y0=i, x1=total_frames,
                      y1=i, line=dict(color="grey", width=1, dash="dot"))

    # draw current time
    fig.add_shape(type="line", x0=frame_num, y0=0, x1=frame_num,
                  y1=NUM_TRACKS+1, line=dict(color="red", width=2))

    # draw objects
    for index, row in object.iterrows():
        y_off = (index) % (NUM_TRACKS - 2)
        fig.add_shape(type="rect", x0=row["Start_Time"], y0=NUM_TRACKS - y_off - 1, x1=row["End_Time"], y1=NUM_TRACKS - y_off,
                      line=dict(color="blue", width=2), fillcolor="blue", opacity=0.5,)
        fig.add_annotation(x=row["Start_Time"], xanchor="left", y=NUM_TRACKS - y_off - 0.5,
                           text=row["Object_Name"], showarrow=False, font=dict(size=15))
        
    # draw interactions
    for index, row in interactions.iterrows():
        fig.add_shape(type="rect", x0=row["Event_Time"], y0=1, x1=row["Event_Time"] + 0.5 * fps, y1=2,
                      line=dict(color="red", width=2), fillcolor="red", opacity=0.5,)
        fig.add_annotation(x=row["Event_Time"], xanchor="left", y=1.9 - index % 4*0.25,
                           text=row["Event_Description"], showarrow=False, font=dict(size=10))

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

