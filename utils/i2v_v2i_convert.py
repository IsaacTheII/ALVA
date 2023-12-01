import os
import sys
import cv2
import numpy as np
import tqdm as tqdm

useage_hint = """
    Description: This script takes a name and either a video file and converts it to a set of images or a directory with images and converts it to a video.
    The output is saved in the same directory under a given name as the input files.

    Useage: python i2v_v2i_convert.py <input_file_directory> <name> -fps <fps>

    Arguments:
        input_file_directory: Path to the input file or directory
        name: Name of the output files (for video, name.mp4 and for images, name_1.jpg, name_2.jpg, ...)
        fps: optional, fps of the video. Default is 30
    Example:
        [1]: Convert a video file to a set of images
                $ python i2v_v2i_convert.py "C:/Users/username/Desktop/video.mp4" "new_images"
        [2]: Convert a directory with images to a video file
                $ python i2v_v2i_convert.py "C:/Users/username/Desktop/images/" "new_video"
        [3]: Convert a directory with images to a video file with 60 fps
                $ python i2v_v2i_convert.py "C:/Users/username/Desktop/images/" "new_video" -fps 60
    
    """

def convert(input_file_directory, name, fps=30):
    if os.path.isfile(input_file_directory):
        # convert video to images
        print("Converting video to images...")
        cap = cv2.VideoCapture(input_file_directory)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Total number of frames: ", total_frames)
        print("FPS: ", fps)
        print("Converting...")
        for i in tqdm.tqdm(range(int(total_frames))):
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(os.path.join(os.path.dirname(input_file_directory), name + "frame_" + str(i) + ".jpg"), frame)
        print("Done!")
    elif os.path.isdir(input_file_directory):
        # convert images to video
        print("Converting images to video...")
        image_files = os.listdir(input_file_directory)
        image_files.sort()
        print("Total number of images: ", len(image_files))
        print("Converting...")
        img_array = []
        for filename in tqdm.tqdm(image_files):
            if filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
                print("Skipping file: ", filename)
                continue
            img = cv2.imread(os.path.join(input_file_directory, filename))
            img_array.append(img)
        height, width, layers = img_array[0].shape
        size = (width,height)
        out = cv2.VideoWriter(os.path.join(os.path.dirname(input_file_directory), name + ".mp4"),cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        print("Done!")

if __name__ == "__main__":
    try:
        # parse the arguments
        input_file_directory = sys.argv[1]
        name = sys.argv[2]

        # parse optionall arguments
        fps = 1
        if "-fps" in sys.argv:
            fps = sys.argv[sys.argv.index("-fps") + 1]

    except Exception as e:
        print(e)
        print("Please provide a video file or a directory with images as an argument.")
        print(useage_hint)
        exit(1)
    convert(input_file_directory, name, fps)