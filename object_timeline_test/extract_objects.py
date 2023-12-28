import os

from ultralytics import YOLO

model = YOLO('./models/yolov8l.pt')

objects_dict = model.names

objects_dict = {str(key): value for key, value in objects_dict.items()}

print(objects_dict)

objects_of_interest = {"cup": [], "bowl": [], "teddy bear": []}

def extract_objects(dir):

    files = os.listdir(dir)

    # dictionary with the frame number as key and a list of objects in that frame as value
    objects_all_frames = {key: [] for key in range(len(files))}

    set_of_objects = set()

    for file in files:
        with open(os.path.join(dir, file), "r") as f:
            lines = f.readlines()

            objects_in_frame = []

            for line in lines:
                set_of_objects.add(objects_dict[line.split(" ")[0]])
                objects_in_frame.append([objects_dict[line.split(" ")[0]], line.split(" ")[1:-1]]) # [object, [x, y, w, h]]
    
    print(set_of_objects)


if __name__ == "__main__":
    extract_objects("object_timeline_test\labels")