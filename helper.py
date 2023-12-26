import boto3
import streamlit as st
from botocore.exceptions import ClientError
import logging
import time
import os
from dotenv import load_dotenv

load_dotenv(".env")


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["aws_access_key_id"],
    aws_secret_access_key=os.environ["aws_secret_access_key"],
)


def check_patient_folder(patient_folder):
    try:
        s3.head_object(Bucket="organisation-hospital", Key=patient_folder)
        return True
    except:
        return False


def upload_to_s3(file_content, file_name, patient_folder, group_name):
    s3.put_object(
        Body=file_content,
        Bucket="organisation-hospital",
        Key=f"patients/{patient_folder}/{group_name}/{file_name}",
    )


def check_group_folder(patient_folder, group_name):
    try:
        s3.head_object(
            Bucket="organisation-hospital",
            Key=f"patients/{patient_folder}/{group_name}/",
        )
    except:
        return False


def create_group_folder(patient_folder, group_name):
    s3.put_object(
        Bucket="organisation-hospital", Key=f"patients/{patient_folder}/{group_name}/"
    )


def create_user_folder(f_patient_number):
    try:
        s3.put_object(Bucket="organisation-hospital", Key=f_patient_number)
    except Exception as e:
        return e


def uploader(f_patient_number, data):
    data = data.lower().replace(" ", "-")
    if not check_group_folder(f_patient_number, data):
        create_group_folder(f_patient_number, data)
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        file_content = uploaded_file.read()
        file_name = uploaded_file.name
        upload_to_s3(file_content, file_name, f_patient_number, data)
        with st.status("Creating Object..."):
            time.sleep(2)
            st.write("Uploaded!")


def list_objects(bucket_name, patient_folder):
    objects = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=f"patients/{patient_folder}",
    )
    key_n_path = {}
    if "Contents" in objects:
        for obj in objects["Contents"][1:]:
            path = obj["Key"]
            key = path.split("/")[-1]
            # path = key.replace(f"patients/{patient_folder}/{key}", "")
            key_n_path[key] = path
    return key_n_path


def presigned_url(bucket_name, object_name, expiration=300):
    try:
        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response
