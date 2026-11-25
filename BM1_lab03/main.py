import os
from data_converter import process_and_average_s_parameters 
from plot_generator import plot_s_parameters_db
from determine_resononace_frequency import find_global_best_resonance
from compute_radiation_pattern import compute_pattern
from analyze_radiation_pattern import analyze_pattern
from plot_radiation_pattern import plot_pattern


# 1. Configuration
# This is the folder containing all measurement subfolders (Cardboard, Air, etc.)
ROOT_DATA_DIR = r"C:\Users\Joel\Downloads\BOMAPS\Lab\Lab03\Recordings\TaskA3.6" # <--- PATH HERE

# 2. Execute the processing and averaging
print("--- Starting data Extracting, Converting and Averaging ---")
list_of_output_files = process_and_average_s_parameters(
    root_dir=ROOT_DATA_DIR
)

print("\nProcessing complete. Averaged files were saved to:")
print("\n-----------------------------------------------------------------------------------------------------------------")
for file_path in list_of_output_files:
    print(f"- {file_path}")

print("-------------------------------------------------------------------------------------------------------------------")

# 3. Generate Plot
if list_of_output_files:
    print("\n-----^_^ Starting Plot Generation ^_^-----")
    plot_s_parameters_db(
        file_paths=list_of_output_files, 
        output_image_name='Final_SParameter_Magnitude_Plot.png'
    )

# Finding Resonance Frequency
print("\n----- Analysing Resonance Frequencies -----")
# We call the function and store the results in a dictionary
resonance_results = find_global_best_resonance(
        file_paths=list_of_output_files, 
        threshold_db=-10.0  # Common antenna bandwidth threshold
    )

#Display the results
if resonance_results:
     print("----------------------------------------------------")
     print(f"Angle:     {resonance_results['angle_deg']} deg")
     print(f"Frequency: {resonance_results['frequency_mhz']} MHz")
     print(f"Magnitude: {resonance_results['magnitude_db']} dB")
     print("----------------------------------------------------")
else:
    print("No resonance data could be extracted.")


print("\n----- ^_^ Computing radiation pattern ^_^ -----")
angles, mag_db = compute_pattern(file_paths=list_of_output_files, 
                       resonance_freq_mhz=resonance_results["frequency_mhz"]
                       )

print("\n----- ^_^ Analyzing radiation pattern ^_^ -----")
main_angle, [left_c, right_c], opening_angle = analyze_pattern(angles, mag_db)

print("\n----- ^_^ Plotting radiation pattern ^_^ -----")
plot_pattern(angles, mag_db, "horizontal", main_angle, [left_c, right_c], opening_angle, resonance_freq_mhz=resonance_results["frequency_mhz"])