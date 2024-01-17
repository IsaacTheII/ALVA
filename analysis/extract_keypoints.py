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

    # Intersection area ( + 1 to account for touching edges)
    intersection_area = max(0, x_right - x_left + 1) * max(0, y_bottom - y_top + 1)

    # Union Area ( + 1 to account for touching edges)
    bb1_area = (x_max_1 - x_min_1 + 1) * (y_max_1 - y_min_1 + 1)
    bb2_area = (x_max_2 - x_min_2 + 1) * (y_max_2 - y_min_2 + 1)
    union_area = (bb1_area + bb2_area) - intersection_area

    return intersection_area / union_area


def get_keypoints_openpose(directory):
    
    # Construct the path to the openpose_output directory
    openpose_output_dir = directory

    # List the files in the directory
    files = os.listdir(openpose_output_dir)

    # check if there are any files other then json files
    for file in files:
        if not file.endswith(".json"):
            files.remove(file)
            print(f"Removed {file} from the list of files processed.")    
    
    # total number of json-files/frames
    total_frames = len(files)
    
    # List of people in the video
    person_1 = np.empty((25, 2, total_frames))
    person_1.fill(np.nan)
    person_1_bbox = np.empty((4, total_frames))
    person_1_bbox.fill(np.nan)
    person_1_bbox_last = [0, 0, 0, 0]

    person_2 = np.empty((25, 2, total_frames))
    person_2.fill(np.nan)
    person_2_bbox = np.empty((4, total_frames))
    person_2_bbox.fill(np.nan)
    person_2_bbox_last = [0, 0, 0, 0]


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
            iou_person_1 = calculate_iou(bbox, person_1_bbox_last)

            # calculate the iou with the person_2
            iou_person_2 = calculate_iou(bbox, person_2_bbox_last)

            # store the iou values in best_iou
            best_iou[person_index, 0] = iou_person_1
            best_iou[person_index, 1] = iou_person_2
        
        # choose the best iou in the best_iou array and add the keypoints to the person_1 or person_2 then set all values to zero for that row.
        if len(person_in_frame) == 0:
            continue
        elif len(person_in_frame) == 1:
            if best_iou[0, 0] > best_iou[0, 1]:
                person_1[:, :, frame_index] = np.array([person_in_frame[0][0], person_in_frame[0][1]]).T
                person_1_bbox[:, frame_index] = np.array(person_in_frame[0][2])
                person_1_bbox_last = person_in_frame[0][2]
            else:
                person_2[:, :, frame_index] = np.array([person_in_frame[0][0], person_in_frame[0][1]]).T
                person_2_bbox[:, frame_index] = np.array(person_in_frame[0][2])
                person_2_bbox_last = person_in_frame[0][2]
        else:
            # get the index absolute best iou in best_iou array
            best_iou_index = np.unravel_index(np.argmax(best_iou, axis=None), best_iou.shape)
            if best_iou_index[1] == 0:
                # add the keypoints to the person_1
                person_1[:, :, frame_index] = np.array([person_in_frame[best_iou_index[0]][0], person_in_frame[best_iou_index[0]][1]]).T
                person_1_bbox[:, frame_index] = np.array(person_in_frame[best_iou_index[0]][2])
                person_1_bbox_last = person_in_frame[best_iou_index[0]][2]
                
                # set the best iou to zero for the column of person_1 and row of person_in_frame
                best_iou[best_iou_index[0], :] = 0
                best_iou[:, best_iou_index[1]] = 0

                # get the best iou index again  and add the keypoints to the person_2
                best_iou_index = np.unravel_index(np.argmax(best_iou, axis=None), best_iou.shape)
                person_2[:, :, frame_index] = np.array([person_in_frame[best_iou_index[0]][0], person_in_frame[best_iou_index[0]][1]]).T
                person_2_bbox[:, frame_index] = np.array(person_in_frame[best_iou_index[0]][2])
                person_2_bbox_last = person_in_frame[best_iou_index[0]][2]
            else:
                # add the keypoints to the person_2
                person_2[:, :, frame_index] = np.array([person_in_frame[best_iou_index[0]][0], person_in_frame[best_iou_index[0]][1]]).T
                person_2_bbox[:, frame_index] = np.array(person_in_frame[best_iou_index[0]][2])
                person_2_bbox_last = person_in_frame[best_iou_index[0]][2]

                # set the best iou to zero for the column of person_2 and row of person_in_frame
                best_iou[best_iou_index[0], :] = 0
                best_iou[:, best_iou_index[1]] = 0

                # get the best iou index again  and add the keypoints to the person_1
                best_iou_index = np.unravel_index(np.argmax(best_iou, axis=None), best_iou.shape)
                person_1[:, :, frame_index] = np.array([person_in_frame[best_iou_index[0]][0], person_in_frame[best_iou_index[0]][1]]).T
                person_1_bbox[:, frame_index] = np.array(person_in_frame[best_iou_index[0]][2])
                person_1_bbox_last = person_in_frame[best_iou_index[0]][2]

    # differentiate between child and therapist by the average size of the bounding box
    person_1_bbox_avg = np.nanmean((person_1_bbox[2, :] - person_1_bbox[0, :]) * (person_1_bbox[3, :] - person_1_bbox[1, :]))
    person_2_bbox_avg = np.nanmean((person_2_bbox[2, :] - person_2_bbox[0, :]) * (person_2_bbox[3, :] - person_2_bbox[1, :]))

    if person_1_bbox_avg > person_2_bbox_avg:
        child, therapist, child_bbox, therapist_bbox = person_2, person_1, person_2_bbox, person_1_bbox
    else:
        child, therapist, child_bbox, therapist_bbox = person_1, person_2, person_1_bbox, person_2_bbox
    
    # return the keypoints of the child and therapist and their bounding boxes
    return child, therapist, child_bbox, therapist_bbox


def animation(p1, p2):

    # setup the figure and plot
    fig, ax = plt.subplots()
    ax.set(xlim=(0, 900), ylim=(-600, 0))

    # count the total number of frames
    total_frames = p1.shape[2]

    # flip the sign of the y axis
    p1[:, 1, :] = -p1[:, 1, :]
    p2[:, 1, :] = -p2[:, 1, :]

    scatter_1 = ax.scatter(p1[:,0,0], p1[:,1,0], c='red', vmin=0, vmax=total_frames)
    scatter_2 = ax.scatter(p2[:,0,0], p2[:,1,0], c='blue', vmin=0, vmax=total_frames)

    def animate(i):
        scatter_1.set_offsets(p1[:, :, i])
        scatter_2.set_offsets(p2[:, :, i])

        return scatter_1 , scatter_2

    anim = FuncAnimation(fig, animate, frames=total_frames, interval=100)
    plt.show()



if __name__ == "__main__":
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("usage_hint")
            exit(0)
        # read arguments
        directory = sys.argv[1]

    except Exception as e:
        print(e)
        print("usage_hint")
        exit(1)
    
    child, therapist, child_bbox, therapist_bbox = get_keypoints_openpose(directory)

    animation(child, therapist)

    