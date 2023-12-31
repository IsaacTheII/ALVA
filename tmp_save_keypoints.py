import os

from analysis.extract_keypoints import get_keypoints_openpose
from structures import keypoints_structure

if __name__ == "__main__":
    directory = os.path.join("runs_full_run", "openpose")

    print(directory)

    child, therapist, child_bbox, therapist_bbox = get_keypoints_openpose(directory)
    # save the keypoints and bounding boxes to the juxtaposition folder
    save_dir = os.path.join("temp", "juxtaposition")

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    keypoints_structure.save_numpy_keypoints_bbox(child, child_bbox, save_dir, "child")
    keypoints_structure.save_numpy_keypoints_bbox(therapist, therapist_bbox, save_dir, "therapist")