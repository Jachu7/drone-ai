import gymnasium as gym
import numpy as np

from envs.track import GOAL_POS, START_POS, check, random_pillars
from physics import dynamics
from physics.drone import MASS, MAX_SPEED, MAX_THRUST
from physics.world import DT

MAX_TIME = 30.0  # s
GOAL = np.array(GOAL_POS)


class DroneEnv(gym.Env):
    def __init__(self, track_seed=None):
        self.track_seed = track_seed  # None = nowy układ filarów co epizod
        self.action_space = gym.spaces.Box(-1.0, 1.0, (3,), np.float32)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, (15,), np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.pillars = random_pillars(self.np_random if self.track_seed is None else self.track_seed)
        self.pos = np.array(START_POS)
        self.vel = np.zeros(3)
        self.t = 0.0
        self.dist = np.linalg.norm(GOAL - self.pos)
        return self._obs(), {}

    def step(self, action):
        thrust = np.asarray(action) * MAX_THRUST - MASS * dynamics.GRAVITY_VEC  # akcja 0 = zawis
        self.pos, self.vel = dynamics.step(self.pos, self.vel, thrust)
        self.t += DT

        dist = np.linalg.norm(GOAL - self.pos)
        reward = self.dist - dist - 0.01  # postęp do mety, kara za czas
        self.dist = dist

        result = check(self.pos, self.pillars)
        if result == "goal":
            reward += 100
        if result == "crash":
            reward -= 100

        terminated = result is not None
        truncated = self.t >= MAX_TIME
        return self._obs(), reward, terminated, truncated, {"result": result, "time": self.t}

    def _obs(self):
        rel = self.pillars - self.pos[:2]
        nearest = rel[np.argsort(np.linalg.norm(rel, axis=1))[:3]]  # 3 najbliższe filary
        return np.concatenate([
            (GOAL - self.pos) / 100,
            self.pos / 100,
            self.vel / MAX_SPEED,
            nearest.ravel() / 10,
        ]).astype(np.float32)
