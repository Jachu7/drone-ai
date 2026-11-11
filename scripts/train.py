import sys
from datetime import datetime
from pathlib import Path

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.env_util import make_vec_env

from envs.drone_env import DroneEnv
from envs.track import TRACK_SEED

N_ENVS = 8
steps = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000


class FlightStats(BaseCallback):
    def _on_step(self):
        for info, done in zip(self.locals["infos"], self.locals["dones"]):
            if done:
                goal = info["result"] == "goal"
                self.logger.record_mean("flight/goal_rate", float(goal))
                if goal:
                    self.logger.record_mean("flight/goal_time", info["time"])
        return True


run_dir = Path(__file__).parent.parent / "runs" / datetime.now().strftime("%Y-%m-%d_%H-%M")
env = make_vec_env(DroneEnv, n_envs=N_ENVS, env_kwargs={"track_seed": TRACK_SEED})
model = PPO("MlpPolicy", env, tensorboard_log=run_dir, device="cpu", verbose=1)

try:
    model.learn(steps, callback=FlightStats())
except KeyboardInterrupt:
    pass

model.save(run_dir / "model")
print("zapisano", run_dir / "model.zip")
