import os
import shutil

# get the current path of the current file
path = os.path.dirname(os.path.realpath(__file__))

# construct assets paths
assets = os.path.join(path, "assets/")

# base structure for the assets folder
base_folders = [
os.path.join(assets, "openpose_output/"),
os.path.join(assets, "pifpaf_output/"),
os.path.join(assets, "yolo_extra_large_output/"),
os.path.join(assets, "yolo_nano_output/"),
]

# construct data_in path
data_in = os.path.join(path, "data_in/")

# reset the assets folder
shutil.rmtree(assets)

# rebuild the assets folder structure
os.mkdir(assets)
for folder in base_folders:
    os.mkdir(folder)

# reset the data_in folder to base state
shutil.rmtree(data_in)

# reset the data_in folder to base state
os.mkdir(data_in)
with open(os.path.join(data_in, "here_goes_the_video_file.md"), "w") as f: pass