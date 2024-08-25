from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_gemini_response(input, image, prompt):
    res = model.generate_content([input,image[0],prompt])
    return res.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()   # reads the file in bytes format

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("Unable to find the file!")


# streamlit app
# Set page configuration
st.set_page_config(page_title="Invoice Extractor", page_icon=":page_facing_up:", layout="wide")

# Add a title and description
st.title("📄 Multilanguage Invoice Extractor")
st.markdown("""
Welcome to the Multilanguage Invoice Extractor! This app allows you to upload an invoice image and extract key information from it. 
You can ask any questions based on the uploaded invoice image.
""")

# Input prompt
st.sidebar.header("User Input")
input = st.sidebar.text_input("Input prompt:", key="input")

# File uploader
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png", "pdf"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button
submit = st.button("Tell me about the invoice")

# Input prompt for the model
input_prompt = """
We will upload an image as invoice and you will have to answer any questions based on the uploaded invoice image.
"""

# Process the input and display the response
if submit:
    with st.spinner("Processing..."):
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)
        st.success("Processing complete!")
        st.subheader("The response is:")
        st.write(response)

# Footer
st.markdown("""
---
API: Google Gemini flash 1.5
*Developed by Soumyadip Majumder*
""")

