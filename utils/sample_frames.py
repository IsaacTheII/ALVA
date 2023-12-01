import os
import sys
import cv2
import numpy as np
import tqdm as tqdm

useage_hint = """
    Description: This script should take a video file, N number of frames to be sampled, an output directory and optionaly a start and end time. Then it 
     should sample the video between the start and end time N times. And save the frames in the output directory.

    Useage: python sample_frames.py <video_file> <number_of_frames> -o <output_directory> -start <start_time> -end <end_time>

    Options:
        -h, --help: Show this help message and exit
        -start, --start_time: Start time of the clip in seconds
        -end, --end_time: End time of the clip in seconds

    Arguments:
        video_file: Path to the video file to sample frames from
        number_of_frames: Number of frames to sample
        output_directory: Path to the output directory to save the frames to. Default is the same directory as the source video
        start_time: optional, start time of the clip in seconds
        end_time: optional, end time of the clip in seconds

    Example: 
        [1]: Sample 10 frames from the video and save them in the output directory.
                $ python sample_frames.py "C:/Users/username/Desktop/video.mp4" 10 "C:/Users/username/Desktop/output/"
        [2]: Sample 5 frames from the video between the start and end time and save them in the output directory.
                $ python sample_frames.py "C:/Users/username/Desktop/video.mp4" 5 "C:/Users/username/Desktop/output/" -start 00:00:05 -end 00:00:10
    
    """


def sample_frames(input_video, number_of_frames, output_dir, start_time, end_time):
    # create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # read the video
    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)


    # get the start and end frame
    start_frame = start_time * fps
    end_frame = end_time * fps

    # get the total number of frames
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # check if end time is inf and set it to the total number of frames
    if end_frame == float("inf"):
        end_frame = total_frames

    # check if the start and end frame are valid and if there are N frames between the start and end frame
    if start_frame > total_frames:
        print("Start time is greater than the total video length.")
        exit()
    if end_frame > total_frames:
        print("End time is greater than the total video length.")
        exit()
    if number_of_frames > end_frame - start_frame - 2:
        number_of_frames = end_frame - start_frame - 2
        print("Number of frames is greater than the number of frames between the start and end time. \n\
              Only sampling {} frames.".format(number_of_frames))
    
    # calculate the frames to sample and evenly space them between the start and end frame not including the start and end frame
    frames_to_sample = np.linspace(start_frame, end_frame, number_of_frames + 2, dtype=int)[1:-1]

    # create a progress bar
    progress_bar = tqdm.tqdm(total=frames_to_sample[-1])

    # set up the counter and check if previous frames have been sampled if so increment the counter to get to a open range of frames
    count = 1 
    while os.path.exists(os.path.join(output_dir, os.path.basename(input_video).split(".")[0] + "_frame_{}.jpg".format(count))):
        count += 1
        number_of_frames += 1

    # read the video and write the frames to the output directory
    while cap.isOpened():
        progress_bar.update(1)
        ret, frame = cap.read()
        if ret:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) in frames_to_sample:
                cv2.imwrite(os.path.join(output_dir, os.path.basename(input_video).split(".")[0] + "_frame_{}.jpg".format(count)), frame)
                count += 1
            if count > number_of_frames:
                break
        else:
            # no more frames to read
            break
    
    cap.release()
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
    if "-h" in sys.argv or "--help" in sys.argv:
        print(useage_hint)
        exit(0)
    try:
        # parse arguments
        if len(sys.argv) < 4:
            print(useage_hint)
            sys.exit(0)

        video_file = sys.argv[1]
        number_of_frames = int(sys.argv[2])
        output_dir = os.path.dirname(video_file)

        # parse optional arguments output directory if it is provided
        if "-o" in sys.argv:
            output_dir = sys.argv[sys.argv.index("-o") + 1]
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

        # parse optional arguments start and end time if they are provided
        start_time = parse_time(sys.argv[sys.argv.index("-start") + 1]) if "-start" in sys.argv else 0.0
        end_time = parse_time(sys.argv[sys.argv.index("-end") + 1]) if "-end" in sys.argv else float("inf")

    
    except Exception as e:
        print(e)
        print(useage_hint)
        exit(1)
    
    sample_frames(video_file, number_of_frames, output_dir, start_time, end_time)

