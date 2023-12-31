import os
import sys
import cv2
import subprocess

SAMPLE_RATE = 1     # how many frames per second to sample


def extract_object_interactions(video_path, sample_rate=SAMPLE_RATE):

    # temp folder for the frames
    tmp_folder = os.path.join("temp", "RelTR_tmp_img_" + os.path.basename(video_path).split(".")[0])

    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)
    
    save_dir = tmp_folder

    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_count = 0
    sample_frame = 1 if int(fps / SAMPLE_RATE) < 1 else int(fps / SAMPLE_RATE)
    

    while True:
        is_read, frame = cap.read()
        if not is_read:
            # no further frames to read
            break
        if frame_count % sample_frame == 0:
            # save the frames with the correct indices 
            cv2.imwrite(os.path.join(save_dir, os.path.basename(video_path).split(".")[0] + "_%d.jpg"%(frame_count)), frame)
        frame_count += 1

    # release input and output video objects
    cap.release()

    # now run the RelTR model on the frames and output to runs folder
    out_path = os.path.join("runs", "RelTR")
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    images = os.listdir(save_dir)

    for image in images:
        frame = image.split("_")[-1].split(".")[0]
        print(image)
        print(frame)
        subprocess.check_output([f'python',
                             f"./RelTR/mkgraph.py",
                             "--img_path", os.path.join(save_dir, image),
                             "--device", "cuda",
                             "--resume", "./RelTR/ckpt/checkpoint0149.pth",
                             "--export_path", os.path.join(out_path, f"{image.split('.')[0]}.json"),
                             "--topk", "30"])



if __name__ == "__main__":
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(__doc__)
            sys.exit(0)
        elif len(sys.argv) == 2:
            extract_object_interactions(sys.argv[1])
        else:
            print("Invalid number of arguments. Run with -h or --help for help.")
            sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

