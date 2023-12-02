import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

# Get the directory of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))


# goes through the openpose output files and calculates the confidence scores for each frame
def calculate_confidenceseries_openpose():
    conf_series = []

    # Construct the path to the openpose_output directory
    openpose_output_dir = os.path.join(current_dir, 'assets', 'openpose_output')

    # List the files in the directory
    files = os.listdir(openpose_output_dir)

    for file in files:
        # Construct the path to the file
        file_path = os.path.join(openpose_output_dir, file)

        # Open the json file and read the json object
        with open(file_path, 'r') as f:
            json_object = json.load(f)

            # Get the people array from the json object
            people = json_object['people']

            # read the confidence scores for each person in the frame
            confidence_scores_frame = np.array([])
            for person in people:
                # Get the pose_keypoints_2d aray from the person object
                pose_keypoints_2d = person['pose_keypoints_2d']

                # Get the confidence score from the keypoints. Formate of body25 output: y1, x1, c1, y2, x2, c2, ... , y25, x25, c25
                c = pose_keypoints_2d[2::3]

                # add the confidence scores to the confidence_scores_frame
                confidence_scores_frame = np.append(confidence_scores_frame, c)

        # Append the confidence score to the conf_series list for each frame if there was a person in the frame
        conf_series.append(confidence_scores_frame.mean() if len(confidence_scores_frame) > 0 else None)
    
    return conf_series

# Utility function 2
def calculate_confidenceseries_yolo_extra_large():
    conf_series = []

    # Construct the path to the yolo_extra_large_output directory
    yolo_extra_large_output_dir = os.path.join(current_dir, 'assets', 'yolo_extra_large_output', 'labels')

    # List the files in the directory
    files = os.listdir(yolo_extra_large_output_dir)
    files.sort(key=lambda f: int(f.split('.')[0].split('_')[-1]))

    # check if the file is missing due to missing detection
    count = 1

    for file in files:
        # account for missing frames
        while count < int(file.split('.')[0].split('_')[-1]):
            count += 1
            conf_series.append(None)
        
        # increment the count for current frame
        count += 1

        # Construct the path to the file
        file_path = os.path.join(yolo_extra_large_output_dir, file)

        # Open the txt file and read the lines object
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
            confidence_scores_frame = np.array([])
            for line in lines:
                # split the line into an array
                array = line.split(' ')
                array = [float(i) for i in array]

                # slice the array to get the keypoints and confidence scores 
                keypoints_conf = array[5:-1]

                # get confidence values from the keypoints_conf array
                c = keypoints_conf[2::3]

                # add the confidence scores to the confidence_scores_frame
                confidence_scores_frame = np.append(confidence_scores_frame, c)
        # Append the confidence score to the conf_series list for each frame if there was a person in the frame
        conf_series.append(confidence_scores_frame.mean() if len(confidence_scores_frame) > 0 else None)

    return conf_series


# Utility function 3
def calculate_confidenceseries_yolo_nano():
    conf_series = []

    # Construct the path to the yolo_nano_output directory
    yolo_nano_output_dir = os.path.join(current_dir, 'assets', 'yolo_nano_output', 'labels')

    # List the files in the directory
    files = os.listdir(yolo_nano_output_dir)
    files.sort(key=lambda f: int(f.split('.')[0].split('_')[-1]))

    # counter to check if the file is missing due to missing detection
    count = 1

    for file in files:
        # account for missing frames
        while count < int(file.split('.')[0].split('_')[-1]):
            count += 1
            conf_series.append(None)
        
        # increment the count for current frame
        count += 1

        # Construct the path to the file
        file_path = os.path.join(yolo_nano_output_dir, file)

        # Initialize the confidence_scores_frame array
        confidence_scores_frame = np.array([])
        
        # Open the txt file and read the lines object
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()

            for line in lines:
                # split the line into an array
                array = line.split(' ')
                array = [float(i) for i in array]

                # slice the array to get the keypoints and confidence scores 
                keypoints_conf = array[5:-1]

                # get confidence values from the keypoints_conf array
                c = keypoints_conf[2::3]

                # add the confidence scores to the confidence_scores_frame
                confidence_scores_frame = np.append(confidence_scores_frame, c)
        # Append the confidence score to the conf_series list for each frame if there was a person in the frame
        conf_series.append(confidence_scores_frame.mean() if len(confidence_scores_frame) > 0 else None)
    
    return conf_series

# goes through the pifpaf output files and calculates the confidence scores for each frame
def calculate_confidenceseries_pifpaf():
    conf_series = []

    # Construct the path to the openpose_output directory
    pifpaf_output_dir = os.path.join(current_dir, 'assets', 'pifpaf_output')

    # List the files in the directory
    files = os.listdir(pifpaf_output_dir)

    for file in files:
        # Check if the file is a json file and skip if not
        if not file.endswith(".json"):
            continue

        # Construct the path to the file
        file_path = os.path.join(pifpaf_output_dir, file)

        # Open the json file and read the json object
        with open(file_path, 'r') as f:
            for line_frame in f:
                # Set the confidence score for the frame
                confidence_scores_frame = np.array([])

                # Load the json object that contains the predictions for the frame
                json_object = json.loads(line_frame)

                # Get prediction array from the json object
                predictions = json_object['predictions']

                # loop over all the predictions in the frame
                for prediction in predictions:
                    # get the keypoints array from the prediction object
                    keypoints = prediction['keypoints']

                    # Get the confidence score from the keypoints. Format of pifpaf output: \TODO
                    c = keypoints[2::3]

                    # add the confidence scores to the confidence_scores_frame
                    confidence_scores_frame = np.append(confidence_scores_frame, c)

                # Append the confidence score to the conf_series list for each frame if there was a person in the frame
                conf_series.append(confidence_scores_frame.mean() if len(confidence_scores_frame) > 0 else None)
    
    return conf_series

def smooth_mov_avg_mask(y, mask_size):
    # remove the None values from the list
    y_tmp = [i for i in y if i is not None]

    mask = np.ones(mask_size)/mask_size
    smooth_mov_avg = np.convolve(y_tmp, mask, mode='same').tolist()

    # add the None values back to the list
    smooth_mov_avg = [None if i is None else smooth_mov_avg.pop(0) for i in y]

    return smooth_mov_avg

# Main function
def main():
    # Call the utility functions
    s_openpose = calculate_confidenceseries_openpose()
    s_yolo_x = calculate_confidenceseries_yolo_extra_large()
    s_yolo_n = calculate_confidenceseries_yolo_nano()
    s_pifpaf = calculate_confidenceseries_pifpaf()

    # Plot the series using matplotlib
    plt.plot(smooth_mov_avg_mask(s_openpose, 100), label='Openpose')
    plt.plot(smooth_mov_avg_mask(s_yolo_x, 100), label='YOLOv8 Pose Extra Large')
    plt.plot(smooth_mov_avg_mask(s_yolo_n, 100), label='YOLOv8 Pose Nano')
    plt.plot(smooth_mov_avg_mask(s_pifpaf, 100), label='Pifpaf')

    # Add title, axis labels and legend
    plt.title('Confidence scores for each frame')
    plt.ylabel('Confidence score')
    plt.xlabel('Frame number')
    plt.legend()

    # Show the plot
    plt.show()

# Call the main function
if __name__ == '__main__':
    main()
