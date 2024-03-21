from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
google_api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is available
if google_api_key is None:
    st.error("Error: GOOGLE_API_KEY not found in .env file")
else:
    # Configure the genai library with the API key
    genai.configure(api_key=google_api_key)

    # Initialize Gemini LLM model for chat
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])

    # Function to get Gemini response for user input
    def get_gemini_response(question):
        try:
            response = chat.send_message(question, stream=True)
            return response
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
            return None

    # Streamlit app initialization
    st.set_page_config(page_title="Q&A Demo")
    st.header("Gemini LLM Application")

    # Initialize session state for chat history and user information
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = {}

    # Ask for user information
    st.subheader("User Information")
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    phone = st.text_input("Phone Number:")

    # Save user information
    st.session_state['user_info']['name'] = name
    st.session_state['user_info']['email'] = email
    st.session_state['user_info']['phone'] = phone

    # User input and submit button
    input_text = st.text_input("Input:")
    submit_button = st.button("Ask the question")

    # Handle user input and display response
    if submit_button and input_text:
        response = get_gemini_response(input_text)
        if response:
            st.subheader("The Response is ")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
            st.session_state['chat_history'].append(("You", input_text))

    # Display chat history
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f'{role}: {text}')
