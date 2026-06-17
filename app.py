import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# चेहरे को पहचानने वाला बुनियादी विजन मॉड्यूल
class FaceDetectionProcessor(VideoTransformerBase):
    def __init__(self):
        # OpenCV का प्री-ट्रेंड चेहरा पहचानने वाला मॉडल लोड करना
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        
        # फ्रेम को ग्रे-स्केल में बदलना (चेहरा पहचानने के लिए जरूरी)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # चेहरा ढूंढना
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # चेहरे के चारों ओर बॉक्स बनाना
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "FACE DETECTED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("🛡️ OmniProtect: चरण 1 (Vision)")
st.write("कैमरा चालू करें और देखें कि क्या सिस्टम आपके चेहरे को पहचान पा रहा है।")

webrtc_streamer(key="face-detection", video_transformer_factory=FaceDetectionProcessor)
