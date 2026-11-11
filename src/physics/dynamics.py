import numpy as np

from physics.drone import DRAG_COEFF, FRONTAL_AREA, MASS, MAX_THRUST
from physics.world import AIR_DENSITY, DT, GRAVITY

GRAVITY_VEC = np.array([0.0, 0.0, -GRAVITY])


def step(pos, vel, thrust, wind=0.0, dt=DT):
    norm = np.linalg.norm(thrust, axis=-1, keepdims=True)
    thrust = thrust * np.minimum(1.0, MAX_THRUST / np.maximum(norm, 1e-9))  # cap at MAX_THRUST, keep direction

    air_vel = vel - wind  # velocity relative to air
    speed = np.linalg.norm(air_vel, axis=-1, keepdims=True)
    drag = -0.5 * AIR_DENSITY * DRAG_COEFF * FRONTAL_AREA * speed * air_vel

    acc = GRAVITY_VEC + (thrust + drag) / MASS
    vel = vel + acc * dt
    pos = pos + vel * dt
    return pos, vel
