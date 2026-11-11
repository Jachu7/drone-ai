import numpy as np
import rerun as rr

from envs.track import GOAL_POS, GOAL_SIZE, PILLAR_RADIUS, START_BOX_SIZE, START_POS, TRACK_MAX, TRACK_MIN, random_pillars


def log_track(pillars):
    """Logs the track once: bounds, start, goal and pillars (x, y centers from random_pillars)."""
    rr.log("/", rr.ViewCoordinates.RIGHT_HAND_Z_UP, static=True)

    lo, hi = np.array(TRACK_MIN), np.array(TRACK_MAX)
    rr.log("track/bounds", rr.Boxes3D(mins=[lo], sizes=[hi - lo], colors=[255, 255, 255], radii=0.05), static=True)

    s = START_BOX_SIZE
    start_center = [START_POS[0], START_POS[1], START_POS[2] - s / 2]  # box top face at start height
    rr.log(
        "track/start",
        rr.Boxes3D(centers=[start_center], sizes=[[s, s, s]], colors=[0, 200, 0], fill_mode=rr.components.FillMode.Solid),
        static=True,
    )

    g = GOAL_SIZE
    rr.log(
        "track/goal",
        rr.Boxes3D(centers=[GOAL_POS], sizes=[[g, g, g]], colors=[255, 0, 0, 100], fill_mode=rr.components.FillMode.Solid),
        static=True,
    )

    height = hi[2] - lo[2]
    centers = np.hstack([pillars, np.full((len(pillars), 1), lo[2] + height / 2)])  # pillars from ground to ceiling
    rr.log(
        "track/pillars",
        rr.Cylinders3D(
            centers=centers, lengths=height, radii=PILLAR_RADIUS, colors=[200, 0, 0], fill_mode=rr.components.FillMode.Solid
        ),
        static=True,
    )


if __name__ == "__main__":
    from viz.drone_model import log_drone_model, log_drone_pose

    rr.init("track", spawn=True)
    log_track(random_pillars())
    log_drone_model()
    log_drone_pose(START_POS, [0, 0, 0, 1])
