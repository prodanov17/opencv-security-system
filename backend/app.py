from camera import Camera
from datetime import datetime, timedelta
from detection.ml_detection import MLDetection
from detection.hog_detection import HogDetection
from detection.mog_detection import MogDetection
from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory, Response
from models import db, Camera as CameraModel, Detection
from dotenv import load_dotenv
import os
from utils import load_config, resolve_storage, resolve_notification

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

config = load_config('config.json')

storage_method = resolve_storage(
    config['implementations']['storage']['default']
)
notification_method = resolve_notification(
    config['implementations']['notifications']['default']
)


def initialize_cameras():
    with app.app_context():
        db.create_all()
        cameras_query = CameraModel.query.all()
        cameras = {
            camera.id: Camera(
                id=camera.id,
                storage_method=resolve_storage("LocalStorage"),
                name=camera.name,
                armed=camera.armed,
                detection_method=camera.algorithm,
                capture=camera.source,
                model=camera
            )
            for camera in cameras_query
        }
    return cameras


def refresh_cameras():
    global cameras
    cameras_query = CameraModel.query.all()
    cameras = {
        camera.id: Camera(
            id=camera.id,
            storage_method=resolve_storage("LocalStorage"),
            name=camera.name,
            armed=camera.armed,
            detection_method=camera.algorithm,
            capture=camera.source,
            model=camera
        )
        for camera in cameras_query
    }


# Initialize cameras
cameras = initialize_cameras()


# camera = Camera(storage_method=storage_method)

@app.route('/cameras', methods=['GET'])
def get_cameras():
    cameras_query = CameraModel.query.all()
    return jsonify({"cameras": [camera.serialize() for camera in cameras_query]}), 200


@app.route('/cameras/<int:camera_id>', methods=['GET'])
def get_camera(camera_id):
    if camera_id not in cameras:
        return jsonify(message="Camera not found."), 404

    camera = CameraModel.query.get(camera_id)
    return jsonify(camera.serialize()), 200


@app.route('/cameras/<int:camera_id>', methods=['DELETE'])
def delete_camera(camera_id):
    if camera_id not in cameras:
        return jsonify(message="Camera not found."), 404

    camera = CameraModel.query.get(camera_id)
    db.session.delete(camera)
    db.session.commit()
    cameras.pop(camera_id)

    return jsonify(message="Camera deleted."), 200


@app.route('/cameras/<int:camera_id>/arm', methods=['POST'])
def arm(camera_id):
    if camera_id not in cameras:
        return jsonify(message="Camera not found."), 404

    if cameras is None:
        initialize_cameras()

    data = request.get_json()

    algorithm = MLDetection()

    if 'algorithm' in data:
        if data['algorithm'] == 'hog':
            algorithm = HogDetection()
        elif data['algorithm'] == 'mog':
            algorithm = MogDetection()

    camera = cameras[camera_id]
    camera.arm(algorithm)

    return jsonify(message="System armed."), 200


@app.route('/cameras/<int:camera_id>/disarm', methods=['POST'])
def disarm(camera_id):
    if camera_id not in cameras:
        return jsonify(message="Camera not found."), 404

    cameras[camera_id].disarm()
    return jsonify(message="System disarmed."), 200


@app.route('/cameras/<int:camera_id>/get-armed', methods=['GET'])
def get_armed(camera_id):
    if camera_id not in cameras:
        return jsonify(message="Camera not found."), 404

    camera = CameraModel.query.get(camera_id)
    return jsonify(armed=camera.armed), 200


@app.route('/cameras/<int:camera_id>', methods=['PATCH'])
def update_camera(camera_id):
    if camera_id not in cameras:
        return jsonify(message="Camera not found."), 404

    camera = cameras[camera_id]
    data = request.get_json()

    if 'name' in data:
        camera.model.name = data['name']
    if 'source' in data:
        camera.model.source = data['source']
    if 'algorithm' in data:
        camera.model.algorithm = data['algorithm']
    if 'armed' in data:
        camera.model.armed = data['armed']
    if 'notifications_enabled' in data:
        camera.model.notifications_enabled = data['notifications_enabled']

    db.session.add(camera.model)
    db.session.commit()

    refresh_cameras()

    return jsonify(message="Camera updated."), 200


@app.route('/cameras', methods=['POST'])
def add_camera():
    data = request.get_json()

    if 'name' not in data:
        return jsonify(message="Missing 'name' in request."), 422
    if 'source' not in data:
        return jsonify(message="Missing 'source' in request."), 422
    if 'algorithm' not in data:
        return jsonify(message="Missing 'algorithm' in request."), 422

    new_camera = CameraModel(
        name=data['name'],
        source=data['source'],
        algorithm=data['algorithm'],
        armed=False
    )
    db.session.add(new_camera)
    db.session.commit()

    refresh_cameras()

    return jsonify(message="Camera added"), 201


@app.route('/cameras/<int:camera_id>/motion', methods=['POST'])
def motion_detected(camera_id):
    data = request.get_json()

    camera = CameraModel.query.get(camera_id)

    if 'url' in data:
        print("URL: ", data['url'])
        if camera.notifications_enabled:
            notification = notification_method
            notification.notify(f"{camera.name}: Motion detected! Check the video at {data['url']}")
        db.session.add(Detection(camera_id=camera_id, url=data['url']))
        db.session.commit()
    else:
        print("'url' not in incoming data")

    return jsonify({}), 201


@app.route('/storage/videos/<path:video_name>', methods=['GET'])
def serve_video(video_name):
    video_directory = os.path.join(os.getcwd(), 'storage/videos')
    file_path = os.path.join(video_directory, video_name)

    if not os.path.isfile(file_path):
        return jsonify(message="File not found."), 404

    return send_from_directory("storage/videos", video_name)


@app.route('/cameras/<int:camera_id>/video_feed')
def video_feed(camera_id):
    if camera_id not in cameras:
        return jsonify(message="Camera not found."), 404

    camera = cameras[camera_id]

    return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/cameras/logs")
def get_detection_logs():
    try:
        # Retrieve start and end dates from query parameters
        start_date_str = request.args.get("startDate", datetime.now().strftime("%d-%m-%y"))
        end_date_str = request.args.get("endDate", datetime.now().strftime("%d-%m-%y"))

        # Parse dates from query parameters
        start_date = datetime.strptime(start_date_str, "%d-%m-%y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%y")

        # Ensure end_date is after start_date
        if end_date < start_date:
            return jsonify({"error": "End date must be after start date"}), 400

        end_date += timedelta(days=1)

        # Load logs based on date range
        logs = Detection.query.filter(Detection.timestamp >= start_date, Detection.timestamp <= end_date).all()

        # Return the logs as JSON
        return jsonify({"logs": [log.serialize() for log in logs]}), 200

    except ValueError as e:
        # Handle date parsing errors
        return jsonify({"error": "Invalid date format. Please use 'dd-mm-yy' format."}), 400


if __name__ == "__main__":
    app.run(host=config['app']['host'], port=config['app']['port'], debug=config['app']['debug'])
