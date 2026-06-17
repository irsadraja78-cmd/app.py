import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

class VideoProcessor(VideoTransformerBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        cv2.putText(img, "SYSTEM READY", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("🛡️ OmniProtect Gateway")
webrtc_streamer(key="omni", video_transformer_factory=VideoProcessor)
