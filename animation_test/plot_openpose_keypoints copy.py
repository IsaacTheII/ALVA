import os
import cv2
import json
import matplotlib.pyplot as plt


# Main function
def main():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    # setup the figure and plot
    plt.figure(figsize=(10, 10))

    # read the keypoints from the file
    with open(f".\\runs\openpose\\Sirius_Intensiv_Spiel_1A_repetitive_0_anonymized_1_fps_000000000510_keypoints.json", 'r') as f:
        json_object = json.load(f)

        # Get the people array from the json object
        people = json_object['people']

        # read the keypoints for each person in the frame and store in a person list of current frame
        for person in people:
            # Get the pose_keypoints_2d array from the person object
            pose_keypoints_2d = person['pose_keypoints_2d']


            # get the x and y values from the keypoints_conf array
            x = [ i for i in pose_keypoints_2d[0::3]]
            y = [-i for i in pose_keypoints_2d[1::3]]
            c = pose_keypoints_2d[2::3]

            bounding_box = [min(x), min(y), max(x), max(y)]


            # plot x and y values to see if the mapping is correct
            plt.scatter(x, y)

            # plot bounding box
            #rect = plt.Rectangle((bounding_box[0] - bounding_box[2] * .5 , -bounding_box[1] - bounding_box[3] * .5), bounding_box[2], bounding_box[3], linewidth=1, edgecolor='r', facecolor='none')
            rect = plt.Rectangle((bounding_box[0], bounding_box[1]), bounding_box[2] - bounding_box[0], bounding_box[3] - bounding_box[1], linewidth=1, edgecolor='r', facecolor='none')
            plt.gca().add_patch(rect)
            plt.plot(bounding_box[0], bounding_box[1], 'ro')

    
    # Show the plot
    plt.show()

# Call the main function
if __name__ == '__main__':
    main()

