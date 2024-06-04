import streamlit as st
import cv2

st.title("Live Webcam Feed")

# Get user permission to access the webcam
permission = st.experimental_get_session_state().get("camera_permission", False)

if not permission:
    permission = st.button("Grant Camera Access")
    if permission:
        st.experimental_set_session_state(camera_permission=True)

if permission:
    # Access the webcam (index 0 is usually the default)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        st.error("Unable to access the webcam. Please check your camera settings and permissions.")
    else:
        # Create a placeholder for the live feed
        live_feed = st.empty()

        while True:
            # Read a frame from the webcam
            ret, frame = camera.read()

            if not ret:
                st.error("Error reading frame from the webcam.")
                break

            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # Display the frame in the Streamlit app
            live_feed.image(frame, channels="BGR")

        # Release the webcam when done
        camera.release()
else:
    st.warning("Please grant camera access to use this feature.")
