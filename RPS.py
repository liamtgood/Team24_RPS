import cv2
import mediapipe as mp
import random
import time
import tkinter as tk
from threading import Thread

def detect_hand_shape(landmarks):
    """Determines if the shape is Rock, Paper, or Scissors based on hand landmarks."""
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    
    fingers = [index_tip, middle_tip, ring_tip, pinky_tip]
    extended = sum(1 for finger in fingers if finger.y < landmarks[5].y)  # Count extended fingers
    
    if extended == 0:
        return "Rock"
    elif extended == 2:
        return "Scissors"
    elif extended == 4:
        return "Paper"
    else:
        return None

def start_game():
    """Starts the hand gesture detection game."""
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    opponent_move = None
    delay = 0  # Delay for opponent's move display
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        h, w, c = frame.shape
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        
        detected_gesture = "No hand detected"
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = detect_hand_shape(hand_landmarks.landmark)
                if gesture:
                    detected_gesture = gesture
        
        # Display detected gesture
        cv2.putText(frame, f"Detected: {detected_gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if detected_gesture != "No hand detected":
            if delay ==0:
                opponent_move = random.choice(['Rock', 'Paper', 'Scissors'])
                delay = 100
            if delay>0:
                delay -= 1
                cv2.putText(frame, f"Opponent: {opponent_move}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        
        cv2.imshow("Hand Gesture Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def launch_game():
    """Launches the game in a separate thread."""
    game_thread = Thread(target=start_game)
    game_thread.start()

# Create a simple GUI with tkinter
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("300x200")

# Add a Start button
start_button = tk.Button(root, text="Start Game", command=launch_game, font=("Arial", 16), bg="green", fg="white")
start_button.pack(expand=True)

# Run the tkinter event loop
root.mainloop()