import logging
import os
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)


def get_ice_servers():
    """Use Twilio's TURN server because Streamlit Community Cloud has changed
    its infrastructure and WebRTC connection cannot be established without TURN server now.
    """
    try:
        account_sid = (
            "AC33632aa93a8aef5cdd18973197a2be57"  # Correct SID, should start with "AC"
        )
        auth_token = "f50b4ea7a35c48d101ea2109639fa577"
    except KeyError:
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)

    try:
        token = client.tokens.create()
    except TwilioRestException as e:
        st.warning(
            f"Error occurred while accessing Twilio API. Fallback to a free STUN server from Google. ({e})"
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    return token.ice_servers


def cartoonify_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon


class CartoonTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        cartoon_img = cartoonify_image(img)
        return cartoon_img


st.title("Live Cartoonifier")
st.write("This app cartoonifies your live video feed using OpenCV and Streamlit.")

ice_servers = get_ice_servers()

webrtc_streamer(
    key="cartoon",
    video_processor_factory=CartoonTransformer,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={"iceServers": ice_servers},
)

st.write("Debug Information")
st.write(f"Streamlit version: {st.__version__}")
