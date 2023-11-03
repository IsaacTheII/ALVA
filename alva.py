#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on 17:39:45 Friday 20/10/2023

Author: Simon Padua

Project: ALVA - Automated Learning and Visualization of Autistic Features

Description:
This is the main file of the ALVA project. It is used to call the different modules of the project. And to generate the different assets needed for the visualisation.
To run the project, simply run this file with the following command:
    python3 alva.py --path_in <path_to_video> --path_out <path_to_output> --mode <video or image> --verbose
To start the visualisation run the alva_visualisation.py file after all the assets have been generated with the following command:
    python3 alva_visualisation.py --path_to_assets <path_to_assets>
"""



import os
import argparse
import subprocess
import tqdm

from dotenv import load_dotenv

from utils import anonymize_faces
from utils import reduce_fps


# set up the environment variables
load_dotenv()
env = os.environ



def main(args):
    print("in main")
    if args.reduce_fps:
        args.video_in = reduce_fps.reduce_fps(args.video_in, args.reduce_fps, callback=True)
    if args.anonymize:
        args.video_in = anonymize_faces.anon_video(args.video_in, callback=True)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser("alva")
    parser.add_argument("--video_in", type=str, default=env["PATH_TO_DATASET_MANUAL_DATA_IN"], help="path to the video / image ")
    # parser.add_argument("--path_out", type=str, help="path to the video / image ")
    parser.add_argument("--reduce_fps", type=int, help="reduces the fps of the input video")
    parser.add_argument("--anonymize", help="video will be anonymized")
    # parser.add_argument("--verbose", help="verbose level of output")
    args = parser.parse_args() 

    main(args)
    
