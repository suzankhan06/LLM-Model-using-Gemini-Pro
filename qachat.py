from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load GEMINI PRO MODEL and get response

model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question, stream=True)
    return response

## Initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

## to record the history of our conversation 
# Initialize session state for chat history  if it doesnt exist

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:", key = "input")

# submit button
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    ## Add user query and responses to sesstion chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")

    # we want to display the history with our responses, so we write

    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("The Chat history is") 

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")



