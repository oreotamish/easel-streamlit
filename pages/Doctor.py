import cv2
import numpy as np
import streamlit as st
import time
import requests
from helper import list_objects, presigned_url
from cryptography.fernet import Fernet
import os
import base64


Key = (os.environ["encryption_key"]).encode()
f = Fernet(Key)

if "submitted" not in st.session_state:
    st.session_state.submitted = False


def downloader(url):
    response = requests.get(url)
    return response.content


def scanner(image):
    if image:
        bytes_data = image.getvalue()
        nparr = np.frombuffer(bytes_data, np.uint8)
        cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(gray_img)

        if data:
            decrypted_data = f.decrypt(data).decode()
            patient_name = decrypted_data.split("/")[-2].capitalize().replace("-", " ")
            st.write("### Patient Information:\n", "#### Name: ", patient_name)
            type_data = st.radio(
                label="###### Choose type of data: ",
                options=["Prescription", "Lab Report", "Diagnosis"],
                captions=[
                    "Previous Prescriptions",
                    "Previous Lab Reports",
                    "Previous Diagnosis",
                ],
                index=None,
                key=1,
            )

            if type_data:
                # st.runtime.legacy_caching.clear_cache()
                with st.spinner("Fetching..."):
                    time.sleep(2)
                # st.write("SHHESH")
                final = (
                    patient_name.lower().replace(" ", "-")
                    + "/"
                    + type_data.lower().replace(" ", "-")
                )
                folder = list_objects(
                    bucket_name="organisation-hospital",
                    patient_folder=final,
                )
                formatted_items = [key for key in folder]
                # formatted_items = [file.split("/")[-1] for file in folder[1:]]
                # formatted_items = [f"${file}.split(" / ")[3]" for file in folder[1:]]
                with st.expander(":red[List of Files]", expanded=True):
                    if formatted_items:
                        for f_item in formatted_items:
                            url = presigned_url("organisation-hospital", folder[f_item])
                            content = downloader(url)

                            st.write(f":orange[{f_item}]")
                            st.download_button(
                                label=f"Download {f_item}",
                                data=content,
                                file_name=f_item,
                                mime="application/octet-stream",
                            )
                    else:
                        st.write("No data found !")


image = st.camera_input("Show QR code")
st.write("OR")
file = st.file_uploader("Choose QR code")
if file or image:
    image = file

    # time.sleep(1)
    st.session_state.submitted = True
    st.success("File uploaded successfully!")
    st.runtime.legacy_caching.clear_cache()
    scanner(image)


# if st.session_state.submitted:
#     scanner(image)
