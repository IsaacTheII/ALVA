import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

# Get the directory of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))


# goes through the openpose output files and calculates the confidence scores for each frame
def calculate_confidenceseries_openpose_1080p():
    conf_series = []

    # Construct the path to the openpose_output directory
    openpose_output_dir = os.path.join(current_dir, 'assets', 'openpose_output_1080p')

    # List the files in the directory
    files = os.listdir(openpose_output_dir)

    for file, i in zip(files, range(len(files))):
        if not i%5 == 0:
            continue
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
def calculate_confidenceseries_openpose_720p():
    conf_series = []

    # Construct the path to the openpose_output directory
    openpose_output_dir = os.path.join(current_dir, 'assets', 'openpose_output_720p')

    # List the files in the directory
    files = os.listdir(openpose_output_dir)

    for file, i in zip(files, range(len(files))):
        if not i%5 == 0:
            continue
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


# Utility function 3
def calculate_confidenceseries_openpose_original():
    conf_series = []

    # Construct the path to the openpose_output directory
    openpose_output_dir = os.path.join(current_dir, 'assets', 'openpose_output_original')

    # List the files in the directory
    files = os.listdir(openpose_output_dir)

    for file, i in zip(files, range(len(files))):
        
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

# goes through the pifpaf output files and calculates the confidence scores for each frame
def calculate_confidenceseries_openpose_480p():
    conf_series = []

    # Construct the path to the openpose_output directory
    openpose_output_dir = os.path.join(current_dir, 'assets', 'openpose_output_480p')

    # List the files in the directory
    files = os.listdir(openpose_output_dir)

    for file, i in zip(files, range(len(files))):
        if not i%5 == 0:
            continue
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

def smooth_mov_avg_mask(y, mask_size):
    # account for the mask size
    pad_size = mask_size//2
    y = np.pad(y, pad_size, mode='wrap')

    # remove the None values from the list
    y_tmp = [i for i in y if i is not None]

    mask = np.ones(mask_size)/mask_size
    smooth_mov_avg = np.convolve(y_tmp, mask, mode='same').tolist()

    # add the None values back to the list
    smooth_mov_avg = [None if i is None else smooth_mov_avg.pop(0) for i in y]

    return smooth_mov_avg[pad_size:-pad_size]

# Main function
def main():
    fig, ax = plt.subplots()

    # Call the utility functions
    high_quality = calculate_confidenceseries_openpose_1080p()
    medium_quality = calculate_confidenceseries_openpose_720p()
    ref_quality = calculate_confidenceseries_openpose_original()
    #low_quality = calculate_confidenceseries_openpose_480p()

        # Replace None values with np.nan

    r_high = [np.nan if i is None else i for i in smooth_mov_avg_mask(high_quality,80)]
    r_medium = [np.nan if i is None else i for i in smooth_mov_avg_mask(medium_quality,80)]
    r_ref = [np.nan if i is None else i for i in smooth_mov_avg_mask(ref_quality,80)]

    # Print range
    print("High quality range: ", min(r_high) - max(r_high), min(r_high), max(r_high))
    print("Medium quality range: ", min(r_medium) - max(r_medium), min(r_medium), max(r_medium))
    print("Reference quality range: ", min(r_ref) - max(r_ref), min(r_ref), max(r_ref))

    # Plot the series using matplotlib
    ax.plot(smooth_mov_avg_mask(high_quality, 80), label='1920x1080', linewidth=2)
    ax.plot(smooth_mov_avg_mask(medium_quality, 80), label='1280x720', linewidth=2)
    #ax.plot(smooth_mov_avg_mask(low_quality, 80), label='864x480', linewidth=2)
    ax.plot(smooth_mov_avg_mask(ref_quality, 80), label='720x576 - reference', linewidth=2)

    # Set styling 
    font = 20
    plt.rcParams.update({'font.size': font})

    # Generate evenly spaced values for the x-axis
    frames = np.linspace(0, len(ref_quality), num=8)

    # Convert frames to minutes and seconds format
    ticks = ['{:02d}:{:02d}'.format(int(frame/5) // 60, int(frame/5) % 60) for frame in frames]

    # Set the x-axis tick labels
    ax.set_xticks(frames)
    ax.set_xticklabels(ticks, fontsize=font*0.6)  # Increase the fontsize to your desired value

    # Add title, axis labels and legend
    ax.set_title('Confidence and Stability of OpenPose with Higher Quality Videos',{'size': font})
    ax.set_ylabel('Confidence score',{'size': font})
    ax.set_xlabel('Time (min:sec)',{'size': font})
    ax.set_ylim([0, 1])
    ax.legend()


    # Show the plot
    plt.show()

# Call the main function
if __name__ == '__main__':
    main()
