import os
import pandas as pd
import numpy as np
import time
import cv2


class Timeline:
    """
    This class is used to store all the data needed for the timeline of the video. It is used 
    it categorizes the data into different tables and defines how to work with set data.
    """

    def __init__(self, video_name=None, duration=None, frame_width=None, frame_height=None, frame_rate=None, total_frames=None, date_recorded=None, author=None, date_coding=None):
        # general information
        self.Video_Name = str(video_name)
        self.Duration = str(duration)
        self.Frame_Width = str(frame_width)
        self.Frame_Height = str(frame_height)
        self.Frame_Rate = str(frame_rate)
        self.Total_Frames = str(total_frames)
        self.Date_Recorded = str(date_recorded)
        self.Author = str(author)
        self.Date_Coding = str(date_coding)

        # dataframes for the different tables
        self.Objects = pd.DataFrame(columns=[
            "Start_Time",
            "End_Time",
            "Object_Name",
        ])

        self.Object_Interactions = pd.DataFrame(columns=[
            "Event_Time",
            "Event_Description",
        ])

        self.ABCS_Coding = pd.DataFrame(columns=[
            "Start_Time",
            "End_Time",
            "ABCS_Variable",
            "ABCS_Comment",
        ])

        return

    # setters and getters for dataframes
    def add_object(self, start_time, end_time, object_name):
        """
        This function is used to add an object to the objects table.
        """
        self.Objects = pd.concat([self.Objects, 
                                  pd.DataFrame([[str(start_time), str(end_time), str(object_name)]], columns=self.Objects.columns)], 
                                  ignore_index=True)
        return

    def add_object_interaction(self, event_time, event_description):
        """
        This function is used to add an object interaction to the object interaction table.
        """
        self.Object_Interactions = pd.concat([self.Object_Interactions, 
                                              pd.DataFrame([[str(event_time), str(event_description)]], columns=self.Object_Interactions.columns)],
                                              ignore_index=True)
        return

    def add_abcs_coding(self, start_time, end_time, abcs_variable, abcs_comment=None):
        """
        This function is used to add an abcs coding to the abcs coding table.
        """
        self.ABCS_Coding = pd.concat([self.ABCS_Coding, 
                                      pd.DataFrame([[str(start_time), str(end_time), str(abcs_variable), str(abcs_comment)]], columns=self.ABCS_Coding.columns)],
                                      ignore_index=True)
        return

    def get_objects(self):
        return self.Objects

    def get_objects_by_name(self, object_name):
        """
        Returns a dataframe with  all the objects with the given name.
        """
        return self.Objects[self.Objects["Object_Name"] == object_name]

    def get_object_from_range(self, start_time, end_time):
        """
        Returns a dataframe with  all the object detections within the given time range.
        """
        return self.Objects[(self.Objects["Start_Time"] >= start_time) & (self.Objects["End_Time"] <= end_time)]

    def get_object_interactions(self):
        return self.Object_Interactions

    def get_object_interactions_by_name(self, object_name):
        """
        Returns a dataframe with  all the object interactions with the given name.
        """
        return self.Object_Interactions[self.Object_Interactions["Object_Name"] == object_name]

    def get_object_interactions_from_range(self, start_time, end_time):
        """
        Returns a dataframe with all the object interactions within the given time range.
        """
        return self.Object_Interactions[(self.Object_Interactions["Start_Time"] >= start_time) & (self.Object_Interactions["End_Time"] <= end_time)]

    def get_abcs_coding(self):
        return self.ABCS_Coding

    # setters and getters for general information
    def set_video_name(self, video_name):
        self.Video_Name = str(video_name)
        return

    def get_video_name(self):
        return self.Video_Name

    def set_duration(self, duration):
        self.Duration = str(duration)
        return

    def get_duration(self):
        return self.Duration

    def set_frame_width(self, frame_width):
        self.Frame_Width = str(frame_width)
        return

    def get_frame_width(self):
        return self.Frame_Width

    def set_frame_height(self, frame_height):
        self.Frame_Height = str(frame_height)
        return

    def get_frame_height(self):
        return self.Frame_Height

    def set_frame_rate(self, frame_rate):
        self.Frame_Rate = str(frame_rate)
        return

    def get_frame_rate(self):
        return self.Frame_Rate
    
    def set_total_frames(self, total_frames):
        self.Total_Frames = str(total_frames)
        return
    
    def get_total_frames(self):
        return self.Total_Frames

    def set_date_recorded(self, date_recorded):
        self.Date_Recorded = str(date_recorded)
        return

    def get_date_recorded(self):
        return self.Date_Recorded

    def set_author(self, author):
        self.Author = str(author)
        return

    def get_author(self):
        return self.Author

    def set_date_coding(self, date_coding):
        self.Date_Coding = str(date_coding)
        return

    def get_date_coding(self):
        return self.Date_Coding

    def import_from_file(self, path_to_file):
        """
        This function is used to import the data from an existing human readable timeline file.
        """
        # Read file
        with open(path_to_file, 'r') as file:
            lines = file.readlines()

        table_sep = "-------------------------------------------------------------------------\n"

        # Parse general information
        general_info_start = lines.index(table_sep)
        general_info_end = lines.index(table_sep, general_info_start + 1)

        general_info_lines = lines[general_info_start + 1 :general_info_end]
        general_info = {}

        for line in general_info_lines:
            key, value = line.split(maxsplit=1)
            general_info[key.strip()] = value.strip()

        self.set_video_name(general_info["Video_Name"])
        self.set_duration(general_info["Duration"])
        self.set_frame_width(general_info["Frame_Width"])
        self.set_frame_height(general_info["Frame_Height"])
        self.set_frame_rate(general_info["Frame_Rate"])
        self.set_total_frames(general_info["Total_Frames"])
        self.set_date_recorded(general_info["Date_Recorded"])
        self.set_author(general_info["Author"])
        self.set_date_coding(general_info["Date_Coding"])

        # Parse objects
        objects_start = lines.index(table_sep, general_info_end + 1)
        objects_end = lines.index(table_sep, objects_start + 1)
        objects_lines = lines[objects_start + 1:objects_end]
        objects = []
        for line in objects_lines:
            start_time, end_time, object_name = line.strip().split(maxsplit=2)
            objects.append((start_time, end_time, object_name))

        # Insert objects into timeline object
        for obj in objects:
            self.add_object(obj[0], obj[1], obj[2])

        # Parse object interactions
        interactions_start = lines.index(table_sep, objects_end + 1)
        interactions_end = lines.index(table_sep, interactions_start + 1)

        interactions_lines = lines[interactions_start + 1:interactions_end]
        interactions = []
        for line in interactions_lines:
            event_time, event_description = line.strip().split(maxsplit=1)
            interactions.append((event_time, event_description))

        # Insert object interactions into timeline object
        for interaction in interactions:
            self.add_object_interaction(interaction[0], interaction[1])

        # Parse ABCS coding
        abcs_start = lines.index(table_sep, interactions_end + 1)
        abcs_end = lines.index(table_sep, abcs_start + 1)

        abcs_lines = lines[abcs_start + 1:abcs_end]
        abcs_coding = []
        for line in abcs_lines:
            start_time, end_time, abcs_variable, abcs_comment = line.strip().split(maxsplit=3)
            abcs_coding.append((start_time, end_time, abcs_variable, abcs_comment))

        # Insert ABCS coding into timeline object
        for coding in abcs_coding:
            self.add_abcs_coding(coding[0], coding[1], coding[2], coding[3])
        return
    
    def export_to_file(self, path_to_file):
        """
        This function is used to export the data to a human readable timeline file.
        """
        title_sep = "=========================================================================\n"
        table_sep = "-------------------------------------------------------------------------\n"
        
        general_info_title = title_sep + "General Information\n" + title_sep
        general_info_table_header = "Name" + "\t" * 4 + "Value\n"

        objects_title = title_sep + "Objects\n" + title_sep
        objects_table_header = "Start_Time" + "\t" * 2 + "End_Time" + "\t" * 2 + "Object_Name\n"

        interactions_title = title_sep + "Object Interactions\n" + title_sep
        interactions_table_header = "Event_Time" + "\t" * 2 + "Event_Description\n"

        abcs_title = title_sep + "ABCS Coding\n" + title_sep
        abcs_table_header = "Start_Time" + "\t" * 2 + "End_Time" + "\t" * 2 + "ABCS_Variable" + "\t" * 2 + "ABCS_Comment\n"

        # write to file
        with open(path_to_file, 'w') as file:
            # write general information
            file.write(general_info_title)

            file.write(general_info_table_header)
            file.write(table_sep)
            file.write("Video_Name" + "\t" * 3 + self.get_video_name() + "\n")
            file.write("Duration" + "\t" * 3 + self.get_duration() + "\n")
            file.write("Frame_Width" + "\t" * 3 + self.get_frame_width() + "\n")
            file.write("Frame_Height" + "\t" * 2 + self.get_frame_height() + "\n")
            file.write("Frame_Rate" + "\t" * 3 + self.get_frame_rate() + "\n")
            file.write("Total_Frames" + "\t" * 2 + self.get_total_frames() + "\n")
            file.write("Date_Recorded" + "\t" * 2 + self.get_date_recorded() + "\n")
            file.write("Author" + "\t" * 4 + self.get_author() + "\n")
            file.write("Date_Coding" + "\t" * 3 + self.get_date_coding() + "\n")
            file.write(table_sep + "\n\n\n")

            # write objects
            file.write(objects_title)

            file.write(objects_table_header)
            file.write(table_sep)
            for index, row in self.get_objects().iterrows():
                file.write(row["Start_Time"] + "\t" * 2 + row["End_Time"] + "\t" * 2 + row["Object_Name"] + "\n")
            file.write(table_sep + "\n\n\n")

            # write object interactions
            file.write(interactions_title)

            file.write(interactions_table_header)
            file.write(table_sep)
            for index, row in self.get_object_interactions().iterrows():
                file.write(row["Event_Time"] + "\t" * 2 + row["Event_Description"] + "\n")
            file.write(table_sep + "\n\n\n")

            # write abcs coding
            file.write(abcs_title)

            file.write(abcs_table_header)
            file.write(table_sep)
            for index, row in self.get_abcs_coding().iterrows():
                file.write(row["Start_Time"] + "\t" * 2 + row["End_Time"] + "\t" * 2 + row["ABCS_Variable"] + "\t" * 5 + row["ABCS_Comment"] + "\n")
            file.write(table_sep + "\n\n\n")

        return
    


def auto_init_(video_path):
    """
    This function is used to auto init the timeline structure from a video file.
    """
    # init timeline
    cap = cv2.VideoCapture(video_path)

    timeline = Timeline(
        video_name = os.path.basename(video_path).split(".")[0],
        duration=cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS),
        frame_width=cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        frame_height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
        frame_rate=cap.get(cv2.CAP_PROP_FPS),
        total_frames=cap.get(cv2.CAP_PROP_FRAME_COUNT),
        date_recorded=time.strftime("%Y-%m-%d", time.strptime(time.ctime(os.path.getctime(video_path)))),
        author=None,
        date_coding=time.strftime("%Y-%m-%d", time.strptime(time.ctime(os.path.getctime(video_path)))),
    )
    return timeline