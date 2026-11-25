import numpy as np
import matplotlib.pyplot as plt


def plot_pattern(
    angles_deg,
    mag_db,
    orientation: str,
    main_angle,
    crossings,
    opening_angle,
    resonance_freq_mhz
):
    """
    Polar radiation pattern with:
      - main direction
      - opening angle edges
      - wrap-safe opening angle arc + label
    """

    # --------------------------------------------------
    # Prepare data
    # --------------------------------------------------
    theta = np.deg2rad(angles_deg)
    theta = np.append(theta, theta[0])
    mag_db = np.append(mag_db, mag_db[0])

    # --------------------------------------------------
    # Create polar plot
    # --------------------------------------------------
    fig, ax = plt.subplots(
        subplot_kw={"projection": "polar"},
        figsize=(8, 8)
    )

    ax.plot(theta, mag_db, 'o-', linewidth=2)
    ax.fill(theta, mag_db, alpha=0.15)

    # --------------------------------------------------
    # Main direction
    # --------------------------------------------------
    # ax.plot(
    #     [np.deg2rad(main_angle), np.deg2rad(main_angle)],
    #     [mag_db.min(), 0],
    #     'r--',
    #     linewidth=2,
    #     label="Main direction"
    # )

    # --------------------------------------------------
    # Opening angle (from crossings)
    # --------------------------------------------------
    # if len(crossings) == 2:
    #     left_c, right_c = crossings

    #     # Edge lines
    #     for c in crossings:
    #         ax.plot(
    #             [np.deg2rad(c), np.deg2rad(c)],
    #             [mag_db.min(), 0],
    #             'g--',
    #             linewidth=1.5
    #         )

    #     # Filled wedge
    #     ax.fill_between(
    #         [np.deg2rad(left_c), np.deg2rad(right_c)],
    #         mag_db.min(),
    #         0,
    #         color='green',
    #         alpha=0.10
    #     )

        # --------------------------------------------------
        # Opening angle ARC (wrap-safe)
        # --------------------------------------------------
        # arc_radius = -15.0  # dB level for arc (always visible)

        # if left_c <= right_c:
        #     # Normal case (no wrap)
        #     arc_angles = np.linspace(
        #         np.deg2rad(left_c),
        #         np.deg2rad(right_c),
        #         200
        #     )
        #     ax.plot(
        #         arc_angles,
        #         np.full_like(arc_angles, arc_radius),
        #         color='green',
        #         linewidth=2
        #     )
        #     mid_angle = 0.5 * (left_c + right_c)

        # else:
        #     # Wrap-around case (crosses 0°)
        #     arc1 = np.linspace(
        #         np.deg2rad(left_c),
        #         np.deg2rad(360),
        #         100
        #     )
        #     arc2 = np.linspace(
        #         0,
        #         np.deg2rad(right_c),
        #         100
        #     )

        #     ax.plot(
        #         arc1,
        #         np.full_like(arc1, arc_radius),
        #         color='green',
        #         linewidth=2
        #     )
        #     ax.plot(
        #         arc2,
        #         np.full_like(arc2, arc_radius),
        #         color='green',
        #         linewidth=2
        #     )

        #     mid_angle = (left_c + (right_c + 360)) / 2
        #     if mid_angle >= 360:
        #         mid_angle -= 360

        # # --------------------------------------------------
        # # Arc label
        # # --------------------------------------------------
        # ax.text(
        #     np.deg2rad(mid_angle),
        #     arc_radius + 1.0,
        #     f"{opening_angle:.1f}°",
        #     color="green",
        #     fontsize=12,
        #     fontweight="bold",
        #     ha="center",
        #     va="center"
        # )

    # --------------------------------------------------
    # Polar formatting (antenna standard)
    # --------------------------------------------------
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    tick_angles = np.arange(0, 360, 15)
    tick_labels = [str(a if a <= 180 else a - 360) for a in tick_angles]
    ax.set_thetagrids(tick_angles, tick_labels)

    ax.set_rlim(mag_db.min(), 0)
    ax.set_rlabel_position(225)

    # --------------------------------------------------
    # Title & legend
    # --------------------------------------------------
    if len(crossings) == 2:
        title = (
            f"{orientation.capitalize()} Radiation Pattern @{resonance_freq_mhz} MHz\n"
            # f"Main direction: {main_angle:.1f}° | Opening angle: {opening_angle:.1f}°"
        )
    else:
        title = (
            f"{orientation.capitalize()} Radiation Pattern @{resonance_freq_mhz} MHz\n"
            # f"Main direction: {main_angle:.1f}° | Opening angle: Not detectable"
        )

    ax.set_title(title, pad=20)
    ax.legend(loc="upper right")

    plt.tight_layout()
    plt.show()
