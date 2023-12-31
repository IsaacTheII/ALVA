import os
import json

from ultralytics import YOLO

FPS = 25    # frames per second

LIFE_TIME_SECONDS = 3   # seconds

LIFE_TIME_SECONDS = 3   # seconds

# get the object names from the yolo model
model = YOLO('./models/yolov8l.pt')
objects_dict = dict(model.names)

objects_dict = {str(key): value for key, value in objects_dict.items()}

# key are objects of interest and values are common mismatches ##TODO: add further objects of interest
objects_of_interest = {"cup": [], "bowl": ["toilet", "sink"], "teddy bear": []}



def extract_objects(dir, fps=FPS, life_time_seconds=LIFE_TIME_SECONDS):

    files = sorted(os.listdir(dir), key=lambda x: int(x.split(".")[0].split("_")[-1]))

    # dictionary with the frame number as key and a list of objects in that frame as value
    objects_all_frames = {}

    obj_mismatch = list(objects_of_interest.keys()) + [item for value in objects_of_interest.values() for item in value]

    for file in files:
        frame_number = int(file.split(".")[0].split("_")[-1])
        with open(os.path.join(dir, file), "r") as f:
            lines = f.readlines()
            objects_in_frame = set()
            for line in lines:
                name = objects_dict[line.split(" ")[0]]  # convert class index to class name
                # skip if object is not in common mismatch list
                if name not in obj_mismatch:
                    continue
                # if object is in common mismatch list, convert to correct name
                for key, value in objects_of_interest.items():
                    if name in value:
                        name = key
                        break
                # add object to list of objects in frame
                objects_in_frame.add(name)
            if len(list(objects_in_frame)) > 0:
                objects_all_frames[frame_number] = list(objects_in_frame)

    # track previous objects
    active_objects = {}
    # track the start frame of new objects
    start_end_frame_objects = {}        # {"name_of_object": [[start_frame, end_frame]]"}
    # max duration of an object before it is considered a new object
    lifetime = life_time_seconds * fps *4
    for key in sorted(objects_all_frames.keys()):
        for object in objects_all_frames[key]:
            # new object
            if object not in active_objects.keys():
                start_end_frame_objects[object] = [[key, key + lifetime]]  # save the start frame of the object
                active_objects[object] = key  # save the current frame of the object
            # object already active
            elif key - active_objects[object] <= lifetime:
                if start_end_frame_objects[object][-1][1] < key:
                    start_end_frame_objects[object][-1][1] = key   # update the end frame of the last object
                active_objects[object] = key   # update the current frame of the object
            # object too old, start new object
            else:
                start_end_frame_objects[object].append([key, key + lifetime])  # save the start frame of the object
                active_objects[object] = key  # save the current frame of the object
    return start_end_frame_objects

