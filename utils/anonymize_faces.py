import os
import argparse
import subprocess



def anon_video(path_to_vid, callback=False):

    filename, _ = os.path.splitext(path_to_vid)
    filename += "_anonymized.mp4"

    # start deface on the video
    subprocess.run(["deface", path_to_vid],)
    
    # optionaly if callback is requested return the new filename
    if callback:
        return filename


def anon_folder(path_to_folder, callback=False):
    # start deface on the video
    subprocess.run(["deface", path_to_vid],)
    
    # optionaly if callback is requested return the new filename
    if callback:
        return 0


def main(args):
    if args:
        anon_video(args.path_in)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("anonymize_faces")
    parser.add_argument("--path_in", type=str, help="path to the video / image ")
    main(parser.parse_args())

