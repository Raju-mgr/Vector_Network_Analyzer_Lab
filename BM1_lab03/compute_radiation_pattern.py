import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def compute_pattern(
    file_paths: list,
    resonance_freq_mhz: float
):
    """
    Parameters
    ----------
    file_paths : list
        CSV files for different angles (one file per angle).
    resonance_freq_mhz : float
        Known resonance frequency in MHz.
    """
    # --------------------------------------------------
    # Frequency window 10 MHz
    # --------------------------------------------------
    f_start = resonance_freq_mhz - 5
    f_end = resonance_freq_mhz + 5

    # --------------------------------------------------
    # Read and average data
    # --------------------------------------------------
    average_mag = {}

    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)

            freq_mhz = pd.to_numeric(df["Frequency"], errors="coerce") / 1e6
            s21_mag = pd.to_numeric(df["S21_Mag"], errors="coerce")

            mask = (freq_mhz >= f_start) & (freq_mhz <= f_end)
            if not mask.any():
                continue

            # Average in linear domain
            mean_linear = np.mean(s21_mag[mask])

            raw_angle = float(df["Angle_deg"].iloc[0])
            # ----map angle immediatly to 0-360 degree----
            angle = raw_angle % 360.0 
            average_mag[angle] = mean_linear

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    if not average_mag:
        raise RuntimeError("No valid data found in ±5 MHz window.")
    
    # --------------------------------------------------
    # Prepare angle + magnitude arrays
    # --------------------------------------------------
    angles = np.array(sorted(average_mag.keys()))
    linear_mag = np.array([average_mag[a] for a in angles])

    # -------------------------------------------------- 
    # Resolution check (should be 15°) 
    # --------------------------------------------------
    diffs = np.diff(angles)
    if not np.allclose(diffs, 15):
        print("Warning: angular steps are not consistently 15°")
        print("Detected steps:", np.unique(diffs))

    # --------------------------------------------------
    # Convert to dB and normalize (max = 0 dB)
    # --------------------------------------------------
    eps = 1e-12
    mag_db = 20 * np.log10(np.maximum(linear_mag, eps))
    mag_db -= mag_db.max()
    print(f"Normalized s21 mag_db: \n{mag_db}")
    print(f"Angles: \n{angles}")

    return angles, mag_db
