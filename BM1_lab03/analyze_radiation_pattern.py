import numpy as np

def analyze_pattern(angles_deg, mag_db, threshold=-3.0):
    """
    Computes:
      - main direction
      - left/right -3 dB crossings around main lobe
      - opening angle (short arc)
    """

    angles_deg = np.asarray(angles_deg)
    mag_db = np.asarray(mag_db)

    # --------------------------------------------------
    # Main direction
    # --------------------------------------------------
    idx_max = np.argmax(mag_db)
    main_angle = angles_deg[idx_max]

    # --------------------------------------------------
    # Find threshold crossings
    # --------------------------------------------------
    crossings = []
    for i in range(len(angles_deg) - 1):
        y1, y2 = mag_db[i], mag_db[i + 1]
        if (y1 - threshold) * (y2 - threshold) < 0:
            x1, x2 = angles_deg[i], angles_deg[i + 1]
            frac = (threshold - y1) / (y2 - y1)
            crossings.append(x1 + frac * (x2 - x1))

    if len(crossings) != 2:
        return main_angle, [], 0.0

    c1, c2 = crossings

    # --------------------------------------------------
    # Signed angular distances from main lobe
    # --------------------------------------------------
    def signed_delta(a, ref):
        """Return angle difference in (-180, 180]"""
        return (a - ref + 180) % 360 - 180

    d1 = signed_delta(c1, main_angle)
    d2 = signed_delta(c2, main_angle)

    # --------------------------------------------------
    # Assign left/right correctly
    # --------------------------------------------------
    if d1 < 0 and d2 > 0:
        left_c, right_c = c1, c2
    elif d2 < 0 and d1 > 0:
        left_c, right_c = c2, c1
    else:
        # fallback (rare numerical edge case)
        if abs(d1) < abs(d2):
            left_c, right_c = c1, c2
        else:
            left_c, right_c = c2, c1

    # --------------------------------------------------
    # Opening angle = short arc
    # --------------------------------------------------
    opening_angle = abs(d1) + abs(d2)

    return main_angle, [left_c, right_c], opening_angle
