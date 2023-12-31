import os
import json


FPS = 25    # frames per second

LIFE_TIME_SECONDS = 3   # seconds

LIFE_TIME_SECONDS = 3   # seconds


# object interactions
object_interactions = ['carrying', 'eating', 'holding', 'laying on',  'looking at', 'lying on', 'playing', 'riding', 'says', 'sitting on', 'standing on',
                       'using', 'walking in', 'walking on', 'watching']
"""     RelTR predicates
['__background__', 'above', 'across', 'against', 'along', 'and', 'at', 'attached to', 'behind',
                   'belonging to', 'between', 'carrying', 'covered in', 'covering', 'eating', 'flying in', 'for',
                   'from', 'growing on', 'hanging from', 'has', 'holding', 'in', 'in front of', 'laying on',
                   'looking at', 'lying on', 'made of', 'mounted on', 'near', 'of', 'on', 'on back of', 'over',
                   'painted on', 'parked on', 'part of', 'playing', 'riding', 'says', 'sitting on', 'standing on',
                   'to', 'under', 'using', 'walking in', 'walking on', 'watching', 'wearing', 'wears', 'with']
"""


def extract_object_interactions_events(dir, fps=FPS, life_time_seconds=LIFE_TIME_SECONDS):

    files = sorted(os.listdir(dir), key=lambda x: int(x.split(".")[0].split("_")[-1]))

    interactions_all_frames = {}

    for file in files:
        frame_number = int(file.split(".")[0].split("_")[-1])
        interactions_all_frames[frame_number] = []
        with open(os.path.join(dir, file), "r") as f:
            triplets = json.load(f)

            for triplet in triplets:
                subject = triplet["subject"]["id"]
                predicate = triplet["predicate"]["id"]
                object = triplet["object"]["id"]

                if predicate in object_interactions:
                    interactions_all_frames[frame_number].append([subject, predicate, object])
    
    # track previous interactions
    active_interactions = {}
    # track the start frame of new interactions
    start_frame_interaction = {}
    # max duration of an interaction before it is considered a new interaction
    lifetime = life_time_seconds * fps
    for key in sorted(interactions_all_frames.keys()):
        for interaction in interactions_all_frames[key]:
            # new interaction
            if interaction[1] not in active_interactions.keys():
                start_frame_interaction[key] = interaction[1:]   # save the start frame of the interaction
                active_interactions[interaction[1]] = key  # save the current frame of the interaction
            # interaction already active
            elif key - active_interactions[interaction[1]] <= lifetime:
                active_interactions[interaction[1]] = key   # update the current frame of the interaction
            # interaction too old, start new interaction
            else:
                start_frame_interaction[key] = interaction[1:]   # save the start frame of the interaction
                active_interactions[interaction[1]] = key   # save the current frame of the interaction
    return start_frame_interaction

