import sys
from pathlib import Path

import numpy as np
import rerun as rr
from stable_baselines3 import PPO

from envs.drone_env import DroneEnv
from envs.track import TRACK_SEED
from viz.drone_model import log_drone_model, log_drone_pose
from viz.live import send_layout
from viz.track_model import log_track

runs = Path(__file__).parent.parent / "runs"
model_path = sys.argv[1] if len(sys.argv) > 1 else max(runs.glob("*/model.zip"))  # domyślnie najnowszy
model = PPO.load(model_path, device="cpu")

env = DroneEnv(track_seed=TRACK_SEED)
obs, _ = env.reset()

rr.init("replay", spawn=True)
send_layout()
log_track(env.pillars)
log_drone_model()
rr.set_time("time", duration=0.0)
log_drone_pose(env.pos, [0, 0, 0, 1])

path = [env.pos]
done = False
while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    path.append(env.pos)

    rr.set_time("time", duration=env.t)
    log_drone_pose(env.pos, [0, 0, 0, 1])
    rr.log("path", rr.LineStrips3D([path], colors=[0, 200, 255]))
    rr.log("speed", rr.Scalars(np.linalg.norm(env.vel)))

print(model_path, info["result"] or "timeout", f"{info['time']:.2f} s")
