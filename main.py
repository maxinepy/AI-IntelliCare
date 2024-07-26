# from openai import OpenAI
# import streamlit as st
# import pandas as pd
# from streamlit_gsheets import GSheetsConnection
# import database as db
# from streamlit_extras.switch_page_button import switch_page
# import os
# import help as hp

# dw = db.DataWriter()

# st.session_state.user = {'Username': "None", 'Role': "None"}

# st.html("<h1 style='text-align: center;'>Welcome to IntelliCare!🤗</h1>")

# login_tab, help = st.tabs([
#     ":closed_lock_with_key: Login", ":sos: Help"
# ])

# @st.experimental_dialog(title="Sign Up Now")
# def sign_up():
#     username = st.text_input("Username")

#     role = st.selectbox("Role", ["Parent", "Teacher"])
#     password = st.text_input("Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")
        
#     if dw.username_exists(username, role) and password != confirm_password:
#         st.error("Username already exists or passwords do not match")
    
#     else:
#         if st.button("Sign Up Now"):
#             new_user = [username, password, role]
#             result = dw.write_sheet("Login", new_user)
#             if result == "Data updated successfully":
#                 st.toast("Sign up successful! You can now log in.")
#             else:
#                 st.error("An error occurred during sign up. Please try again.")

#             st.experimental_rerun()

# with login_tab:
    
#     st.subheader("Login")

#     st.write("Please enter your username and password to login.")
    
#     exist_username = st.text_input("Username", key="username1")
#     exist_role = st.selectbox("Role", ["Parent", "Teacher"], key="role1")
#     exist_password = st.text_input("Password",
#                                    type="password",
#                                    key="password1")
#     submitted = st.button("Submit")

#     if submitted:
#         login_result = dw.check_login(exist_username, exist_password, exist_role)
#         if login_result and login_result[0]:
#             st.success("Login Successful!")
#             st.toast("Welcome, " + ' '.join(word.capitalize() for word in exist_username.split()) + "!")

#             st.session_state.user["Username"] = exist_username.lower()
            
#             if exist_role:
#                 st.session_state.user["Role"] = exist_role
            
#             # Retrieve all records for the logged-in user's role
#             all_records = dw.get_all_records_as_dict(exist_username.lower())

#             # Store in session state
#             st.session_state.all_records = all_records

#             if login_result[1] == "Teacher":
#                 st.session_state.user["Role"] = "Teacher"
#                 switch_page("teacher page")
#             else:
#                 st.session_state.user["Role"] = "Parent"
#                 switch_page("parent page")
                
#         else:
#             st.error("Wrong Username or Password.")
#             st.error("If you don't have an account, please click the \"Sign Up\" button to create one.")
                
#     if st.button("Sign Up"):
#         # Trigger the dialog if not already signed up
#         sign_up()

# with help:
#    help = hp.Help()
   
    