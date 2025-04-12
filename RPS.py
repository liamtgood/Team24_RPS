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

    # Load images for computer's choices
    rock_img = cv2.imread("rock.png")
    paper_img = cv2.imread("paper.png")
    scissors_img = cv2.imread("scissor.png")

    # Resize images to fit on the frame
    rock_img = cv2.resize(rock_img, (150, 150))
    paper_img = cv2.resize(paper_img, (150, 150))
    scissors_img = cv2.resize(scissors_img, (150, 150))

    opponent_move = None  # Store the opponent's move
    last_detected_gesture = None  # Store the last detected gesture
    player_score = 0
    opponent_score = 0
    round_processed = False  # Flag to track if the round result has been processed
    wait_for_next_round = False  # Flag to wait for user input to start the next round
    results = ""  # Initialize result variable

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

        # Check if the player's gesture has changed
        if not wait_for_next_round and detected_gesture != last_detected_gesture and detected_gesture != "No hand detected":
            opponent_move = random.choice(['Rock', 'Paper', 'Scissors'])  # Generate a new opponent move
            last_detected_gesture = detected_gesture  # Update the last detected gesture
            round_processed = False  # Reset the round flag for the new gesture

        if detected_gesture == "No hand detected":
            last_detected_gesture = None
            round_processed = False  # Reset the round flag

        # Display the computer's choice as an image
        if opponent_move:
            if opponent_move == "Rock":
                frame[50:200, w - 200:w - 50] = rock_img
            elif opponent_move == "Paper":
                frame[50:200, w - 200:w - 50] = paper_img
            elif opponent_move == "Scissors":
                frame[50:200, w - 200:w - 50] = scissors_img

        # Determine the winner (only process once per round)
        if not round_processed and detected_gesture != "No hand detected" and opponent_move:
            if detected_gesture == opponent_move:
                results = "Draw!"
            elif (detected_gesture == "Rock" and opponent_move == "Scissors") or \
                (detected_gesture == "Scissors" and opponent_move == "Paper") or \
                (detected_gesture == "Paper" and opponent_move == "Rock"):
                results = "You Win!"
                player_score += 1
            else:
                results = "You Lose!"
                opponent_score += 1
            round_processed = True  # Mark the round as processed
            wait_for_next_round = True  # Wait for user input to start the next round

        cv2.putText(frame, results, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Draw scores at the bottom of the screen
        cv2.putText(frame, f"Player Score: {player_score}", (20, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Opponent Score: {opponent_score}", (w - 355, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display instructions to start the next round
        if wait_for_next_round:
            cv2.putText(frame, "Press SPACE to start the next round", (50, h - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Hand Gesture Detection", frame)

        # Check for user input to start the next round
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit the game
            break
        elif key == ord(' '):  # Spacebar to start the next round
            wait_for_next_round = False  # Reset the flag to allow the next round
            opponent_move = None  # Reset the opponent's move for the next round

    cap.release()
    cv2.destroyAllWindows()

def launch_game():
    """Launches the game in a separate thread."""
    game_thread = Thread(target=start_game)
    game_thread.start()

# Create a simple GUI with tkinter
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("400x300")

#add text
title = tk.Label(root, text="Rock Paper Scissors", font=("Arial", 24), bg="white", fg="blue")
title.pack(expand=True)

# Add a Start button
start_button = tk.Button(root, text="Start Game", command=launch_game, font=("Arial", 16), bg="blue", fg="white")
start_button.pack(expand=True)



# Run the tkinter event loop
root.mainloop()