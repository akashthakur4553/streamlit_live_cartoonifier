import streamlit as st
from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    RTCConfiguration,
)

# Define a video processor (does nothing in this example)
class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        return frame

def main():
    st.title("Real-Time Video Stream")

    # Configure RTC with STUN servers 
rtc_configuration = RTCConfiguration(
    {
        "iceServers": [
            {"urls": "stun:stun.l.google.com:19302"},   # Google
            {"urls": "stun:stun1.l.google.com:19302"}, 
            {"urls": "stun:stun2.l.google.com:19302"},
            {"urls": "stun:stun3.l.google.com:19302"},
            {"urls": "stun:stun4.l.google.com:19302"}, 
            {"urls": "stun:stun.services.mozilla.com"}, # Mozilla
            {"urls": "stun:stun.aircall.io:3478"},      # Aircall
            {"urls": "stun:stun.voip.eutelia.it:3478"}, # Eutelia
            # Add more STUN servers if needed from the resources mentioned below
        ]
    }
)

    # Create the WeBRTC component
    webrtc_streamer(
        key="example",
        video_processor_factory=VideoProcessor,
        rtc_configuration=rtc_configuration, 
        media_stream_constraints={"video": True, "audio": False},
    )

if __name__ == "__main__":
    main()
