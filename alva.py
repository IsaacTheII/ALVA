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
To start the visualisation run the oc_tool.py file after all the assets have been generated with the following command:
    python3 oc_tool.py

"""


import sys
import os
import argparse
import subprocess
import shutil
import time
import tqdm

from dotenv import load_dotenv

from utils import anonymize_faces
from utils import reduce_fps

from modules import pose_estimation
from modules import object_detection
from modules import object_interaction
from modules import object_segmentation

from analysis import extract_keypoints
from analysis import extract_objects
from analysis import extract_interactions

from structures import timeline_structure
from structures import keypoints_structure

# set up the environment variables
load_dotenv()
env = os.environ


def main(args):
    # SETUP THE TIMELINE STRUCTURE
    timeline = timeline_structure.auto_init_(args.video_in)

    # RUN PREPROCESSING MODULES
    if args.reduce_fps:
        # update the frame rate of the timeline
        timeline.set_frame_rate(args.reduce_fps)
        args.video_in = reduce_fps.reduce_fps(
            args.video_in, args.reduce_fps, callback=True)
    if args.anonymize:
        args.video_in = anonymize_faces.anon_video(
            args.video_in, callback=True)
    
    #update the filename of the video_in in the timeline
    timeline.set_video_name(os.path.basename(args.video_in).split(".")[0])



    # SET UP FOLDERS AND PATHS FOR THE PROJECT
    # split the basename and discard the file extension
    video_name = os.path.splitext(os.path.basename(args.video_in))[0]

    # set up temp folder
    if not os.path.exists("temp"):
        os.mkdir("temp")
    path_to_assets = "temp"

    # destination folder for the assets for the visualisation tool
    path_to_vis_tool_assets = os.path.join("vis_tool", "assets", "video_assets")

    # create output directory with the same name as the basename of video_in in ./temp/ folder and copy the video_in to the output directory
    # check if the namespace is open in the ./vis_tool/assets/video_assets folder
    if not os.path.exists(os.path.join(path_to_vis_tool_assets, video_name)):
        # create the directory where all the assets will be stored
        os.mkdir(os.path.join(path_to_assets, video_name))
        path_to_assets = os.path.join(path_to_assets, video_name)
        # copy the video to the output directory
        shutil.copy2(args.video_in, path_to_assets)
        # set the path to the video_in to the new path
        args.video_in = os.path.join(
            path_to_assets, video_name + os.path.splitext(args.video_in)[1])
    # if there is already a directory with the same name then find open namespace, copy the video and rename it
    else:
        count = 2
        new_video_name = video_name + "_" + str(count)
        while os.path.exists(os.path.join(path_to_vis_tool_assets, new_video_name)):
            count += 1
            new_video_name = video_name + "_" + str(count)
        os.mkdir(os.path.join(path_to_assets, new_video_name))
        path_to_assets = os.path.join(path_to_assets, new_video_name)
        shutil.copy2(args.video_in, os.path.join(path_to_assets,
                     new_video_name + os.path.splitext(args.video_in)[1]))
        args.video_in = os.path.join(
            path_to_assets, new_video_name + os.path.splitext(args.video_in)[1])
    
    # update the path to the video_in in the timeline
    timeline.set_video_name(os.path.basename(args.video_in).split(".")[0])

    

    # RUN THE DIFFERENT PROCESSING MODULES
    if args.pose_estimation:
        pose_estimation.extract_pose_openpose(args.video_in)
    if args.object_detection:
        object_detection.detect_objects(args.video_in)
    if args.object_interaction:
        object_interaction.extract_object_interactions(
            args.video_in, sample_rate=1)
    """ if args.object_segmentation:
        object_segmentation.segment_objects(args.video_in) """

    # RUN THE DIFFERENT ANALYSIS MODULES AND STORE THEM IN THE ASSETS FOLDER
    # we need to run all video files through ffmpeg due to a incompatible codec issue with opencv and dash player then remove to old files

    # check if if pose estimation was run
    if args.pose_estimation:
        subprocess.run(["ffmpeg", "-i", args.video_in,
                       os.path.splitext(args.video_in)[0] + "_original.mp4"])
        os.remove(args.video_in)

        # save the superimposed video to the superposition folder
        if not os.path.exists(os.path.join(path_to_assets, "superposition")):
            os.mkdir(os.path.join(path_to_assets, "superposition"))

        # get the path to the superimposed video from openpose
        files = os.listdir(os.path.join(path_to_assets))
        for file in files:
            if file.endswith("_openpose.avi"):
                # run the video through ffmpeg to convert it to mp4 and make it compatible with dash player
                subprocess.run(["ffmpeg", "-i", os.path.join(path_to_assets, file), os.path.join(
                    path_to_assets, "superposition", os.path.splitext(file)[0] + ".mp4")])
                os.remove(os.path.join(path_to_assets, file))

        # save the keypoints and bounding boxes to the juxtaposition folder
        jux_path = os.path.join(path_to_assets, "juxtaposition")
        os.mkdir(jux_path)
        child, therapist, child_bbox, therapist_bbox = extract_keypoints.get_keypoints_openpose(os.path.join("runs", "openpose"))
        keypoints_structure.save_numpy_keypoints_bbox(child, child_bbox, jux_path, "child")
        keypoints_structure.save_numpy_keypoints_bbox(therapist, therapist_bbox, jux_path, "therapist")

    # check if if object detection was run
    if args.object_detection:
        objects = extract_objects.extract_objects(
            dir=os.path.join("runs", "detect", "predict", "labels"),
            fps=int(float(timeline.Frame_Rate)),
            life_time_seconds=10)
        # insert objects into timeline
        for objname, list_start_end in objects.items():
            for start, end in list_start_end:
                timeline.add_object(
                    start_time=time.strftime("%H:%M:%S", time.gmtime(start / float(timeline.Frame_Rate))),
                    end_time=time.strftime("%H:%M:%S", time.gmtime(end / float(timeline.Frame_Rate))),
                    object_name=objname)
    
    # check if if object interaction was run
    if args.object_interaction:
        interactions = extract_interactions.extract_object_interactions_events(
            dir=os.path.join("runs", "RelTR"), 
            fps=int(float(timeline.Frame_Rate)), 
            life_time_seconds=3)
        for start, event in interactions.items():
            timeline.add_object_interaction(
                event_time=time.strftime("%H:%M:%S", time.gmtime(start / float(timeline.Frame_Rate))),
                event_description="Is " + event[0] + " " + event[1] + ".")
            
    
    # SAVE THE TIMELINE TO THE ASSETS FOLDER
    # create the timeline folder
    if not os.path.exists(os.path.join(path_to_assets, "timeline")):
        os.mkdir(os.path.join(path_to_assets, "timeline"))
    # save the timeline to the timeline folder
    timeline_file_name = os.path.join(path_to_assets, "timeline", os.path.split(path_to_assets)[1] + "_timeline.txt")
    timeline.export_to_file(timeline_file_name)


    # copy the generated assets to the vis_tool/assets/video_assets folder and then clean up everythin in runs and temp folder
    shutil.move(os.path.join(path_to_assets), path_to_vis_tool_assets)
    shutil.rmtree("runs")
    os.mkdir("runs")
    shutil.rmtree("temp")
    os.mkdir("temp")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="alva.py",
        description="This is the main file of the ALVA project. It is used to call the different modules of the project. And to generate the different assets needed for the visualisation.",)

    parser.add_argument("--video-in", type=str,
                        default=env["PATH_TO_DATASET_MANUAL_DATA_IN"], help="path to the video / image ")
    # parser.add_argument("--path_out", type=str, help="path to the video / image ")    # will automatically be saved in the assets folder of the oc_tool
    parser.add_argument("--reduce-fps", type=int, help="reduces the fps of the input video")  # this step should be done before loading the video into data-in
    parser.add_argument("--anonymize", action="store_true", help="video will be anonymized")  # this step should be done before loading the video into data-in
    parser.add_argument("--pose-estimation", action="store_true",
                        help="extract the pose infromation of people in the video")
    parser.add_argument("--object-detection", action="store_true",
                        help="extract the objects of interest in the video")
    parser.add_argument("--object-interaction", action="store_true",
                        help="extract interactions object and people in the video")
    # parser.add_argument("--object-segmentation", action="store_true", help="extract the pose infromation of people in the video")
    # parser.add_argument("--verbose", action="store_true", help="verbose")

    # catch no arguments
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    main(args)
