# How to Run the program.

### Have Python installed on computer

### Then in the directory of Team24_RPS run
    python -m venv rps_env
###    
    windows: rps_env\Scripts\activate
    macOS/Linux: source rps_env/bin/activate
###
    pip install opencv-python mediapipe numpy

### Next Run this

    python
###    
    import cv2
    import mediapipe as mp
    print("OpenCV version:", cv2.__version__)

###
    cap = cv2.VideoCapture(0)
    cap.isOpened()

if done correctly cap.isOpened() should return true.

### To Run Program

    python RPS.py

Run just this whenever you want to rerun the program again.

Press 'q' to quit program
