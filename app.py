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
                {"urls": "stun:stun.l.google.com:19302"},  # Google's public STUN server
                {"urls": "stun:stun1.l.google.com:19302"}, 
                {"urls": "stun:stun2.l.google.com:19302"}, 
                # Add more STUN servers here if needed
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
