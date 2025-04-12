# How to Run the program.
This is just the basic setup from the demo workshop to get the camera working and have rps_env installed


##

Also I could not get git hub to allow me to put the rps_env file in the repository so that is why you have to install it.
##
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
