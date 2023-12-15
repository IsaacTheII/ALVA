import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation



def calculate_iou(bbox1, bbox2):
    # get the coordinates of the bounding boxes
    x_min_1, y_min_1, x_max_1, y_max_1 = bbox1
    x_min_2, y_min_2, x_max_2, y_max_2 = bbox2

    # get the coordinates of the intersection rectangle
    x_left = max(x_min_1, x_min_2)
    y_top = max(y_min_1, y_min_2)
    x_right = min(x_max_1, x_max_2)
    y_bottom = min(y_max_1, y_max_2)

    # Intersection area
    intersection_area = max(0, x_right - x_left + 1) * max(0, y_bottom - y_top + 1)

    # Union Area
    bb1_area = (x_max_1 - x_min_1 + 1) * (y_max_1 - y_min_1 + 1)
    bb2_area = (x_max_2 - x_min_2 + 1) * (y_max_2 - y_min_2 + 1)
    union_area = (bb1_area + bb2_area) - intersection_area

    return intersection_area / union_area

def insert_keypoints(keypoint_dict, x, y, frame_index):
    # insert the keypoints into the keypoint_dict
    keypoint_dict["Nose"][:,frame_index] = np.array([x[0], y[0]])
    keypoint_dict["Neck"][:,frame_index] = np.array([x[1], y[1]])
    keypoint_dict["RShoulder"][:,frame_index] = np.array([x[2], y[2]])
    keypoint_dict["RElbow"][:,frame_index] = np.array([x[3], y[3]])
    keypoint_dict["RWrist"][:,frame_index] = np.array([x[4], y[4]])
    keypoint_dict["LShoulder"][:,frame_index] = np.array([x[5], y[5]])
    keypoint_dict["LElbow"][:,frame_index] = np.array([x[6], y[6]])
    keypoint_dict["LWrist"][:,frame_index] = np.array([x[7], y[7]])
    keypoint_dict["MidHip"][:,frame_index] = np.array([x[8], y[8]])
    keypoint_dict["RHip"][:,frame_index] = np.array([x[9], y[9]])
    keypoint_dict["RKnee"][:,frame_index] = np.array([x[10], y[10]])
    keypoint_dict["RAnkle"][:,frame_index] = np.array([x[11], y[11]])
    keypoint_dict["LHip"][:,frame_index] = np.array([x[12], y[12]])
    keypoint_dict["LKnee"][:,frame_index] = np.array([x[13], y[13]])
    keypoint_dict["LAnkle"][:,frame_index] = np.array([x[14], y[14]])
    keypoint_dict["REye"][:,frame_index] = np.array([x[15], y[15]])
    keypoint_dict["LEye"][:,frame_index] = np.array([x[16], y[16]])
    keypoint_dict["REar"][:,frame_index] = np.array([x[17], y[17]])
    keypoint_dict["LEar"][:,frame_index] = np.array([x[18], y[18]])
    keypoint_dict["LBigToe"][:,frame_index] = np.array([x[19], y[19]])
    keypoint_dict["LSmallToe"][:,frame_index] = np.array([x[20], y[20]])
    keypoint_dict["LHeel"][:,frame_index] = np.array([x[21], y[21]])
    keypoint_dict["RBigToe"][:,frame_index] = np.array([x[22], y[22]])
    keypoint_dict["RSmallToe"][:,frame_index] = np.array([x[23], y[23]])
    keypoint_dict["RHeel"][:,frame_index] = np.array([x[24], y[24]])



