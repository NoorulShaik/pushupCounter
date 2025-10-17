AI Pushup Counter and Form Analyzer

Project Overview

This project is a real-time AI-powered fitness application designed to accurately count pushup repetitions and analyze exercise form using computer vision. It leverages Google's MediaPipe Pose model to track 33 key body landmarks and uses custom trigonometric calculations to measure joint angles (elbow, hip, and knee).

The application provides instant visual feedback on:

Repetition Count: Based on the average elbow angle (Shoulder-Elbow-Wrist).

Exercise Stage: Tracks whether the user is in the UP or DOWN phase.

Form Status: Checks for common errors like dropped hips (Plank Alignment) or bent knees (Straight Leg check).

Files in this Repository

File Name

Description

main.py

The main script. Handles video capture, MediaPipe processing, core counting logic (state machine), form analysis, and displaying the real-time overlay.

pushup_logic.py

A utility module containing the calculate_angle function, which performs the necessary trigonometry (using NumPy) to measure the angle between three body landmarks.

requirements.txt

Lists all necessary Python dependencies for easy setup.

🚀 Installation and Setup

Prerequisites

You need Python 3.7 or higher installed on your system.

Step 1: Clone the Repository

git clone [Your-Repository-URL]
cd [Your-Repository-Name]


Step 2: Install Dependencies

All required libraries are listed in requirements.txt. We highly recommend using a virtual environment to manage dependencies.

Create a Virtual Environment (Optional but Recommended):

python -m venv venv
# Activate the environment
# Windows: .\venv\Scripts\activate
# macOS/Linux: source venv/bin/activate


Install Libraries:

pip install -r requirements.txt


Core Dependencies:

opencv-python (for video stream and UI rendering)

mediapipe (for real-time pose estimation)

numpy (for efficient vector mathematics in angle calculation)

▶️ How to Run the Application

Once the dependencies are installed, you can launch the application from your terminal:

python main.py


The application will open a new window showing your webcam feed with the real-time AI overlay. Press 'q' to close the application.

🤸 How to Use the Pushup Counter

Camera Setup: Ensure your camera captures your full body in a side view while you perform pushups (parallel to the camera frame).

Counting: The count increments only when you transition from the DOWN stage (elbow angle below 100°) back to the UP stage (elbow angle above 160°).

Form Feedback:

GOOD FORM (Green): You are maintaining proper alignment.

BAD FORM (HIPS - Red): Your hip angle (Shoulder-Hip-Ankle) has dropped below 165° (signaling a dropped hip).

BAD FORM (KNEES - Orange): Your leg is bent, or the Hip-Knee-Ankle angle is below 170°.

⚙️ Configuration (Tuning Thresholds)

If the counter is too strict or too loose for your body type, you can easily adjust the sensitivity by modifying the constant values at the top of the main.py file:

# main.py constants:
DOWN_ANGLE_THRESHOLD = 100  # Decrease for a deeper pushup requirement
UP_ANGLE_THRESHOLD = 160    # Increase to require straighter arms at the top
PLANK_ALIGNMENT_THRESHOLD = 165 # Alignment check for dropped hips
KNEE_STRAIGHTNESS_THRESHOLD = 170 # Alignment check for bent legs
