import os
import sys
import subprocess

def main(src):
    # this is a workaround for a bug in openpifpaf. try removing it before your first run. It might not be necessary anymore.
    os.environ['KMP_DUPLICATE_LIB_OK']='True'

    # check src file type. (video or image)
    if src.split(".")[-1].lower() in ["mp4", "avi", "mov", "mkv"]:
        is_video = True
    elif src.split(".")[-1].lower() in ["jpg", "jpeg", "png"]:
        is_video = False
    else:
        print("Please provide a video or image file as an argument.")
        exit()

    # ouput directory for the json and video files
    output_dir_vid = os.path.join(os.path.dirname(__file__), "assets", "pifpaf_output", os.path.basename(src).split(".")[0] + ".mp4")
    output_dir_jsn = os.path.join(os.path.dirname(__file__), "assets", "pifpaf_output", os.path.basename(src).split(".")[0] + ".json")

    # choose command for src type. the commands will create a json and a rendered output file in the assets/pifpaf_output folder.
    if is_video:
        command = f"python -m openpifpaf.video --source {src} --video-output {output_dir_vid} --json-output {output_dir_jsn}"
    else:
        command = f"python -m openpifpaf.predict {src} --image-output {output_dir_vid} --json-output {output_dir_jsn}"

    # run the command
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    # check if the script is run in the correct environment
    if not os.environ["CONDA_PREFIX"].split("\\")[-1] == "pifpaf":
        print("Please run this script in the pifpaf environment. See the README for more information. Or disable this check in the script.")
        exit()

    # get video location and run the pose estimation
    try:
        src_vid = sys.argv[1]
    except Exception as e:
        print(e)
        print("Please provide a video file as an argument.")

    main(src_vid)
    