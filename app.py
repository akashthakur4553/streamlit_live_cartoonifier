import logging
from pathlib import Path

import av
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

from turn import get_ice_servers  # Assuming this is correctly defined




def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    """Simple callback that just returns the input frame."""
    return frame


webrtc_ctx = webrtc_streamer(
    key="simple-video-stream",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={
        "iceServers": get_ice_servers(),
        "iceTransportPolicy": "relay", 
    },
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
)

st.markdown("**Simple WebRTC Video Stream**") 
