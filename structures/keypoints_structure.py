import os
import numpy as np


def save_numpy_keypoints_bbox(keypoints, bbox, path, name):
    # save the keypoints as numpy array
    np.save(os.path.join(path, name + ".npy"), keypoints)

    # save the bounding box as numpy array
    np.save(os.path.join(path, name + "_bbox.npy"), bbox)


def load_numpy_keypoints_bbox(path, name):
    # load the keypoints as numpy array
    keypoints = np.load(os.path.join(path, name + ".npy"))

    # load the bounding box as numpy array
    bbox = np.load(os.path.join(path, name + "_bbox.npy"))

    return keypoints, bbox

    