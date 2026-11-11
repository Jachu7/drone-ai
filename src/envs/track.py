import numpy as np

# Track 100 x 50 m, height 20 m. z = up.

TRACK_MIN = (-2.5, -25.0, 0.0)
TRACK_MAX = (97.5, 25.0, 20.0)

START_POS = (0.0, 0.0, 1.0)  # drone rests on the start box
START_BOX_SIZE = 1.0         # m

GOAL_POS = (95.0, 0.0, 1.0)  # goal center
GOAL_SIZE = 1.0              # m, cube edge

PILLAR_COUNT = 15
PILLAR_RADIUS = 2.5          # m
PILLAR_CLEARANCE = 10.0      # m, min. x distance from pillar edge to start and goal

TRACK_SEED = 0               # pillar layout for training and replay, None = new each episode


def random_pillars(seed=None):
    """Random pillar centers (x, y), shape [PILLAR_COUNT, 2]. Inside the track, no overlap."""
    rng = np.random.default_rng(seed)
    lo = [START_POS[0] + PILLAR_CLEARANCE + PILLAR_RADIUS, TRACK_MIN[1] + PILLAR_RADIUS]
    hi = [GOAL_POS[0] - PILLAR_CLEARANCE - PILLAR_RADIUS, TRACK_MAX[1] - PILLAR_RADIUS]
    pillars = []
    while len(pillars) < PILLAR_COUNT:
        p = rng.uniform(lo, hi)
        if all(np.linalg.norm(p - q) >= 2 * PILLAR_RADIUS for q in pillars):
            pillars.append(p)
    return np.array(pillars)


def check(pos, pillars):
    if np.all(np.abs(pos - GOAL_POS) <= GOAL_SIZE / 2):
        return "goal"
    if np.any(pos < TRACK_MIN) or np.any(pos > TRACK_MAX):
        return "crash"
    if np.any(np.linalg.norm(pillars - pos[:2], axis=1) < PILLAR_RADIUS):
        return "crash"
    if np.all(np.abs(pos[:2] - START_POS[:2]) < START_BOX_SIZE / 2) and pos[2] < START_POS[2]:
        return "crash"
    return None
