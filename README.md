AI 🏋️ Pushup Counter and Form Analyzer

🌟 Project Overview

This project is a real-time AI-powered fitness application that uses your webcam to accurately count pushup repetitions and analyze your exercise form on the fly. It functions as a personal virtual coach, ensuring quality of movement for better training results.

Key Features:

Dual-Angle Counting: Tracks repetition based on the average elbow angle (Shoulder-Elbow-Wrist) for maximum accuracy.

Form Analysis: Provides immediate feedback for two critical form faults:

Dropped Hips (Plank Alignment Check).

Bent Knees (Straight Leg Check).

Real-Time Overlay: Displays Rep Count, Exercise Stage (UP/DOWN), and Form Status directly on the video feed using OpenCV.

💻 Tech Stack

Python             --->Core programming language.

MediaPipe Pose     --->Real-time human pose estimation and landmark tracking.

OpenCV (cv2)       --->Video stream capture, frame manipulation, and UI rendering.

NumPy              --->Efficient vector mathematics for calculating joint angles.


📂 Files in this Repository

main.py  ---The main execution script. Handles video input, MediaPipe processing, the core counting state machine, form analysis, and all display logic.

pushup_logic.py   ---A utility module containing the precise calculate_angle function, which converts three body landmarks into an accurate joint angle measurement.


🚀 Installation and Setup

Prerequisites

You need Python 3.7 or higher installed on your system.

Step 1: Clone the Repository

git clone [Your-Repository-URL]

cd [Your-Repository-Name]

Step 2: Install Dependencies

Install Libraries:

pip install opencv-python mediapipe numpy

▶️ How to Run the Application

Once the dependencies are installed, launch the application from your terminal:

python main.py


The application will open a new window showing your webcam feed with the real-time AI overlay. Press 'q' to close the application.

🤸 Usage & Form Rules

Camera Setup: Position your camera to capture your full body in a clear side view while you perform pushups.

Counting: A repetition is counted only when the system registers a transition from the DOWN stage (elbow angle below 100°) back to the UP stage (elbow angle above 160°).

Form Feedback:

GOOD FORM (Green): You are maintaining proper alignment.

BAD FORM (HIPS - Red): Your hip angle (Shoulder-Hip-Ankle) has dropped below 165° (signaling a dropped hip).

BAD FORM (KNEES - Orange): Your leg is bent, or the Hip-Knee-Ankle angle is below 170°.

⚙️ Configuration (Tuning Thresholds)

If the counter feels too strict or too loose for your body type, you can easily adjust the sensitivity by modifying the constant values at the top of the main.py file:

# main.py constants:

DOWN_ANGLE_THRESHOLD = 100  # Decrease for a deeper pushup requirement

UP_ANGLE_THRESHOLD = 160    # Increase to require straighter arms at the top

PLANK_ALIGNMENT_THRESHOLD = 165 # Alignment check for dropped hips

KNEE_STRAIGHTNESS_THRESHOLD = 170 # Alignment check for bent legs
