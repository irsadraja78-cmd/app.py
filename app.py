import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

class JasSecurityGate(VideoTransformerBase):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # मार्केटिंग डेमो के लिए: पहला चेहरा 'Authorized', बाकी 'Unknown'
        for i, (x, y, w, h) in enumerate(faces):
            if i == 0:
                # पहला व्यक्ति 'मालिक' (Authorized)
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, "ACCESS GRANTED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                # बाकी लोग 'अनजान' (Denied)
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(img, "ACCESS DENIED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("🛡️ OmniProtect: Advanced Security")
webrtc_streamer(key="security-gate", video_transformer_factory=JasSecurityGate)
