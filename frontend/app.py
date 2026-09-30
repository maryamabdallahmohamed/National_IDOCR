import os

import requests
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Egyptian National ID OCR",
    layout="wide",
)

if "BACKEND_URL" not in os.environ:
    try:
        secret_backend_url = st.secrets.get("BACKEND_URL")
    except Exception:
        secret_backend_url = None
    if secret_backend_url:
        os.environ["BACKEND_URL"] = secret_backend_url

if "BACKEND_URL" not in os.environ:
    st.error("Backend configuration is missing. Set the BACKEND_URL environment variable.")
    st.stop()

BACKEND_URL = os.environ["BACKEND_URL"]
API_URL = f"{BACKEND_URL.rstrip('/')}/CardProcessings"

EXPECTED_FIELDS = {
    "name",
    "address",
    "id_number",
    "factory_number",
    "gender",
    "birth_date",
    "english_id_number",
    "photo",
}

st.title("🪪 Egyptian National ID OCR")
st.write("Upload a synthetic Egyptian national ID card image to extract its information.")
st.warning(
    "Demo only — Please upload synthetic/test ID images. "
    "Do not upload real national IDs or other sensitive personal documents."
)

uploaded_file = st.file_uploader("Upload ID card",type=["jpg", "jpeg", "png"],)

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image,caption="Uploaded ID",width=500,)

    if st.button("Extract Information", type="primary"):
        with st.spinner("Processing ID..."):
            try:
                response = requests.post(
                    API_URL,
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    },
                    timeout=(10, 180),
                )
                response.raise_for_status()
            except requests.exceptions.Timeout:
                st.error("The OCR backend took too long to respond. Please try again.")
            except requests.exceptions.HTTPError:
                st.error(
                    f"The OCR backend rejected the request (HTTP {response.status_code})."
                )
            except requests.exceptions.RequestException:
                st.error("The OCR backend is unavailable. Please try again later.")
            else:
                try:
                    result = response.json()
                except ValueError:
                    st.error("The OCR backend returned an invalid response.")
                else:
                    if not isinstance(result, dict) or not EXPECTED_FIELDS.issubset(result):
                        st.error("The OCR backend returned an incomplete response.")
                    else:
                        st.success("Extraction completed!")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Extracted Information")

                            st.text_input(
                                "Name",
                                value=result["name"],
                                disabled=True,
                            )

                            st.text_input(
                                "National ID",
                                value=result["id_number"],
                                disabled=True,
                            )
                            st.text_input(
                                "English National ID",
                                value=result["english_id_number"],
                                disabled=True,
                            )

                        with col2:
                            st.text_input(
                                "Birth Date",
                                value=result["birth_date"],
                                disabled=True,
                            )

                            st.text_input(
                                "Gender",
                                value=result["gender"],
                                disabled=True,
                            )

                        st.text_area(
                            "Address",
                            value=result["address"],
                            disabled=True,
                        )