import sys
import argparse
import subprocess

from ultralytics import YOLO


def extract_pose(src, show_bool=False, save_bool=True, save_txt_bool=True, save_conf_bool=False):

    # configure the model
    model = YOLO('./models/yolov8n-pose.pt')

    # run the model on the gpu
    model.to('cuda')

    # execute the prediciton on the video
    results = model(source=src, show=show_bool, save=save_bool, save_txt=save_txt_bool, save_conf=save_conf_bool)


def main(args):
    # run the pose estimation
    if args.video_in:
        extract_pose(args.video_in, show_bool=args.show, save_bool=args.save, save_txt_bool=args.save_text, save_conf_bool=args.save_conf)
    


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="pose_estimation.py",
        description="This script will run YOLOv8 pose estimation on a video file and save the results in a new foler called './runs/' in the current directory.",
        epilog="For more information visit: https://github.com/ultralytics/ultralytics",)

    parser.add_argument("--video_in", type=str, default=0, help="path to the video / image / 0 for webcam stream")
    parser.add_argument("--show", action="store_true", help="show the output video in a new up window")
    parser.add_argument("--save", action="store_true", help="save the output video")
    parser.add_argument("--save_text", action="store_true", help="save the output of the pose estimation in a text file")
    parser.add_argument("--save_conf", action="store_true", help="save the confidence of the pose estimation in the results object for further processing")

    # catch no arguments
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    main(args)

