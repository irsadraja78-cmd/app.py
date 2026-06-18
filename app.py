import streamlit as st
import cv2
import av
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

if 'access_logs' not in st.session_state:
    st.session_state.access_logs = []

class FinalGate(VideoTransformerBase):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "REENA DETECTED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # सिर्फ तभी लॉग करें जब 2 सेकंड का गैप हो (ताकि लिस्ट न भरे)
            if not st.session_state.access_logs or (time.time() - st.session_state.last_log_time > 2):
                st.session_state.access_logs.append(f"REENA Detected: {time.strftime('%H:%M:%S')}")
                st.session_state.last_log_time = time.time()
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

if 'last_log_time' not in st.session_state:
    st.session_state.last_log_time = 0

st.title("🛡️ OmniProtect: ACTIVE")
webrtc_streamer(key="final-gate", video_transformer_factory=FinalGate)

st.subheader("Access History")
st.write(st.session_state.access_logs)
