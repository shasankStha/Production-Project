from flask import Blueprint, Response, request
from src.services.live_stream import generate_frames, release_camera

video_bp = Blueprint("video", __name__)

@video_bp.route("/video_feed")
def video_feed():
    try:
        attendance = request.args.get("attendance", default=None, type=str)

        if attendance is not None:
            attendance = attendance.lower() == "true"
            return Response(generate_frames(attendance), mimetype="multipart/x-mixed-replace; boundary=frame")

            
        return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
    except Exception as e:
        print(f"[ERROR] An error occurred in video_feed: {str(e)}")
        return Response("Error: Unable to stream video.", status=500)
    
@video_bp.route("/disconnect", methods=["POST"])
def disconnect():
    try:
        release_camera()
        return {"message": "Camera released successfully"}, 200
    except Exception as e:
        print(f"[ERROR] Failed to release camera: {str(e)}")
        return {"error": str(e)}, 500