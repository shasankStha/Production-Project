from flask import Blueprint, Response, request, current_app
from src.services.live_stream import generate_frames, release_camera
from src.utils.extensions import db

video_bp = Blueprint("video", __name__)

@video_bp.route("/video_feed")
def video_feed():
    try:
        attendance = request.args.get("attendance", default=None, type=str)

        if attendance is not None:
            attendance = attendance.lower() == "true"
        else:
            attendance = False
            
        return Response(generate_frames(attendance, current_app._get_current_object(), db), mimetype="multipart/x-mixed-replace; boundary=frame")
    except Exception as e:
        print(f"[ERROR] An error occurred in video_feed: {str(e)}")
        return Response("Error: Unable to stream video.", status=500)