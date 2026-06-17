
import streamlit as st
import cv2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

st.title("🛡️ OmniProtect Gateway")

class SimpleProcessor(VideoTransformerBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        cv2.putText(img, "SECURE GATE ACTIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(key="cam", video_transformer_factory=SimpleProcessor)
