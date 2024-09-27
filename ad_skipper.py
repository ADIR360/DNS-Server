import cv2
import time
from pytesseract import pytesseract
import os

# Define path for Tesseract executable (if needed)
pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def detect_advertisement(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Use Tesseract to extract text from the frame (this assumes text-based ads)
    text = pytesseract.image_to_string(gray)
    
    # Check if ad-related keywords appear
    ad_keywords = ['Ad', 'Advertisement', 'Sponsored', 'Skip Ad']
    for keyword in ad_keywords:
        if keyword.lower() in text.lower():
            return True
    return False

def skip_advertisement(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error opening video file")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if detect_advertisement(frame):
            print("Ad detected! Speeding up video...")
            # Simulate speeding up by skipping frames
            for _ in range(100):  # Skip 100 frames (adjust as necessary)
                cap.read()
        else:
            # Show the video normally
            cv2.imshow('Video', frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage: replace 'video.mp4' with your actual video file
skip_advertisement('video.mp4')
