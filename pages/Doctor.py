import cv2
import numpy as np
import streamlit as st
import time
import requests
from helper import list_objects, presigned_url
from cryptography.fernet import Fernet
import os
from PIL import Image

Key = (os.environ["encryption_key"]).encode()

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "downloaded" not in st.session_state:
    st.session_state.downloaded = False

if "clicked" not in st.session_state:
    st.session_state.clicked = False


def downloader(url, f_item):
    response = requests.get(url, stream=True)
    st.session_state.content = response.content
    st.session_state.f_name = f_item
    st.session_state.clicked = True


def downloaded():
    st.session_state.downloaded = True


def scanner(image):
    img = Image.open(image)
    img_array = np.array(img)
    # bytes_data = image.getvalue()
    # nparr = np.frombuffer(bytes_data, np.uint8)
    # st.write(nparr.shape)
    # cv2_img = cv2.imdecode(nparr)
    # gray_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    detector = cv2.QRCodeDetector()
    # st.write(cv2_img)
    data, _, _ = detector.detectAndDecode(img_array)

    if data:
        f = Fernet(Key)
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
                    if not st.session_state.clicked:
                        for f_item in formatted_items:
                            url = presigned_url("organisation-hospital", folder[f_item])
                            # content = downloader(url)
                            st.write(f":orange[{f_item}]")

                            st.button(
                                label=f"Download {f_item}",
                                on_click=downloader,
                                args=[url, f_item],
                            )
                    if st.session_state.clicked:
                        st.download_button(
                            label="DOWNLOAD",
                            data=st.session_state.content,
                            file_name=st.session_state.f_name,
                        )
                    # if st.session_state.downloaded:
                    #     with open(st.session_state.f_name, "wb") as file:

                    # st.write(Image.open(content))

                else:
                    st.write("No data found !")


image = st.camera_input("Show QR code")
st.write("OR")
file = st.file_uploader("Choose QR code")
if file or image:
    if image:
        file = image
    else:
        image = file
    # time.sleep(1)
    st.session_state.submitted = True
    st.success("File uploaded successfully!")
    st.runtime.legacy_caching.clear_cache()
    scanner(image)


# if st.session_state.submitted:
#     scanner(image)
