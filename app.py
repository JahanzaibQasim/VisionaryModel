from flask import Flask, render_template, redirect, url_for
import subprocess
import webbrowser
import threading
import os

app = Flask(__name__)

# Index Route (Main Page)
@app.route("/")
def index():
    return render_template("index.html")

# Route to Start Object Detection
@app.route("/start-model")
def start_model():
    def run_model():
        # Use the subprocess to activate the virtual environment and run the script
        command = [
            "cmd.exe", "/c",
            "E:\\PYTHON\\VisionaryModel\\VisionaryModel\\vm-od\\Scripts\\activate.bat && python object_detection_v2.py"
        ]
        subprocess.Popen(command, shell=True)

    threading.Thread(target=run_model).start()

    # Open object detection page on port 5001 directly
    webbrowser.open_new_tab("http://127.0.0.1:5001")
    
    return redirect(url_for("index"))

# Route to Start Action Detection
@app.route("/start-action-model")
def start_action_model():
    def run_action_model():
        # Activate virtual environment and run action detection model
        command = [
            "cmd.exe", "/c",
            "E:\\PYTHON\\VisionaryModel\\VisionaryModel\\vm-ad\\Scripts\\activate.bat && python action_detection_v2.py"
        ]
        subprocess.Popen(command, shell=True)

    threading.Thread(target=run_action_model).start()

    # Open action detection page on port 5002
    webbrowser.open_new_tab("http://127.0.0.1:5002")

    return redirect(url_for("index"))

# Route to Display Object Detection HTML Page
@app.route("/object-detection")
def object_detection():
    return render_template("object_detection.html")

# Route to Display Action Detection HTML Page
@app.route("/action-detection")
def action_detection():
    return render_template("action_detection_v2.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=False)
