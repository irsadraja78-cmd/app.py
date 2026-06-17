import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

class JasFastVision(VideoTransformerBase):
    def __init__(self):
        # ये बहुत हल्का मॉडल है जो बिना एरर दिए चलेगा
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "REENA: JAS ACTIVE", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("🛡️ OmniProtect: Lite Mode")
webrtc_streamer(key="jas-light", video_transformer_factory=JasFastVision)
