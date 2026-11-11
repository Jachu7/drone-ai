import numpy as np
import rerun as rr

from envs.track import GOAL_POS, START_POS, check, random_pillars
from physics.drone import MASS
from physics.dynamics import GRAVITY_VEC, step
from physics.world import DT
from viz.drone_model import log_drone_model, log_drone_pose
from viz.live import send_layout
from viz.track_model import log_track


def controller(pos, vel):
    acc = 1.0 * (np.array(GOAL_POS) - pos) - 1.5 * vel
    acc *= min(1.0, 30.0 / np.linalg.norm(acc))
    return MASS * (acc - GRAVITY_VEC)


pillars = random_pillars()
rr.init("demo_flight", spawn=True)
send_layout()
log_track(pillars)
log_drone_model()

pos, vel = np.array(START_POS), np.zeros(3)
path = [pos]
result = None
t = 0.0
while result is None and t < 30:
    pos, vel = step(pos, vel, controller(pos, vel))
    t += DT
    path.append(pos)
    result = check(pos, pillars)

    rr.set_time("time", duration=t)
    log_drone_pose(pos, [0, 0, 0, 1])
    rr.log("path", rr.LineStrips3D([path], colors=[0, 200, 255]))
    rr.log("speed", rr.Scalars(np.linalg.norm(vel)))

print(result or "timeout", f"{t:.2f} s")
