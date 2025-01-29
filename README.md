# Visionary Model (Object, Action & Emotion Detection with Flask Website)

This project integrates **Object Detection, Action Detection, and Emotion Detection** models into a **Flask-based website**. Each model runs in its own virtual environment and can be accessed through the website.

---

## 📁 Project Structure

```
E:\PYTHON\VisionaryModel\VisionaryModel
│── vm-od\                     # Virtual environment for Object Detection
│── vm-ad\                     # Virtual environment for Action Detection
│── vm-ed\                     # Virtual environment for Emotion Detection
│── vm-env\                    # Virtual environment for Flask website
│── object_detection_v2.py     # Object detection model script
│── action_detection_v2.py     # Action detection model script
│── emotion_detection_v2.py    # Emotion detection model script
│── app.py                     # Flask web application
│── templates\                 # HTML templates for website
│    ├── index.html            # Main homepage
│    ├── object_detection.html # Object detection page
│    ├── action_detection.html # Action detection page
│    ├── emotion_detection.html# Emotion detection page
│── static\                    # CSS, JS, and images
│── run_all.bat                # Batch script to run everything
│── stop_all.bat               # Batch script to stop all models
│── README.md                  # Documentation
```

---

## 🔧 Installation Steps

### Step 1: Clone or Copy the Project
Ensure you have the **complete project structure** on your local machine.

### Step 2: Install Python (if not installed)
- Install Python **3.10**.(higher version may causes error)
- Add Python to **system PATH** during installation.

### Step 3: Install Virtual Environments & Dependencies
Each model runs in its own virtual environment.

#### Object Detection Setup
```sh
cd E:\PYTHON\VisionaryModel\VisionaryModel\vm-od
Scripts\activate
pip install -r requirements.txt
```

#### Action Detection Setup
```sh
cd E:\PYTHON\VisionaryModel\VisionaryModel\vm-ad
Scripts\activate
pip install -r requirements.txt
```

#### Emotion Detection Setup
```sh
cd E:\PYTHON\VisionaryModel\VisionaryModel\vm-ed
Scripts\activate
pip install -r requirements.txt
```

#### Flask Website Setup
```sh
cd E:\PYTHON\VisionaryModel\VisionaryModel\vm-env
Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### Option 1: Run Everything Together (Recommended)
Use the provided batch script to start all models and the website.

1. Navigate to the project folder:
```sh
cd E:\PYTHON\VisionaryModel\VisionaryModel
```

2. Run the batch script:
```sh
run_all.bat
```

This will start all models in the background and launch the Flask website.

### Option 2: Run Manually (One by One)
If you want to start each model separately:

#### Run Object Detection
```sh
cd E:\PYTHON\VisionaryModel\VisionaryModel\vm-od
Scripts\activate
python E:\PYTHON\VisionaryModel\VisionaryModel\object_detection_v2.py
```

#### Run Action Detection
```sh
cd E:\PYTHON\VisionaryModel\VisionaryModel\vm-ad
Scripts\activate
python E:\PYTHON\VisionaryModel\VisionaryModel\action_detection_v2.py
```

#### Run Emotion Detection
```sh
cd E:\PYTHON\VisionaryModel\VisionaryModel\vm-ed
Scripts\activate
python E:\PYTHON\VisionaryModel\VisionaryModel\emotion_detection_v2.py
```

#### Run Flask Website
```sh
cd E:\PYTHON\VisionaryModel\VisionaryModel\vm-env
Scripts\activate
python E:\PYTHON\VisionaryModel\VisionaryModel\app.py
```

---

## 🌐 Using the Website

Once the website is running, open a browser and visit:

http://127.0.0.1:5555

From the homepage, you can select:

- Object Detection (Runs on http://127.0.0.1:5001)
- Action Detection (Runs on http://127.0.0.1:5002)
- Emotion Detection (Runs on http://127.0.0.1:5003)

Each model starts automatically when the respective page is opened.

---

## ❌ Stopping the Models

To stop all running models and the website, use:
```sh
stop_all.bat
```
OR manually stop each process via Task Manager (python.exe or pythonw.exe).

---

## ⚠️ Troubleshooting

1. **Flask Website Not Opening?**
   - Check if Flask is running:
     ```sh
     netstat -ano | findstr :5555
     ```
   - If nothing appears, restart the website manually.

2. **Camera Not Working for a Model?**
   - Close any running Python instances in Task Manager.
   - Ensure the webcam is not already in use by another model.

3. **Dependencies Not Found?**
   - Activate the correct virtual environment before running any script.
   - Reinstall dependencies:
     ```sh
     pip install -r requirements.txt
     ```

---

## 📌 Future Enhancements

- Optimize model performance for real-time processing.
- Deploy using Docker for better portability.
- Add support for more models (e.g., face recognition, gesture detection).

---

✅ Project is now fully functional and ready to use! 🚀
