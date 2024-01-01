import os
import subprocess

# INPUT_DIR must cointain only videos
INPUT_DIR = os.path.join("test_data", "ALVA_PostProcessed_Data")    # path to the directory containing the videos
SUPPORTED_FORMATS = [".mp4", ".avi", ".mov", ".mkv", ".webm"]

def main():
    # run the video through alva.py to generate the assets and store everything in ./vis_tool/assets
    for video in os.listdir(INPUT_DIR):
        if os.path.splitext(video)[1] in SUPPORTED_FORMATS:
            print(f"Processing {video}")
            subprocess.run([
                "python", 
                os.path.join(".", "alva.py"),
                "--video-in", os.path.join(INPUT_DIR, video),
                "--pose-estimation",
                "--object-detection",
                "--object-interaction"
                ])
            print(f"Finished processing {video}")
        else:
            print(f"Unsupported format for {video}")
    print("Finished processing all videos")
    print("Starting visualisation tool by running oc_tool.py")


if __name__ == "__main__":
    main() 

