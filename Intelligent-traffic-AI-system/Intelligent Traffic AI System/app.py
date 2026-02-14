# Streamlit library for building web dashboard
import streamlit as st
import cv2
import tempfile
from backend import TrafficSystem


# ---------------------------------------------------------
# Configure Streamlit Page Settings
# ---------------------------------------------------------
st.set_page_config(
    page_title="Intelligent Traffic AI",
    layout="wide"
)

# Dashboard Title
st.title("🚦 Intelligent Traffic AI System")

st.write("Real-time Vehicle Detection | Speed Estimation | Line Crossing | OCR")

# Video Upload Section

uploaded_video = st.file_uploader(
    "Upload Traffic Video",
    type=["mp4"]
)


# ---------------------------------------------------------
# If user uploads video → Start processing
# ---------------------------------------------------------
if uploaded_video:

    # Save uploaded video into temporary file location
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_video.read())

    # Open video using OpenCV
    cap = cv2.VideoCapture(temp_file.name)

    # Initialize AI backend system
    traffic_system = TrafficSystem()
    
    frame_window = st.image([])       # For displaying processed frames
    count_placeholder = st.empty()    # For displaying vehicle count metric


    # -----------------------------------------------------
    # Frame-by-frame Processing Loop
    # -----------------------------------------------------
    while cap.isOpened():

        ret, frame = cap.read()

        # If video ends → break loop
        if not ret:
            break

        frame, count = traffic_system.process_frame(frame)

        frame_window.image(frame, channels="BGR")

        count_placeholder.metric("Vehicle Count", count)

    # Release video capture after processing
    cap.release()
