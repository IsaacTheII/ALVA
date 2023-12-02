import os
import cv2
import matplotlib.pyplot as plt


# Main function
def main():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # open capture.txt in assets folder and read the txt file
    with open(os.path.join(current_dir, 'assets/yolo_nano_output/labels', 'Capture.txt'), 'r') as f:
        line = f.read().splitlines()[0]
        array = line.split(' ')
        array = [float(i) for i in array]

    # open source image to get aspect ratio
    img = cv2.imread(os.path.join(current_dir, 'assets/yolo_nano_output/', 'Capture.png'))
    h, w, c = img.shape
    img_aspect_ratio = w / h

    # slice the array to get the confidence scores 
    keypoints_conf = array[5:-1]
    class_index = array[:1]
    bounding_box = array[1:5]
    conf_all = array[-1]

    # get the x and y values from the keypoints_conf array
    x = [ i for i in keypoints_conf[0::3]]
    y = [-i for i in keypoints_conf[1::3]]
    c = keypoints_conf[2::3]

    # setup the figure and plot
    plt.figure(figsize=(12, 12 * img_aspect_ratio))
    plt.axes().set_aspect(1/img_aspect_ratio)
    plt.xlim(0, 1)
    plt.ylim(-1, 0)

    # plot x and y values to see if the mapping is correct
    plt.scatter(x, y)

    # plot bounding box
    rect = plt.Rectangle((bounding_box[0] - bounding_box[2] * .5 , -bounding_box[1] - bounding_box[3] * .5), bounding_box[2], bounding_box[3], linewidth=1, edgecolor='r', facecolor='none')
    #rect = plt.Rectangle((bounding_box[0], -bounding_box[1]), bounding_box[2], bounding_box[3], linewidth=1, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect)
    plt.plot(bounding_box[0], -bounding_box[1], 'ro')

    # Annotate the points,bounding box and for center 
    xoffset = 0.01
    yoffset = 0.01
    for i in range(len(x)):
        plt.annotate(i + 1, (x[i], y[i] + yoffset), ha='center')

    plt.annotate('Center', (bounding_box[0], -bounding_box[1] + yoffset), ha='center')

    plt.annotate('Bounding Box - Person', (bounding_box[0] - bounding_box[2] * .5 +xoffset, -bounding_box[1] - bounding_box[3] * .5 + yoffset))


    # Show the plot
    plt.show()

# Call the main function
if __name__ == '__main__':
    main()

