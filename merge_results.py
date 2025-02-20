import pandas as pd
import csv

# Load the CSV files
video_mapping_df = pd.read_csv('/data/vidlab_datasets/challenge_crop/split/val.csv', header=None, names=['video', 'index'], skiprows=0)
prediction_results_df = pd.read_csv('batch_indices.csv', header=None, names=['id', 'top_1_index'], skiprows=1)
labels_df = pd.read_csv('/data/users/sdas/scripts/ViFi-CLIP/labels/challenge.csv', header=None, names=['id', 'label'], skiprows=1)

# Convert types for accurate merging
video_mapping_df['index'] = video_mapping_df['index'].astype(int)
prediction_results_df['id'] = prediction_results_df['id'].astype(int)
prediction_results_df['top_1_index'] = prediction_results_df['top_1_index'].astype(int)
labels_df['id'] = labels_df['id'].astype(int)

# Assuming prediction_results_df and video_mapping_df are already defined and properly indexed
with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(['video_name', 'action_category'])

    # Initialize k to start at the first index of video_mapping_df
    k = 0

    # Loop through the 'top_1_index' in prediction_results_df
    for i in prediction_results_df['top_1_index']:
        if 0 <= i <= 7:
            action_category = 'locomotion'
        elif 8 <= i <= 22:
            action_category = 'manipulation'
        elif 23 <= i <= 31:
            action_category = 'communication'
        elif 32 <= i <= 37:
            action_category = 'hygiene'
        elif i in {38, 39}:  # This corrects the logic to check for both values 38 and 39
            action_category = 'eating_drinking'
        else:
            action_category = 'leisure'

        # Write the row to the CSV file
        writer.writerow([video_mapping_df['video'][k], action_category])
        k += 1

