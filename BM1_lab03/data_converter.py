import pandas as pd
import numpy as np
import os
import glob
from typing import List

def generate_rotation_angles(num_folders: int, step: int = 15):
    positive = list(range(0, 181, step))
    negative = list(range(-180 + step, 0, step))
    angles = positive + negative

    if num_folders > len(angles):
        raise ValueError("Not enough angles for number of measurement folders.")
    
    return angles[:num_folders]


def process_and_average_s_parameters(root_dir: str, 
                                     polar_output_suffix: str = '_polar', 
                                     output_filename: str = 'averaged_polar_data.csv') -> List[str]:
    """
    Reads all N.csv files (where N is any integer) from subdirectories, 
    converts them to Polar (Mag/Phase), calculates the average of those files (Intra-folder Average),
    and saves the single resulting DataFrame to a new dedicated subdirectory.
    
    The function focuses only on S11 and automatically detects the file range.

    :param root_dir: The path to the directory containing all the original measurement subfolders.
    :param polar_output_suffix: Suffix to append to the original folder name for the new polar directory.
    :param output_filename: The name of the resulting CSV file in the new polar directory.
    :return: A list of paths to the successfully created polar output files.
    """
    processed_files = []
    
    # Iterate through all direct subdirectories of the root_dir
    # for item_name in os.listdir(root_dir):
    folder_names = sorted([
        d for d in os.listdir(root_dir)
        if os.path.isdir(os.path.join(root_dir, d)) and not d.endswith(polar_output_suffix)
    ])

    angles = generate_rotation_angles(len(folder_names))
    for item_name, angle in zip(folder_names, angles):
        sub_dir = os.path.join(root_dir, item_name)
        
        # Check if it is a directory and not an output directory created previously
        if os.path.isdir(sub_dir) and not item_name.endswith(polar_output_suffix):
            
            sub_folder_polar_data = []
            print(f"Processing measurement folder: {item_name}")

            # 1. AUTOMATICALLY FIND AND SORT ALL N.csv FILES
            # Use glob to find files matching the pattern [0-9]*.csv
            search_pattern = os.path.join(sub_dir, "[0-9]*.csv")
            file_paths = glob.glob(search_pattern)
            
            # Sort files numerically based on the leading number (0.csv, 1.csv, 2.csv, ..., 10.csv, ...)
            def numeric_sort_key(path):
                filename = os.path.basename(path)
                try:
                    # Extract the leading number by splitting at the first dot
                    return int(filename.split('.')[0]) 
                except ValueError:
                    # Fallback for non-numeric filenames
                    return 999999 

            sorted_file_paths = sorted(file_paths, key=numeric_sort_key)
            
            print(f"  -> Found {len(sorted_file_paths)} files to process in this folder.")
            
            # 2. READ, EXTRACT, AND CONVERT ALL FILES
            for input_file_path in sorted_file_paths:
                try:
                    # Read the CSV file using a semicolon delimiter
                    df = pd.read_csv(input_file_path, sep=';')
                    
                    # --- CONVERSION (S11 ONLY) ---
                    df['S11_Mag'] = np.hypot(df['S11_Real'], df['S11_Imag'])
                    df['S11_Phase_Rad'] = np.arctan2(df['S11_Imag'], df['S11_Real'])
                    df['S21_Mag'] = np.hypot(df['S21_Real'], df['S21_Imag'])
                    df['S21_Phase_Rad'] = np.arctan2(df['S21_Imag'], df['S21_Real'])
                    
                    polar_df = df[['Frequency', 'S11_Mag', 'S11_Phase_Rad', 'S21_Mag', 'S21_Phase_Rad']]
                    sub_folder_polar_data.append(polar_df)
                    
                except Exception as e:
                    print(f"  -> Error processing {os.path.basename(input_file_path)}: {e}")
                
            
            if sub_folder_polar_data:
                # 3. CALCULATE INTRA-FOLDER AVERAGE
                combined_df = pd.concat(sub_folder_polar_data, ignore_index=True)
                averaged_polar_df = combined_df.groupby('Frequency').mean().reset_index()

                # 4. SAVE THE SINGLE AVERAGED POLAR DATA
                output_dir_name = item_name + polar_output_suffix
                output_dir_path = os.path.join(root_dir, output_dir_name)
                os.makedirs(output_dir_path, exist_ok=True)
                
                output_file_path = os.path.join(output_dir_path, output_filename)
                averaged_polar_df['Angle_deg'] = angle
                averaged_polar_df.to_csv(output_file_path, index=False)
                processed_files.append(output_file_path)
                
                print(f"   -> Successfully saved average to: {output_file_path}")
            else:
                print(f"No valid data found in {item_name}. Skipping save.")

    return processed_files