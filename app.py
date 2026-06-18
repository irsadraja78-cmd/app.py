import streamlit as st
import cv2
import av
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# सेशन स्टेट का सेटअप (डेटा को याद रखने के लिए)
if 'access_logs' not in st.session_state:
    st.session_state.access_logs = []

class FinalSecurityGate(VideoTransformerBase):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            # बॉक्स और नाम
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "REENA: ACCESS", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # लॉग अपडेट लॉजिक - इसे यहाँ एक फंक्शन की तरह जोड़ दिया है
            log_entry = f"ENTRY: {time.strftime('%H:%M:%S')}"
            if log_entry not in st.session_state.access_logs:
                st.session_state.access_logs.append(log_entry)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("🛡️ OmniProtect: Final Build")
webrtc_streamer(key="final-build", video_transformer_factory=FinalSecurityGate)

st.subheader("Access History Logs")
st.write(st.session_state.access_logs)
