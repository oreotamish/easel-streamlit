import streamlit as st
from qr import generate_qr_code
import io
import time
from cryptography.fernet import Fernet
import os
import base64
from helper import (
    check_patient_folder,
    create_user_folder,
    # create_group_folder,
    # check_group_folder,
    uploader,
)

Key = (os.environ["encryption_key"]).encode()
f = Fernet(Key)


st.set_page_config(page_title="Patient", page_icon="🙋‍♂️")

if "submitted" not in st.session_state:
    st.session_state.submitted = False


def submitted():
    st.session_state.submitted = True


@st.cache_data(experimental_allow_widgets=True)
def user(s3_path, f_patient_number):
    encrypted_s3_path = f.encrypt(s3_path.encode())
    patient_qr = generate_qr_code(encrypted_s3_path)
    img_byte_arr = io.BytesIO()
    patient_qr.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    st.image(img_byte_arr, caption="Generated QR Code", use_column_width=True)

    st.button("Add Data", on_click=submitted)

    if st.session_state.submitted:
        key = f"patients/{f_patient_number}/"
        if not check_patient_folder(key):
            st.write("Patient folder not found!")
            create_user_folder(key)
            st.write("Patient folder created successfully!")
        else:
            st.write("Patient folder found!")
            data = st.selectbox(
                "Select data to upload",
                ["Prescription", "Lab Report", "Diagnosis"],
            )
            if data == "Prescription":
                uploader(f_patient_number, data)

            if data == "Lab Report":
                uploader(f_patient_number, data)

            if data == "Diagnosis":
                uploader(f_patient_number, data)


st.title("Patient")

patient_number = st.selectbox("Select Patient", ["Patient 1", "Patient 2", "Patient 3"])


if patient_number:
    st.cache_data.clear()
    f_patient_number = patient_number.lower().replace(" ", "-")
    st.write(f"Selected Patient: {f_patient_number}")
    s3_path = f"s3://organisation-hospital/patients/{f_patient_number}/"
    user(s3_path, f_patient_number)


st.sidebar.header("Patient Stats:")

if st.session_state.submitted:
    with st.sidebar:
        with st.spinner("Syncing..."):
            time.sleep(2)
