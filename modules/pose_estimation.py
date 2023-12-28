import sys
import os
import argparse
import subprocess

from ultralytics import YOLO

from dotenv import load_dotenv

# set up the environment variables
load_dotenv()
env = os.environ


def extract_pose(src, show_bool=False, save_bool=True, save_txt_bool=True, save_conf_bool=False):

    # configure the model
    #model = YOLO('./models/yolov8n-pose.pt')
    model = YOLO('./models/yolov8x-pose.pt')
    #model = YOLO('./models/yolov8x-pose-p6.pt')

    # run the model on the gpu
    model.to('cuda')

    # execute the prediciton on the video
    results = model(source=src, show=show_bool, save=save_bool, save_txt=save_txt_bool, save_conf=save_conf_bool)

def extract_pose_openpose(src):
    try:
        print(
            [env["PATH_TO_OPENPOSE"] + "bin\OpenPoseDemo.exe", 
                        "--video", src, 
                        "--write_json", "./runs/openpose/", 
                        "--write_video", os.path.splitext(src)[0] + "_openpose.avi",
                        "--display", "0", ]
        )
        # execute the prediciton on the video
        subprocess.run([env["PATH_TO_OPENPOSE"] + "bin\OpenPoseDemo.exe", 
                        "--video", src, 
                        "--write_json", "./runs/openpose/", 
                        "--write_video", os.path.splitext(src)[0] + "_openpose.avi",
                        "--display", "0", ])
        #subprocess.run(["./openpose/build/examples/openpose/openpose.bin", "--video", src, "--write_json", "./runs/openpose/", "--display", "0", "--render_pose", "0", "--number_people_max", "1"])
    except:
        print("OpenPose is not properly installed or not in the correct directory. Please follow the instructions in the README.md to install OpenPose.")    

    

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
    parser.add_argument("--show", action="store_true", help="show the output video in a new window")
    parser.add_argument("--save", action="store_true", help="save the output video")
    parser.add_argument("--save_text", action="store_true", help="save the output of the pose estimation in a text file")
    parser.add_argument("--save_conf", action="store_true", help="save the confidence of the pose estimation in the results object for further processing")

    # catch no arguments
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    main(args)

