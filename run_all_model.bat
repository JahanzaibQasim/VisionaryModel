@echo off
echo Starting all models and the website...

REM Base path
set BASE_PATH=E:\PYTHON\VisionaryModel\VisionaryModel

REM Start Object Detection Model
start cmd.exe /k "cd %BASE_PATH%\vm-od && call Scripts\activate && python %BASE_PATH%\object_detection_v2.py"

REM Start Action Detection Model
start cmd.exe /k "cd %BASE_PATH%\vm-ad && call Scripts\activate && python %BASE_PATH%\action_detection_v2.py"

REM Start Emotion Detection Model
start cmd.exe /k "cd %BASE_PATH%\vm-ed && call Scripts\activate && python %BASE_PATH%\emotion_detection_v2.py"

REM Start Website (Flask app)
start cmd.exe /k "cd %BASE_PATH%\vm-env && call Scripts\activate && python %BASE_PATH%\app.py"

echo All models and the website are starting...
