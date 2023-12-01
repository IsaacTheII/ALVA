import sys
import os
import subprocess

from ultralytics import YOLO

from dotenv import load_dotenv

# set up the environment variables
load_dotenv()
env = os.environ




def main(src):
    try:
        # set the output directory
        output_dir = os.path.join(os.path.dirname(__file__), "assets/openpose_output")

        # execute the prediction on the video
        subprocess.run([env["PATH_TO_OPENPOSE"] + "bin\OpenPoseDemo.exe", 
                        "--video", src, 
                        "--write_json", output_dir, 
                        "--render_pose", "0",
                        "--display", "0"])
    except Exception as e:
        print(e)
        print("OpenPose is not properly installed or not in the correct directory. Please follow the instructions in the README.md to install OpenPose.")    


if __name__ == "__main__":
    # get video location and run the pose estimation
    try:
        src_vid = sys.argv[1]
    except Exception as e:
        print(e)
        print("Please provide a video file as an argument.")

    main(src_vid)

