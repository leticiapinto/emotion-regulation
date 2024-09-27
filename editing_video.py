import os
import pandas as pd
from moviepy.video.io.VideoFileClip import VideoFileClip

# Define a function to convert the timestamps to seconds
def convert_to_seconds(timestamp, base_timestamp):
    return (timestamp - base_timestamp) / 1000

# Define a function to cut 5 seconds of video from the decision time
def cut_decision_time_segment(video_path, decision_times, output_prefix, base_timestamp, user_id):
    try:
        clip = VideoFileClip(video_path)
        
        for i, decision_time in enumerate(decision_times):
            start_time = convert_to_seconds(decision_time, base_timestamp)
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

# Load the CSV file
csv_path = '/home/leticia/datasets/emotion-regulation/other_files/Split_steal_study2_decisions_and_timestamps_fix.csv'
data = pd.read_csv(csv_path)

# Ensure the 'user' and 'other' columns are treated as strings to handle mixed data types
data['user'] = data['user'].astype(str)
data['other'] = data['other'].astype(str)

# Create a directory to save the decision time segments
output_directory = 'edited_file'
os.makedirs(output_directory, exist_ok=True)

# Process each user folder
#user_folders = [f"user{i:03}" for i in range(101, 201)]
user_folders = ["/home/leticia/datasets/emotion-regulation/videos/video_test_user101_session0"]

for user_folder in user_folders:
    video_path = os.path.join(user_folder, 'converted30fps.mp4')
    print(video_path)
    if os.path.exists(video_path):
        print(f"Processing video for {user_folder}")
        #user_id = user_folder.replace('user', '')
        user_id = "101_session0"
        print(f"Checking data for user ID: {user_id}")
        user_data = data[(data['user'] == user_id) | (data['other'] == user_id)]

        # Debugging: Print user-specific data
        print(f"User ID: {user_id}")
        print(user_data)

        if not user_data.empty:
            try:
                # Extract decision times
                decision_times = [float(user_data[f'd_time_r{i}'].iloc[0]) for i in range(1, 11)]
                # Get the base timestamp (first decision time) for normalization
                base_timestamp = float(user_data['d_time_r1'].iloc[0])
                
                # Create user-specific output directory
                user_output_directory = os.path.join(output_directory, user_folder)
                os.makedirs(user_output_directory, exist_ok=True)
                
                # Cut and save 5 seconds of video from each decision time
                cut_decision_time_segment(video_path, decision_times, user_output_directory, base_timestamp, user_id)
            except Exception as e:
                print(f"Error processing decision times for {user_folder}: {e}")
        else:
            print(f"No data found for user {user_id} in CSV")
    else:
        print(f"Video file not found for {user_folder}")

print("Decision time segments saved successfully.")