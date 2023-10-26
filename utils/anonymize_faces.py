import os
import argparse
import subprocess



def anon_video(path_to_vid, callback=False):
    # start deface on the video
    subprocess.run(["deface", path_to_vid],)
    

def main(args):
    if args:
        anon_video(args.path_in)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("anonymize_faces")
    parser.add_argument("--path_in", type=str, help="path to the video / image ")
    main(parser.parse_args())

