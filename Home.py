import streamlit as st
from st_pages import Page, show_pages, add_page_title
from dotenv import load_dotenv

load_dotenv(".env")

st.write("Welcome!")
add_page_title()

show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        Page("pages/Patient.py", "Patient", "🙋‍♂️"),
        Page("pages/Doctor.py", "Doctor", "🧑‍⚕️"),
        Page("pages/Lab.py", "Lab", "🔬"),
        Page("pages/Pharmacy.py", "Pharmacy", "💊"),
    ]
)
