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
        auth_token = "204b198c1a053a12fb4fee7f2158d4e6"
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
 
    img_color = cv2.pyrDown(cv2.pyrDown(img))

    for _ in range(6):
        img_color = cv2.bilateralFilter(img_color, 9, 9, 7)

    img_color = cv2.pyrUp(cv2.pyrUp(img_color))

    img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_edges = cv2.medianBlur(img_edges, 7)


    img_edges = cv2.adaptiveThreshold(
        img_edges, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
    )

  
    img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

    img_cartoon = cv2.bitwise_and(img_color, img_edges)

    return img_cartoon


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
