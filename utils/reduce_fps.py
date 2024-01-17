from datetime import timedelta
import cv2
import numpy as np
import os
import sys
import tqdm

usage_hint = """
    Description: Reduces the framerate of a video file using OpenCV and saves the new video with the new fps as 
                 a copy with an apendix ("_[new_fps]_fps.mp4") in a new mp4 file.

    Usage: python ./reduce_fps.py [Options] <path_to_video> <frames_per_second>

    Options:
        -h, --help: Show this help message and exit

    Arguments:
        path_to_video: Path to the video file to redice framerate of
        frames_per_second: How many frames per second to save, if not given, defaults to 1 frame per second

    Examples: 
    [1]: Reduce the framerate to 1 frame per second.
         $ python reduce_fps.py "C:/Users/username/Desktop/video.mp4"
    [2]: Reduces the framerate to 15 frames per second.
         $ python reduce_fps.py "C:/Users/username/Desktop/video.mp4" 15
"""


def reduce_fps(input_video, new_fps, callback=False):

    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # check if the desired fps is smaller than the source fps other wise use source fps
    new_fps = fps if new_fps>=fps else new_fps
    
    # create a linspace of frame posisiton of the source video and sample it at the new framerate then extrapolate the frame indices to be saved.
    frames_to_save = (np.arange(0, cap.get(cv2.CAP_PROP_FRAME_COUNT)/fps, 1 / new_fps ) * fps).astype(int)

    # setup progress bar
    pbar = tqdm.tqdm(total=len(frames_to_save), desc="Reducing FPS", unit="frames")

    # new file name
    filename, _ = os.path.splitext(input_video)
    filename += "_%d_fps.mp4"%(new_fps)

    # save the new_frames into a new video
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), new_fps, (int(cap.get(3)), int(cap.get(4))))

    # read frames of source video and save the needed frames to a new array
    count = 0
    while True:
        count += 1
        is_read, frame = cap.read()
        if not is_read:
            # no further frames to read
            break
        if count in frames_to_save:
            pbar.update(1)
            # save the frames with the correct indices 
            out.write(frame) 

    # release input and output video objects
    cap.release()
    out.release()

    # if this function has been called from a diffrent script then optionaly return the new filename
    if callback:
        return filename
        

if __name__ == "__main__":
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(usage_hint)
            exit(0)
        # read arguments
        video_file = sys.argv[1]
        fps_to_save = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    except IndexError:
        print(usage_hint)
        exit(1)

    reduce_fps(video_file, fps_to_save)