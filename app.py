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
            "cmd.exe", "/c",  # Use cmd to run a series of commands
            "E:\\PYTHON\\VisionaryModel\\VisionaryModel\\vm-od\\Scripts\\activate.bat && python object_detection_v2.py"
        ]
        # Start subprocess in the background
        subprocess.Popen(command, shell=True)

    # Run the model in a separate thread to avoid blocking
    threading.Thread(target=run_model).start()

    # Open object detection page in a new tab
    webbrowser.open_new_tab(url_for("object_detection", _external=True))

    return redirect(url_for("object_detection"))

# Route to Display Object Detection HTML Page
@app.route("/object-detection")
def object_detection():
    return render_template("object_detection.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=False)
