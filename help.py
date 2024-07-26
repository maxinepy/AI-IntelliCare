import streamlit as st

class Help:

  def help_desc(self):
    st.subheader("Welcome to IntelliCare! :robot_face:")
    st.write(
        "I am your pocket-sized parenting assistant. I am here to help you with any problems you may have with your child. I can provide advice on how to approach your child's problems, automatic allergy alerts from Meal Scanner, Medication reminders, and more."
    )

    st.subheader("Signing Up")
    st.write("If you are a first time user, Click 'Sign UP' on the login page, enter your details and submit.")

    st.subheader("Logging In")
    st.write("Log in by entering your username and password.")

    st.subheader("Getting Started")
    st.write(
        "To get started, navigate to \'Getting to Know Your Child More\' tab")
    st.write(
        "Simply enter your child's name, age, gender, medical conditions, allergies, and other relevant information. ."
    )
    st.write("Click \"Done\" to save your information.")

    st.subheader("CareBot :robot_face:")
    st.write("Present your problem in the \'Carebot\' tab.")
    st.write(
        "Click \"Submit\". I will then provide a well-tailored advice on how to approach your problem."
    )

    st.subheader("Meal Scanner :fork_and_knife:")
    st.write("Snap or Upload a photo of your meal. Click 'Analyse Ingredients' and I will tell you if it is safe for your kids!")

    st.subheader("Medication Tracker :pill:")
    st.write("Track daily medications so your child never misses a dose!")