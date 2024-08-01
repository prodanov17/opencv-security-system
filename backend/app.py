from camera import Camera
from datetime import datetime, timedelta
from detection.ml_detection import MLDetection
from detection.hog_detection import HogDetection
from detection.mog_detection import MogDetection
from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory, Response
from notification.smsto_notification import SmsToNotification
import os
from utils import *

app = Flask(__name__)
CORS(app)

config = load_config('config.json')

storage_method = resolve_storage(config['implementations']['storage']['default'])
notification_method = resolve_notification(config['implementations']['notifications']['default'])

camera = Camera(storage_method=storage_method)

@app.route('/arm', methods=['POST'])
def arm():
    data = request.get_json()

    algorithm = MLDetection()

    if 'algorithm' in data:
        if data['algorithm'] == 'hog':
            algorithm = HogDetection()
        elif data['algorithm'] == 'mog':
            algorithm = MogDetection()

    camera.arm(algorithm)
    return jsonify(message="System armed."), 200

@app.route('/disarm', methods=['POST'])
def disarm():
    camera.disarm()
    return jsonify(message="System disarmed."), 200

@app.route('/get-armed', methods=['GET'])
def get_armed():
    return jsonify(armed=camera.armed), 200

@app.route('/motion_detected', methods=['POST'])
def motion_detected():
    data = request.get_json()

    if 'url' in data:
        print("URL: ", data['url'])
        notification = notification_method
        notification.notify("Motion detected! Check the video at " + data['url'])
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

@app.route('/live')
def index():
    return '''
        <html>
        <head>
            <title>Live Stream</title>
        </head>
        <body>
            <h1>Live Video Stream</h1>
            <img src="/video_feed">
        </body>
        </html>
    '''


@app.route('/video_feed')
def video_feed():
    return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/get-logs")
def get_logs():
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
        logs = camera.storage.load(start_date.strftime("%d-%m-%y"), end_date.strftime("%d-%m-%y"))

        reverse_logs = logs[::-1]

        # Return the logs as JSON
        return jsonify({"logs": reverse_logs}), 200

    except ValueError as e:
        # Handle date parsing errors
        return jsonify({"error": "Invalid date format. Please use 'dd-mm-yy' format."}), 400

if __name__ == "__main__":
    app.run(host=config['app']['host'], port=config['app']['port'], debug=config['app']['debug'])
