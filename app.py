import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

# Define a simple video transformer (for demonstration, does nothing)
class IdentityTransformer(VideoTransformerBase):
    def transform(self, frame):
        return frame

def main():
    st.title("Real-Time Video Stream")

    # Customize RTC configuration for better connectivity (optional)
    rtc_configuration = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    # Create a WeBRTC component
    webrtc_streamer(
        key="example",
        video_transformer_factory=IdentityTransformer,
        rtc_configuration=rtc_configuration,  # Optional
        media_stream_constraints={"video": True, "audio": False},
    )

if __name__ == "__main__":
    main()
