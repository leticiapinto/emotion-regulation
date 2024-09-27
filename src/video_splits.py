# video_splits.py

import os
import pandas as pd
from moviepy.video.io.VideoFileClip import VideoFileClip

class VideoSplits:
    def __init__(self):
        
        print("starting point")
        
    # Define a function to convert the timestamps to seconds
    def convert_to_seconds(self, timestamp, base_timestamp):
        return (timestamp - base_timestamp) / 1000

    # Define a function to cut 5 seconds of video from the decision time
    def cut_decision_time_segment(self, video_path, decision_times, output_prefix, base_timestamp, user_id):
        try:
            clip = VideoFileClip(video_path)
            
            for i, decision_time in enumerate(decision_times):
                start_time = self.convert_to_seconds(decision_time, base_timestamp)
                end_time = start_time + 5
                if start_time < clip.duration and end_time <= clip.duration:
                    subclip = clip.subclip(start_time, end_time)
                    output_path = os.path.join(output_prefix, f"{user_id}_{i+1}.mp4")
                    subclip.write_videofile(output_path, codec="libx264")
                else:
                    print(f"Skipping session {i+1} for user {user_id} due to invalid times: start={start_time}, end={end_time}")

            clip.close()
        except Exception as e:
            print(f"Error processing video for user {user_id}: {e}")
    
    def run(self, data, output_directory, user_folder, type_split = 'decision'):

        type_split = type_split[0]
        print("type split: ", type_split)
        video_path = os.path.join(user_folder, 'converted30fps.mp4')
        print(video_path)
        if os.path.exists(video_path):
            print(f"Processing video for {user_folder}")
            user_folder = user_folder.split("/")[-1]
            user_id = user_folder.replace('user', '')
            #user_id = "101"
            print(f"Checking data for user ID: {user_id}")
            user_data = data[(data['user'] == user_id) | (data['other'] == user_id)]

            # Debugging: Print user-specific data
            print(f"User ID: {user_id}")
            print(user_data)

            if not user_data.empty:
                try:
                    # Extract decision times
                    decision_times = [float(user_data[f'{type_split}_time_r{i}'].iloc[0]) for i in range(1, 11)]
                    # Get the base timestamp (first decision time) for normalization
                    base_timestamp = float(user_data[f'{type_split}_time_r1'].iloc[0])

                    # Create user-specific output directory
                    user_output_directory = os.path.join(output_directory, user_folder)
                    os.makedirs(user_output_directory, exist_ok=True)
                    self.cut_decision_time_segment(video_path, decision_times, 
                                                   user_output_directory, base_timestamp, user_id)
                except Exception as e:
                    print(f"Error processing decision times for {user_folder}: {e}")
            else:
                print(f"No data found for user {user_id} in CSV")
        else:
            print(f"Video file not found for {user_folder}")    
    
         

