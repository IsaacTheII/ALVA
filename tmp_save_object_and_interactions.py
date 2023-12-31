import os
import cv2
import time

from structures.timeline_structure import Timeline

from analysis import extract_objects
from analysis import extract_interactions

def parse_seconds(sec):
    return time.strftime("%H:%M:%S", time.gmtime(sec))

if __name__ == "__main__":
    # path to the video file and processed video files
    video_name = os.path.join("vis_tool", "assets", "Sirius_Intensiv_Spiel_1A_repetitive_0_anonymized" , "Sirius_Intensiv_Spiel_1A_repetitive_0_anonymized_original.mp4" )
    interaction_dir = os.path.join("runs_full_run", "RelTR")
    object_dir = os.path.join("runs_full_run","detect","predict","labels")

    # init timeline
    cap = cv2.VideoCapture(video_name)

    timeline = Timeline(
        video_name = os.path.basename(video_name).split(".")[0],
        duration=cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS),
        frame_width=cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        frame_height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
        frame_rate=cap.get(cv2.CAP_PROP_FPS),
        total_frames=cap.get(cv2.CAP_PROP_FRAME_COUNT),
        date_recorded=time.strftime("%Y-%m-%d", time.strptime(time.ctime(os.path.getctime(video_name)))),
        author="max mustermann",
        date_coding=time.strftime("%Y-%m-%d", time.strptime(time.ctime(os.path.getctime(video_name)))),
    )

    # extract objects
    objects = extract_objects.extract_objects(object_dir, fps=int(float(timeline.Frame_Rate)), life_time_seconds=10)

    # insert objects into timeline
    for objname, list_start_end in objects.items():
        for start, end in list_start_end:
            print(objname, start, end, start / cap.get(cv2.CAP_PROP_FPS), parse_seconds(start / cap.get(cv2.CAP_PROP_FPS)))
            timeline.add_object(parse_seconds(start / cap.get(cv2.CAP_PROP_FPS)), parse_seconds(end / cap.get(cv2.CAP_PROP_FPS)), objname)

    # extract interactions
    interactions = extract_interactions.extract_object_interactions_events(interaction_dir, fps=int(float(timeline.Frame_Rate)), life_time_seconds=3)
    for start, event in interactions.items():
        timeline.add_object_interaction(parse_seconds(start / cap.get(cv2.CAP_PROP_FPS)), "Is " + event[0] + " " + event[1] + ".")


    timeline.export_to_file("timeline_test.txt")

    
