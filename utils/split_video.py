import os
import sys
import cv2
import numpy as np
import tqdm as tqdm

usage_hint = """
    Description: Takes a video in an splits it horizonaly and verticaly then saves four sepearate videos.
                    The four videos are saved in the output directory with the same name as the source video 
                    with an apendix ("_top_left.mp4", "_top_right.mp4", "_bottom_left.mp4", "_bottom_right.mp4").
                    The output directory is created if it does not exist.

    Usage: python split_video.py <video_file> -o <output_dir> -delete_top_left -delete_top_right -delete_bottom_left -delete_bottom_right>

    Options:
        -h, --help: Show this help message and exit

    Arguments:
        video_file: Path to the video file to redice framerate of
        output_dir: optional, path to the output directory, defaults to the same directory as the source video
        delete_top_left: optional, if set, deletes the top left video
        delete_top_right: optional, if set, deletes the top right video
        delete_bottom_left: optional, if set, deletes the bottom left video
        delete_bottom_right: optional, if set, deletes the bottom right video

    Examples: 
    [1]: Split the video into four videos and save them in the same directory as the source video.
         $ python split_video.py "C:/Users/username/Desktop/video.mp4"
    [2]: Split the video into four videos and save them in the output directory.
         $ python split_video.py "C:/Users/username/Desktop/video.mp4" -o "C:/Users/username/Desktop/output"
    [3]: Split the video into four videos and save them in the same directory as the source video, and delete the top left and bottom right videos.
         $ python split_video.py "C:/Users/username/Desktop/video.mp4" -delete_top_left -delete_bottom_right

"""



def split_video(input_video, output_dir, delete_top_left, delete_top_right, delete_bottom_left, delete_bottom_right):
    # create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # read the video
    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    progress_bar = tqdm.tqdm(total=cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # create the four output videos
    if not delete_top_left:
        top_left = cv2.VideoWriter(os.path.join(output_dir, os.path.splitext(os.path.basename(input_video))[0] + "_top_left.mp4"), cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width/2), int(height/2)))
    if not delete_top_right:
        top_right = cv2.VideoWriter(os.path.join(output_dir, os.path.splitext(os.path.basename(input_video))[0] + "_top_right.mp4"), cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width/2), int(height/2)))
    if not delete_bottom_left:
        bottom_left = cv2.VideoWriter(os.path.join(output_dir, os.path.splitext(os.path.basename(input_video))[0] + "_bottom_left.mp4"), cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width/2), int(height/2)))
    if not delete_bottom_right:
        bottom_right = cv2.VideoWriter(os.path.join(output_dir, os.path.splitext(os.path.basename(input_video))[0] + "_bottom_right.mp4"), cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width/2), int(height/2)))

    # read frames of source video and save the needed frames to a new array
    while True:
        progress_bar.update()
        is_read, frame = cap.read()
        if not is_read:
            # no further frames to read
            break

        # split and write the frames to the output videos
        if not delete_top_left:
            top_left_frame = frame[0:int(height/2), 0:int(width/2)]
            top_left.write(top_left_frame)
        if not delete_top_right:
            top_right_frame = frame[0:int(height/2), int(width/2):width]
            top_right.write(top_right_frame)    
        if not delete_bottom_left:
            bottom_left_frame = frame[int(height/2):height, 0:int(width/2)]
            bottom_left.write(bottom_left_frame)
        if not delete_bottom_right:
            bottom_right_frame = frame[int(height/2):height, int(width/2):width]
            bottom_right.write(bottom_right_frame)

    # release input and output video objects
    cap.release()
    if not delete_top_left:
        top_left.release()
    if not delete_top_right:
        top_right.release()
    if not delete_bottom_left:
        bottom_left.release()
    if not delete_bottom_right:
        bottom_right.release()


if __name__ == "__main__":
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(usage_hint)
            exit(0)
        # read arguments
        video_file = sys.argv[1]
        output_dir = sys.argv[3] if sys.argv[2] in ["-o", "-output"] else os.path.dirname(video_file)
        delete_top_left = True if "-delete_top_left" in sys.argv or "-delete_top" in sys.argv else False
        delete_top_right = True if "-delete_top_right" in sys.argv or "-delete_top" in sys.argv  else False
        delete_bottom_left = True if "-delete_bottom_left" in sys.argv or "-delete_bottom" in sys.argv  else False
        delete_bottom_right = True if "-delete_bottom_right" in sys.argv or "-delete_bottom" in sys.argv  else False

        print(delete_bottom_left, delete_bottom_right, delete_top_left, delete_top_right)


    except  Exception as e:
        print(e)
        print(usage_hint)
        exit(1)

    split_video(video_file, output_dir, delete_top_left, delete_top_right, delete_bottom_left, delete_bottom_right)
