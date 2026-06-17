import streamlit as st
import cv2
import av
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# इतिहास के लिए एक खाली लिस्ट
if 'access_logs' not in st.session_state:
    st.session_state.access_logs = []

class EnterpriseGate(VideoTransformerBase):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "AUTHORIZED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            # टाइमस्टैम्प लॉग करें
            st.session_state.access_logs.append(f"Entry at {time.strftime('%H:%M:%S')}")
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("🛡️ OmniProtect: Enterprise Edition")
webrtc_streamer(key="enterprise-gate", video_transformer_factory=EnterpriseGate)

# लॉग्स दिखाएं (मार्केटिंग के लिए बहुत ज़रूरी)
st.subheader("Live Security Logs")
st.write(st.session_state.access_logs[-5:]) # पिछले 5 रिकॉर्ड