def get_keypoints_openpose(directory, total_frames):
    
    # Construct the path to the openpose_output directory
    openpose_output_dir = directory

    # List the files in the directory
    files = os.listdir(openpose_output_dir)
    if len(files) != total_frames:
        raise ValueError("Number of files in the directory does not match the total number of frames")
    
    # List of people in the video
    xy = np.empty((2, total_frames))
    xy.fill(np.nan)

    person_1 = {
        "keypoints": {
            "Nose": np.copy(xy),
            "Neck": np.copy(xy),
            "RShoulder": np.copy(xy),
            "RElbow": np.copy(xy),
            "RWrist": np.copy(xy),
            "LShoulder": np.copy(xy),
            "LElbow": np.copy(xy),
            "LWrist": np.copy(xy),
            "MidHip": np.copy(xy),
            "RHip": np.copy(xy),
            "RKnee": np.copy(xy),
            "RAnkle": np.copy(xy),
            "LHip": np.copy(xy),
            "LKnee": np.copy(xy),
            "LAnkle": np.copy(xy),
            "REye": np.copy(xy),
            "LEye": np.copy(xy),
            "REar": np.copy(xy),
            "LEar": np.copy(xy),
            "LBigToe": np.copy(xy),
            "LSmallToe": np.copy(xy),
            "LHeel": np.copy(xy),
            "RBigToe": np.copy(xy),
            "RSmallToe": np.copy(xy),
            "RHeel": np.copy(xy),
        },
        "bbox": [],

    }
    person_2 = {
        "keypoints": {
            "Nose": np.copy(xy),
            "Neck": np.copy(xy),
            "RShoulder": np.copy(xy),
            "RElbow": np.copy(xy),
            "RWrist": np.copy(xy),
            "LShoulder": np.copy(xy),
            "LElbow": np.copy(xy),
            "LWrist": np.copy(xy),
            "MidHip": np.copy(xy),
            "RHip": np.copy(xy),
            "RKnee": np.copy(xy),
            "RAnkle": np.copy(xy),
            "LHip": np.copy(xy),
            "LKnee": np.copy(xy),
            "LAnkle": np.copy(xy),
            "REye": np.copy(xy),
            "LEye": np.copy(xy),
            "REar": np.copy(xy),
            "LEar": np.copy(xy),
            "LBigToe": np.copy(xy),
            "LSmallToe": np.copy(xy),
            "LHeel": np.copy(xy),
            "RBigToe": np.copy(xy),
            "RSmallToe": np.copy(xy),
            "RHeel": np.copy(xy),
        },
        "bbox": [],
    }


    for file, frame_index in zip(files, range(len(files))):
        # Construct the path to the file
        file_path = os.path.join(openpose_output_dir, file)

        # collect all the detected people in the frame
        person_in_frame = []
        
        # Open the json file and read the json object
        with open(file_path, 'r') as f:
            json_object = json.load(f)

            # Get the people array from the json object
            people = json_object['people']

            # read the keypoints for each person in the frame and store in a person list of current frame
            for person in people:
                # Get the pose_keypoints_2d array from the person object
                pose_keypoints_2d = person['pose_keypoints_2d']

                x = pose_keypoints_2d[0::3]
                y = pose_keypoints_2d[1::3]

                # calculate the bounding box from the person object. Important: discard all 0.0 values as they represent missing keypoints
                bbox = [min(filter(lambda val: val >= 0.0, x)), min(filter(lambda val: val >= 0.0, y)), max(x), max(y)]
                #bbox = [min(x), min(y), max(x), max(y)]

                # add the bounding box and keypoints to the person in the frame
                person_in_frame.append([x, y, bbox])

        # compare the bounding box of the person_1 and person_2 with the bounding box of the people in the frame
        # if the bounding box of the person in the frame is within the bounding box of the person_1 or person_2, add the keypoints to the person_1 or person_2

        best_iou = np.zeros((len(person_in_frame), 2))
        for person, person_index in zip(person_in_frame, range(len(person_in_frame))):
            # get the bounding box of the person in the frame
            bbox = person[2]

            # calculate the iou with the person_1
            iou_person_1 = calculate_iou(bbox, person_1["bbox"][len(person_1["bbox"]) - 1] if len(person_1["bbox"]) > 0 else [0, 0, 0, 0])

            # calculate the iou with the person_2
            iou_person_2 = calculate_iou(bbox, person_2["bbox"][len(person_2["bbox"]) - 1] if len(person_2["bbox"]) > 0 else [0, 0, 0, 0])

            # store the iou values in best_iou
            best_iou[person_index, 0] = iou_person_1
            best_iou[person_index, 1] = iou_person_2

            """ # if the iou with the person_1 is greater than the iou with the person_2, add the keypoints to the person_1
            if iou_person_1 > iou_person_2:
                insert_keypoints(person_1["keypoints"], person[0], person[1], frame_index)
                person_1["bbox"].append(bbox)
            # if the iou with the person_2 is greater than the iou with the person_1, add the keypoints to the person_2
            elif iou_person_2 > iou_person_1:
                insert_keypoints(person_2["keypoints"], person[0], person[1], frame_index)
                person_2["bbox"].append(bbox)
            # if the iou with the person_1 and person_2 are equal, add the keypoints to the person_1
            else:
                insert_keypoints(person_1["keypoints"], person[0], person[1], frame_index)
                person_1["bbox"].append(bbox) """
        
        # choose the best iou in the best_iou array and add the keypoints to the person_1 or person_2 then set all values to zero for that row.
        if len(person_in_frame) == 0:
            continue
        if len(person_in_frame) == 1:
            if best_iou[0, 0] > best_iou[0, 1]:
                insert_keypoints(person_1["keypoints"], person_in_frame[0][0], person_in_frame[0][1], frame_index)
                person_1["bbox"].append(person_in_frame[0][2])
            else:
                insert_keypoints(person_2["keypoints"], person_in_frame[0][0], person_in_frame[0][1], frame_index)
                person_2["bbox"].append(person_in_frame[0][2])
            continue
        else:
            # get the index absolute best iou in best_iou array
            best_iou_index = np.unravel_index(np.argmax(best_iou, axis=None), best_iou.shape)
            if best_iou_index[1] == 0:
                # add the keypoints to the person_1
                insert_keypoints(person_1["keypoints"], person_in_frame[best_iou_index[0]][0], person_in_frame[best_iou_index[0]][1], frame_index)
                person_1["bbox"].append(person_in_frame[best_iou_index[0]][2])
                
                # set the best iou to zero for the column of person_1 and row of person_in_frame
                best_iou[best_iou_index[0], :] = 0
                best_iou[:, best_iou_index[1]] = 0

                # get the best iou index again  and add the keypoints to the person_2
                best_iou_index = np.unravel_index(np.argmax(best_iou, axis=None), best_iou.shape)
                insert_keypoints(person_2["keypoints"], person_in_frame[best_iou_index[0]][0], person_in_frame[best_iou_index[0]][1], frame_index)
                person_2["bbox"].append(person_in_frame[best_iou_index[0]][2])
            else:
                # add the keypoints to the person_2
                insert_keypoints(person_2["keypoints"], person_in_frame[best_iou_index[0]][0], person_in_frame[best_iou_index[0]][1], frame_index)
                person_2["bbox"].append(person_in_frame[best_iou_index[0]][2])

                # set the best iou to zero for the column of person_2 and row of person_in_frame
                best_iou[best_iou_index[0], :] = 0
                best_iou[:, best_iou_index[1]] = 0

                # get the best iou index again  and add the keypoints to the person_1
                best_iou_index = np.unravel_index(np.argmax(best_iou, axis=None), best_iou.shape)
                insert_keypoints(person_1["keypoints"], person_in_frame[best_iou_index[0]][0], person_in_frame[best_iou_index[0]][1], frame_index)
                person_1["bbox"].append(person_in_frame[best_iou_index[0]][2])
        
        
    return person_1, person_2


