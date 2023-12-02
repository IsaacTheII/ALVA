import os
import cv2
import json
import matplotlib.pyplot as plt


# Main function
def main():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # open capture.txt in assets folder and read the txt file
    with open(os.path.join(current_dir, 'assets/pifpaf_output', 'Capture.json'), 'r') as f:
        for line in f:
            obj = json.loads(line)[0]

    # open source image to get aspect ratio
    img = cv2.imread(os.path.join(current_dir, 'assets/pifpaf_output/', 'Capture.png'))
    h, w, c = img.shape
    img_aspect_ratio = w / h

    # slice the array to get the confidence scores 
    keypoints_conf = obj.get('keypoints')
    class_index = obj.get('category_id')
    bounding_box = obj.get('bbox')
    conf_all = obj.get('score')

    # get the x and y values from the keypoints_conf array
    x = [ i for i in keypoints_conf[0::3]]
    y = [-i for i in keypoints_conf[1::3]]
    c = keypoints_conf[2::3]

    # setup the figure and plot
    plt.figure(figsize=(w/100, h/100))
    #plt.axes().set_aspect(1/img_aspect_ratio)

    # plot x and y values to see if the mapping is correct
    plt.scatter(x, y)

    # plot bounding box
    rect = plt.Rectangle((bounding_box[0], -bounding_box[1]), 
                         bounding_box[2], -bounding_box[3], 
                         linewidth=1, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect)

    # Annotate the points,bounding box and for center 
    yoffset = -10
    for i in range(len(x)):
        plt.annotate(i + 1, (x[i], y[i] + yoffset), ha='center', va='top', fontsize=12)

    plt.annotate('Bounding Box - Person', (bounding_box[0], -bounding_box[1] - yoffset))


    # Show the plot
    plt.show()

# Call the main function
if __name__ == '__main__':
    main()

