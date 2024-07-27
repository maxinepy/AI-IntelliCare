import streamlit as st
from openai import OpenAI
from meal_scanner import MealScanner
import database as db
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import os
import carebot as cb
import help as hp
import info
from medication import medi_reminder

dw = db.DataWriter()

# Hide Sidebar
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center;'>Welcome Back to IntelliCare!🤗</h1>",
    unsafe_allow_html=True)

add_info_tab, carebot, meal_scan, med_remind, help, logout = st.tabs([
    ":baby: Getting to Know Your Student(s) More", ":robot_face: Carebot",
    ":camera: Meal Scanner", ":pill: Medication Tracker", ":sos: Help",
    ":door: Logout"
])

with add_info_tab:
    info = info.Info()

    info.info()

    with st.form(key="add_info_form"):
        # submit buttons
        add = st.form_submit_button("Add Student", use_container_width=True)
        update = st.form_submit_button("Update Student", use_container_width=True)
        delete = st.form_submit_button("Delete Student", use_container_width=True)

        if add:
            info.add_dialog()
            
        elif update:
            info.update_dialog()
                
        elif delete:
            info.delete_dialog()

    st.session_state.all_records = dw.get_all_records_as_dict(st.session_state.user["Worksheet Name"])
        
with carebot:
    st.subheader("Carebot")

    # Create a container for the chat messages
    chat_container = st.container()

    # Create a container for the input box
    input_container = st.container()

    openai_api_key = os.environ['OPENAI_NANNY']  
    st.write(f"API Key Length: {len(openai_api_key)}")
    
    client = OpenAI(api_key=os.environ['OPENAI_NANNY'])
    # client = OpenAI(api_key=st.secrets['OPENAI_NANNY'])

    st.markdown("""
    <style>
    .stApp {
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    .main {
        flex-grow: 1;
        overflow: auto;
    }
    .chat-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem;
        z-index: 1000;
    }
    .chat-messages {
        padding-bottom: 70px;
    }
    </style>
    """,
                unsafe_allow_html=True)

    with chat_container:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if len(st.session_state.messages) == 0:
            with st.chat_message("assistant"):
                st.markdown(
                    "Hi! I'm CareBot, your virtual childcare assistant. How can I help you today?"
                )
            st.session_state.messages.append({
                "role" :
                "assistant",
                "content":
                "Hi! I'm CareBot, your virtual childcare assistant. How can I help you today?"
            })

    with input_container:
        prompt = st.chat_input("Ask a question!")
        if prompt:
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt
                })

                with st.spinner("Carebot is analyzing..."):
                    refined_prompt = cb.prompt_refine_teachers(client, prompt)
                    response = cb.generate_advice_teachers(client, prompt)
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })

            # Rerun to update the chat container
            st.rerun()

with meal_scan:
    ms = MealScanner()
    ms.run()

with med_remind:
    st.subheader("Medication Tracker")
    st.write("Here are the medications you have keyed-in:")

    medi_reminder()

with help:
    help = hp.Help()
    help.help_desc()
    
with logout:
    st.subheader("Logout")
    st.write("Are you sure you want to log out?")
    butt = st.button("Yes")
    if butt:
        switch_page("login")
