# main.py
# AI-Powered Pushup Counter using MediaPipe and OpenCV  
# All required libraries: mediapipe, opencv-python, numpy
# Ensure you have the required libraries installed:
import cv2
import mediapipe as mp
import numpy as np
from pushup_logic import calculate_angle

# --- CONSTANTS FOR PUSHUP COUNTING AND FORM CHECK ---

# Elbow Angle Thresholds for Repetition Counting (The main trigger for counting)
DOWN_ANGLE_THRESHOLD = 100  # Angle must drop below this to register 'down'
UP_ANGLE_THRESHOLD = 160    # Angle must rise above this to register a completed 'up' rep

# Form Check Thresholds
# 1. Plank Alignment (Shoulder-Hip-Ankle) - Check for dropped hips
PLANK_ALIGNMENT_THRESHOLD = 165 
# 2. Knee Angle (Hip-Knee-Ankle) - Check for bent/straight legs
KNEE_STRAIGHTNESS_THRESHOLD = 170


# --- INITIALIZATION ---
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Video stream setup (Use 0 for built-in webcam)
cap = cv2.VideoCapture(0)

# Push-up Counter Logic variables
counter = 0 
stage = "up"  # Can be "up" or "down"
form_status = "GOOD FORM"
form_color = (0, 255, 0) # Green for good form

# --- MAIN APPLICATION LOOP ---
# Initialize the Pose model
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue

        # Convert the BGR image to RGB for MediaPipe processing
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor image back to BGR for OpenCV rendering
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        current_elbow_angle = 0
        current_form_status = "GOOD FORM"
        current_form_color = (0, 255, 0)

        try:
            landmarks = results.pose_landmarks.landmark

            # --- LANDMARK EXTRACTION (Right and Left Sides) ---
            
            # Right Side Points (for both Elbow Angle and Form Checks)
            r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, 
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, 
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, 
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, 
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, 
                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, 
                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                       
            # Left Side Elbow Points (for averaging)
            l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, 
                       landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, 
                       landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


            # --- ANGLE CALCULATIONS ---
            
            # 1. Elbow Angle (Primary for Repetition Counting) - Use average for robustness
            right_elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
            left_elbow_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
            
            # Use the average angle to smooth out uneven tracking or uneven pushups
            current_elbow_angle = (right_elbow_angle + left_elbow_angle) / 2
            
            # 2. Plank Angle (Shoulder-Hip-Ankle) - Check for dropped hips
            plank_angle = calculate_angle(r_shoulder, r_hip, r_ankle)
            
            # 3. Knee Angle (Hip-Knee-Ankle) - Check for straight legs
            knee_angle = calculate_angle(r_hip, r_knee, r_ankle)
            
            
            # --- FORM CHECK LOGIC (Multiple Criteria) ---
            if plank_angle < PLANK_ALIGNMENT_THRESHOLD:
                current_form_status = "BAD FORM (HIPS)"
                current_form_color = (0, 0, 255) # Red
            elif knee_angle < KNEE_STRAIGHTNESS_THRESHOLD:
                current_form_status = "BAD FORM (KNEES)"
                current_form_color = (0, 165, 255) # Orange
            else:
                current_form_status = "GOOD FORM"
                current_form_color = (0, 255, 0) # Green

            # --- VISUAL FEEDBACK (Elbow Angle) ---

            # Convert normalized coordinates (0 to 1) to pixel coordinates for display
            h, w, c = image.shape
            elbow_x = int(r_elbow[0] * w)
            elbow_y = int(r_elbow[1] * h)

            # Display the calculated angle near the elbow
            cv2.putText(image, f'{int(current_elbow_angle)}°', 
                        (elbow_x + 15, elbow_y + 15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3, cv2.LINE_AA)
            
            # Add a small circle at the elbow for better visibility
            cv2.circle(image, (elbow_x, elbow_y), 8, (0, 255, 255), -1)
            
            
            # --- PUSHUP COUNTING LOGIC (State Machine based on Average Elbow Angle) ---
            
            # Stage 1: Down Movement
            if current_elbow_angle < DOWN_ANGLE_THRESHOLD:
                stage = "down"
            
            # Stage 2: Up Movement (Completing the rep)
            # Rep counts only if the movement is complete AND the form is currently good
            if current_elbow_angle > UP_ANGLE_THRESHOLD and stage == "down":
                stage = "up"
                # You can add an optional form check here to only count perfect reps:
                # if current_form_status == "GOOD FORM":
                counter += 1 # Repetition complete!


            # --- RENDER OVERLAY BOX ---
            cv2.rectangle(image, (0, 0), (550, 120), (245, 117, 16), -1)

            # Reps display
            cv2.putText(image, 'REPS:', (20, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, str(counter), (20, 90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3, cv2.LINE_AA)
            
            # Stage display
            cv2.putText(image, 'STAGE:', (200, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, stage.upper(), (200, 90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Form display
            cv2.putText(image, 'FORM STATUS:', (350, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, current_form_status, (350, 90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, current_form_color, 2, cv2.LINE_AA)

        except Exception as e:
            # Error handling for when landmarks are not detected
            # print(f"Error processing landmarks: {e}") 
            pass

        # Draw the pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2) 
                                )        

        # Resize the image for a larger display window
        display_image = cv2.resize(image, (1080, 720)) 
        
        # Display the result
        cv2.imshow('AI Pushup Counter', display_image)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
