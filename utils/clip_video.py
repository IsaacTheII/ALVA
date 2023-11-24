import os
import sys
import cv2
import numpy as np
import tqdm as tqdm

useage_hint = """
    Description: Takes a video and a start and end time and saves a clip of the video between the start and end time to a new video file.
                 The new video file is saved in the same directory as the source video with an apendix ("_clip.mp4").

    Usage: python clip_video.py <video_file> <start_time> <end_time> <output_filename> -o <output_dir>

    Options:
        -h, --help: Show this help message and exit
        -o, --output_dir: Path to the output directory, defaults to the same directory as the source video

    Arguments:
        video_file: Path to the video file to redice framerate of
        start_time: Start time of the clip in format hh:mm:ss
        end_time: End time of the clip in format hh:mm:ss
        output_filename: Name of the output video file, if none given then the ouput file will have the same name as the source video with an apendix ("_clip.mp4")
        output_dir: optional, path to the output directory, defaults to the same directory as the source video

    Examples:
    [1]: Clip the video and save it in the same directory as the source video.
         $ python clip_video.py "C:/Users/username/Desktop/video.mp4" 00:10:00 00:20:00
    [2]: Clip the video and save it in the output directory.
         $ python clip_video.py "C:/Users/username/Desktop/video.mp4" 00:10:00 00:20:00 -o "C:/Users/username/Desktop/output"

"""


def clip_video(input_video, start_time, end_time, output_filename, output_dir):
    # create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # read the video
    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    progress_bar = tqdm.tqdm(total=cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # create the output video
    output = cv2.VideoWriter(os.path.join(output_dir, output_filename), cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # skip to the start time
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_time * fps)

    # read the video and write the frames to the output video
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            output.write(frame)
            progress_bar.update(1)
        else:
            # no more frames to read
            break

        if cap.get(cv2.CAP_PROP_POS_FRAMES) >= end_time * fps:
            break

    cap.release()
    output.release()
    cv2.destroyAllWindows()


def parse_time(time):
    # check if the time is the string "start" or "end"
    if time.lower() == "start":
        return 0.0
    if time.lower() == "end":
        return float("inf")
    
    # check if the time is in the format hh:mm:ss
    if len(time.split(":")) != 3:
        print(useage_hint)
        print("Please provide the time in the format hh:mm:ss")
        exit(1)

    # try to parse the time and catch any errors
    try:
        # check if the time is a valid time
        time = time.split(":")
        seconds = 0
        for i, t in enumerate(time[::-1]):
            seconds += float(t) * 60 ** i
    
    except Exception as e:
        print(e)
        print(useage_hint)
        print("Please provide a valid time in the format hh:mm:ss")
        exit(1)
    
    return seconds


if __name__ == "__main__":
    print(sys.argv)
    try:
        # parse arguments
        if len(sys.argv) < 4:
            print(useage_hint)
            sys.exit(0)

        input_video = sys.argv[1]
        start_time = parse_time(sys.argv[2])
        end_time = parse_time(sys.argv[3])
        output_filename = os.path.splitext(os.path.basename(input_video))[0] + "_clip.mp4"
        output_dir = os.path.dirname(input_video)

        if len(sys.argv) > 4 and sys.argv[4] != "-o":
            output_filename = os.path.splitext(os.path.basename(sys.argv[4]))[0]

        if len(sys.argv) > 5 and "-o" in sys.argv:
            if sys.argv[5] == "-o":
                output_dir = sys.argv[6]
            elif sys.argv[4] == "-o":
                output_dir = sys.argv[5]
    
    except Exception as e:
        print(e)
        print(useage_hint)
        exit(1)
    
    clip_video(input_video, start_time, end_time, output_filename, output_dir)
    