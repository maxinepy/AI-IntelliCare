import streamlit as st
import database as db
dw = db.DataWriter()

# Function for Parents
def generate_advice_parents(client, prompt):
  generated_advice = client.chat.completions.create(
      model="gpt-4o",
      messages=[{
          "role":
          'system',
          "content":
          """You are a helpful assistant that helps caretakers with problems based on the basic information about their children like age, gender, name, medical conditions, medications and allergies. Here is a dictionary containing information about each child in a home:"""
          + str(st.session_state.all_records) +
          """ . If the user does not provide any information, you can provide a general advice, and advise the user to provide information about their child for better response. You will provide advice based on the information provided by the user. The advice should be concise, easy to read and understand, and straight to the point. It must also be medically accurate and if unsure about anything, be sure to identify potential need for professional help. Make sure the response is relevant to the child's characteristics. Also be able to state the child's information on request. """
      }, {
          "role": "user",
          "content": f'{prompt}'
      }],
      max_tokens=500,
      temperature=0.5)

  advice = generated_advice.choices[0].message.content
  return advice

def prompt_refine_parents(client, problem):
  refined_prompt = client.chat.completions.create(
      model="gpt-4o",
      messages=[{
          "role":
          'system',
          "content":
          """You are a prompt refiner for generating a detailed prompt to an AI ChatBot to generate advice for parents or caretakers. you are presented with a problem, as well as basic information about a group of children, saved in a dictionary format. You are able to see the user information here: """
          + str(st.session_state.all_records) +
          """ .. generate a refined prompt that asks an AI chatbot to give advice that is strongly related to the characteristics and information about the child/children. Make sure to check again the answer against the user information for a more tailored response. Also be able to state the child's information on request. Always include all details of the child's information in the generated prompt like literally write it out."""
      }, {
          "role": "user",
          "content": f'{problem}. {st.session_state.all_records}'
      }],
      max_tokens=500,
      temperature=0.5
  )

  return refined_prompt.choices[0].message.content

# Functions for Teachers
def generate_advice_teachers(client, prompt):
  generated_advice = client.chat.completions.create(
      model="gpt-4o",
      messages=[{
          "role":
          'system',
          "content":
          """You are a helpful assistant that helps teachers who are also caretakers with problems based on the basic information about their children like age, gender, name, medical conditions, medications and allergies. Here is a dictionary containing information about each student in a childcare centre or educational organisation:"""
          + str(st.session_state.all_records) +
          """ . If the user does not provide any information, you can provide a general advice, and advise the user to provide information about their students for better response. You will provide advice based on the information provided by the user. The advice should be concise, easy to read and understand, and straight to the point. It must also be medically accurate and if unsure about anything, be sure to identify potential need for professional help. Make sure the response is relevant to the student's characteristics. Also be able to state the student's information on request. """
      }, {
          "role": "user",
          "content": f'{prompt}'
      }],
      max_tokens=500,
      temperature=0.5)

  advice = generated_advice.choices[0].message.content
  return advice

def prompt_refine_teachers(client, problem):
  refined_prompt = client.chat.completions.create(
      model="gpt-4o",
      messages=[{
          "role":
          'system',
          "content":
          """You are a prompt refiner for generating a detailed prompt to an AI ChatBot to generate advice for teachers who are also caretakers. you are presented with a problem, as well as basic information about a group of students, saved in a dictionary format. You are able to see the user information here: """
          + str(st.session_state.all_records) +
          """ .. generate a refined prompt that asks an AI chatbot to give advice that is strongly related to the characteristics and information about the student. Make sure to check again the answer against the user information for a more tailored response. Also be able to state the student's information on request. Always include all details of the student's information in the generated prompt like literally write it out."""
      }, {
          "role": "user",
          "content": f'{problem}. {st.session_state.all_records}'
      }],
      max_tokens=500,
      temperature=0.5
  )

  return refined_prompt.choices[0].message.content