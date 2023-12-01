import sys
import os
import pandas as pd
import json

from ultralytics import YOLO

from dotenv import load_dotenv

# set up the environment variables
load_dotenv()
env = os.environ

def main(src):

    # configure the nano model called yolov8n-pose.pt
    model = YOLO('./models/yolov8n-pose.pt')

    # run the model on the gpu
    model.to('cuda')

    # clear the output directory
    try:
        os.remove(os.path.join(os.path.dirname(__file__), "assets/yolo_nano_output"))
    except Exception as e:
        print(e)
        print("Could not remove the output directory. Make sure it is empty.")

    #get current directory and set the output directory to set them in the model prediction function 
    # as project and name fields. This will save the results in the output directory
    current_dir = os.path.dirname(__file__)
    output_dir = "assets/yolo_nano_output"

    # execute the prediciton on the video
    results = model(source=src, 
                    project=current_dir, 
                    name=output_dir, 
                    show=False, 
                    save=True, 
                    save_txt=True, 
                    save_conf=True)



if __name__ == "__main__":
    # get video location and run the pose estimation
    try:
        src_vid = sys.argv[1]
    except Exception as e:
        print(e)
        print("Please provide a video file as an argument.")

    main(src_vid)
