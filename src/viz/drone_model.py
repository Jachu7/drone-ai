from pathlib import Path

import rerun as rr

MESH_PATH = Path(__file__).parent.parent / "assets" / "fpv_drone_5inch.stl"


def log_drone_model():
    """Loguje kształt drona raz. Przód = oś +x."""
    rr.log(
        "drone/mesh",
        rr.Transform3D(translation=[0.005, 0, -0.01], scale=0.001),  # mm -> m, środek między silnikami w (0, 0, 0)
        rr.Asset3D(path=MESH_PATH, albedo_factor=[100, 30, 30]),
        static=True,
    )
    rr.log("drone/arrow", rr.Arrows3D(origins=[[0, 0, 0.045]], vectors=[[0.1, 0, 0]], colors=[255, 255, 255], radii=0.004), static=True)


def log_drone_pose(pos, quat_xyzw):
    """Przesuwa i obraca model. Wołaj co krok symulacji."""
    rr.log("drone", rr.Transform3D(translation=pos, rotation=rr.Quaternion(xyzw=quat_xyzw)))


if __name__ == "__main__":
    rr.init("drone_model", spawn=True)
    log_drone_model()
