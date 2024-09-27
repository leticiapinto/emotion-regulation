# main.py

import pandas as pd
import os
from video_splits import VideoSplits

class Main:
    def __init__(self, csv_path, output_directory, type_split):
            print("Initialization of Main ")
            data = pd.read_csv(csv_path)

            # Ensure the 'user' and 'other' columns are treated as strings to handle mixed data types
            data['user'] = data['user'].astype(str)
            data['other'] = data['other'].astype(str)

            self.data = data
            self.type_split = type_split
            os.makedirs(output_directory, exist_ok=True)
            self.output_directory = output_directory
            self.splitmyvideo = VideoSplits()

    def run(self, user_folders ):
        print("Let's start this run")
        for user_folder in user_folders:
            self.splitmyvideo.run(self.data, output_directory, user_folder, self.type_split)
        print("Decision time segments saved successfully.")
       
                        


if __name__ == "__main__":
    csv_path = '/home/leticia/datasets/emotion-regulation/other_files/Split_steal_study2_decisions_and_timestamps_fix.csv'

    # Create a directory to save the decision time segments
    type_split = 'outcome'
    output_directory = '/home/leticia/datasets/emotion-regulation/edited_videos/' + type_split
    

    # Process each user folder
    #user_folders = [f"user{i:03}" for i in range(101, 201)]
    videos_ = '/home/leticia/datasets/emotion-regulation/videos_test_only/'
    user_folders = [f"{videos_}user{i:03}" for i in range(101, 102)]
    main = Main(csv_path=csv_path, output_directory= output_directory, type_split=type_split)
    for user_folder in user_folders:
        main.run(user_folders)


