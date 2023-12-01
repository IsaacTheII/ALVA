import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

# Get the directory of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))


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
    series1 = calculate_confidenceseries_pifpaf()
    #series4 = utility_function_4()

    # Plot the series using matplotlib
    plt.plot(smooth_mov_avg_mask(series1, 100), label='Pifpaf')

    #plt.plot(series4, label='Series 4')

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

