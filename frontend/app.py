import streamlit as st
import requests
from PIL import Image

API_URL = "http://localhost:8000/CardProcessings"

st.set_page_config(
    page_title="Egyptian National ID OCR",
    layout="wide",
)

st.title("🪪 Egyptian National ID OCR")
st.write("Upload an Egyptian national ID card to extract its information.")

uploaded_file = st.file_uploader("Upload ID card",type=["jpg", "jpeg", "png"],)

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image,caption="Uploaded ID",width=500,)

    if st.button("Extract Information", type="primary"):
        with st.spinner("Processing ID..."):
            response = requests.post(
                API_URL,
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                },
            )

        if response.ok:
            result = response.json()

            st.success("Extraction completed!")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Extracted Information")

                st.text_input(
                    "Name",
                    value=result.get("name", ""),
                    disabled=True,
                )

                st.text_input(
                    "National ID",
                    value=result.get("id_number", ""),
                    disabled=True,
                )
                st.text_input(
                                    "National ID",
                                    value=result.get("english_id_number", ""),
                                    disabled=True,
                                )

            with col2:
                st.text_input(
                    "Birth Date",
                    value=result.get("birth_date", ""),
                    disabled=True,
                )

                st.text_input(
                    "Gender",
                    value=result.get("gender", ""),
                    disabled=True,
                )

            st.text_area(
                "Address",
                value=result.get("address", ""),
                disabled=True,
            )

        else:
            st.error(
                f"OCR request failed: "
                f"{response.status_code} - {response.text}"
            )