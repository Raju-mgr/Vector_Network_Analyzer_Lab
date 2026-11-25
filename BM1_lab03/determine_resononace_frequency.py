import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from typing import List, Dict

def find_global_best_resonance(file_paths: List[str], threshold_db: float = -10.0) -> Dict:
    """
    Analyzes S11 data and returns the single best resonance frequency 
    (maximum return loss/deepest dip) across all provided files.
    """
    global_best = None

    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            if df.empty: continue
            
            angle = df['Angle_deg'].iloc[0]
            freqs = pd.to_numeric(df['Frequency'], errors='coerce').values / 1e6 # Convert to MHz unit
            s11_mag = pd.to_numeric(df['S11_Mag'], errors='coerce').values
            s11_db = 20 * np.log10(s11_mag)

            # --- Peak Finding ---
            inverted_s11 = -s11_db
            peaks, _ = find_peaks(inverted_s11, prominence=1.0)
            
            for peak_idx in peaks:
                db_val = s11_db[peak_idx]
                f_res = freqs[peak_idx]
                
                # Check if this dip is deeper than our current best
                if db_val <= threshold_db:
                    if global_best is None or db_val < global_best['magnitude_db']:
                        global_best = {
                            'angle_deg': angle,
                            'frequency_mhz': round(f_res, 2),
                            'magnitude_db': round(db_val, 2)
                        }

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    return global_best
