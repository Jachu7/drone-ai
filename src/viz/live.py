import rerun as rr
import rerun.blueprint as rrb


def send_layout():
    rr.send_blueprint(rrb.Blueprint(rrb.Horizontal(
        rrb.Spatial3DView(name="tor", origin="/", eye_controls=rrb.EyeControls3D(tracking_entity="/drone")),
        rrb.Spatial3DView(name="kamera za dronem", origin="/drone", contents="/**"),
        rrb.TimeSeriesView(name="prędkość", origin="/speed"),
    )))