def animation(p1, p2, total_frames):
    keypoints_1 = p1["keypoints"]
    keypoints_2 = p2["keypoints"]

    fig, ax = plt.subplots()
    ax.set(xlim=(0, 900), ylim=(-600, 0))
    t = np.linspace(0, total_frames, total_frames)

    data_1 = np.c_[[x[0][0] for x in keypoints_1.values()], [y[1][0] for y in keypoints_1.values()]]
    data_2 = np.c_[[x[0][0] for x in keypoints_2.values()], [y[1][0] for y in keypoints_2.values()]]

    scatter_1 = ax.scatter(data_1[:,0], -data_1[:,1], c='red', vmin=0, vmax=total_frames)
    scatter_2 = ax.scatter(data_2[:,0], -data_2[:,1], c='blue', vmin=0, vmax=total_frames)

    def animate(i):
        scatter_1.set_offsets(np.c_[[x[0][i] for x in keypoints_1.values()], [-y[1][i] for y in keypoints_1.values()]])
        scatter_2.set_offsets(np.c_[[x[0][i] for x in keypoints_2.values()], [-y[1][i] for y in keypoints_2.values()]])

        return scatter_1 , scatter_2

    anim = FuncAnimation(fig, animate, frames=total_frames, interval=10)
    plt.show()



if __name__ == "__main__":
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("usage_hint")
            exit(0)
        # read arguments
        directory = sys.argv[1]
        total_frames = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    except Exception as e:
        print(e)
        print("usage_hint")
        exit(1)
    
    p1, p2 = get_keypoints_openpose(directory, total_frames)

    print(p1["keypoints"]["Nose"].shape)
    print(p2["keypoints"]["Nose"].shape)

    animation(p1, p2, total_frames)