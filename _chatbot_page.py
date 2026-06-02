import streamlit as st
import os
import io
import google.generativeai as ggi
import google.ai.generativelanguage as gag
from dotenv import load_dotenv
from PIL import Image

def chatbot_page():
    load_dotenv()

    def image_byte_array(image : Image) -> bytes:
        IBA = io.BytesIO()
        image.save(IBA, format = image.format)
        IBA = IBA.getvalue()
        return IBA
    
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    ggi.configure(api_key=API_KEY)

    st.image('D:\\edge浏览器\\SOF106\\ALZHEIMER\\Asset\\images\\google-gemini-logo-A5787B2669-seeklogo.com-removebg-preview.png', width = 200)

    gemini1, gemini2 = st.tabs(["Prompt gemini", "Image prompt gemini"])

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    with gemini1:
        st.header("Prompt Gemini")
        st.write("")
        for chat in st.session_state.chat_history:
            st.markdown(f"**User:** {chat['user']}")
            st.markdown(f"**Response:** {chat['response']}")
            st.write("---")
        ask_box = st.text_input("Ask anything", placeholder = "Message here", label_visibility= "visible")
        model = ggi.GenerativeModel("gemini-pro")

        if st.button(":blue[Send]", use_container_width= True, key = "send_input"):
            if ask_box.strip() != "":
                response = model.generate_content(ask_box)
                st.session_state.chat_history.append({'user': ask_box, 'response': response.text})
                st.write("")
                st.header(":green[Response]")
                st.write("")
                avatars, response_texts = st.columns([1,9])
                with avatars:
                    st.image("D:\\edge浏览器\\SOF106\\ALZHEIMER\\Asset\\images\\_c0471f3d-0626-454b-b2cf-da1b5a9d8527.jpeg", use_column_width= True)
                with response_texts:
                    st.markdown(response.text)
            else:
                st.write("")
                st.write("Please provide a message")

        if st.button(":red[Clear History]", use_container_width=True, key="clear_history"):
            st.session_state.chat_history = []

    with gemini2:
        st.header("Image Prompt Gemini")
        st.write("")

        for chat in st.session_state.chat_history:
            st.markdown(f"**User:** {chat['user']}")
            st.markdown(f"**Response:** {chat['response']}")
            st.write("---")

        uploaded_file = st.file_uploader("Choose an Image", accept_multiple_files = False, type = ["jpg", "png", "jpeg", "img", "webp"])
        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width = True)
            st.markdown("""
                <style>
                        img {
                            border-radius : 10px;
                        }
                <style>
                        """, unsafe_allow_html=True)
        image_input = st.text_input("Input an image to generate", placeholder = "Message here", label_visibility = "visible")
        if st.button(":blue[Send]", use_container_width= True, key = "send_image"):
            model = ggi.GenerativeModel("gemini-pro-vision")
            if uploaded_file is not None:
                if image_input != "":
                    image = Image.open(uploaded_file)
                    response = model.generate_content(
                        gag.Content(
                            parts = [
                                gag.Part(text = image_input),
                                gag.Part(
                                    inline_data = gag.Blob(
                                        mime_type = "image/jpeg",
                                        data = image_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )

                    response.resolve()
                    st.write("")
                    st.header(":green[Response]")
                    st.write("")

                    avatar, response_text = st.columns([1,9])
                    with avatar:
                        st.image("D:\\edge浏览器\\SOF106\\ALZHEIMER\\Asset\\images\\_c0471f3d-0626-454b-b2cf-da1b5a9d8527.jpeg", use_column_width= True)
                    with response_text:
                        st.markdown(response.text)

                    st.session_state.chat_history.append({'user': f"Image: {image_input}", 'response' : response.text})
                else:
                    st.write("")
                    st.header(":red[Please provide any message]")
            else:
                st.write("")
                st.header(":red[Please provide an image]")
        if st.button(":red[Clear History]", use_container_width= True, key = "clear_history1"):
            st.session_state.chat_history = []
