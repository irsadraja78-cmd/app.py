import streamlit as st
import cv2
import av
import face_recognition
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# 1. आपके चेहरे का गणितीय कोड (इसे हम आगे और अपडेट करेंगे)
JAS_ENCODING = None 

class JasGate(VideoTransformerBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        
        # चेहरा ढूंढना
        face_locations = face_recognition.face_locations(img)
        face_encodings = face_recognition.face_encodings(img, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # अगर मैच हुआ तो नाम लिखें, नहीं तो "UNKNOWN"
            label = "UNKNOWN"
            color = (0, 0, 255) # लाल (अजनबी)
            
            # यहाँ 'जस' मैचिंग करेगा
            if JAS_ENCODING is not None:
                matches = face_recognition.compare_faces([JAS_ENCODING], face_encoding)
                if matches[0]:
                    label = "REENA ACCESS GRANTED"
                    color = (0, 255, 0) # हरा (आप)
            
            cv2.rectangle(img, (left, top), (right, bottom), color, 2)
            cv2.putText(img, label, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("🛡️ JAS: Identity Verification")
webrtc_streamer(key="jas-gate", video_transformer_factory=JasGate)
