import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import os
from database import DataWriter

class MealScanner:

    
    def __init__(self):
      st.subheader('Meal Scanner :knife_fork_plate:')

      self.client = OpenAI(api_key=st.secrets['OPENAI_NANNY'])
      self.dw = DataWriter()  

    
    def scan_meal(self):
      pic = st.camera_input("Take a picture of the meal")

      if pic is not None:
        image = Image.open(pic)
        st.image(image, caption='Uploaded Meal Image', use_column_width=True)

        image_bytes = pic.getvalue()
        return image_bytes

    
    def upload_meal(self):
      uploaded_file = st.file_uploader("Upload a meal image", type=["jpg", "jpeg", "png"])

      if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Meal Image", use_column_width=True)

        image_bytes = uploaded_file.getvalue()
        return image_bytes

    
    def generate_ingredients(self, image_bytes):
      if image_bytes:
          base64_image = base64.b64encode(image_bytes).decode('utf-8')

          response = self.client.chat.completions.create(
              model="gpt-4o",
              messages=[
                  {
                      "role": "user",
                      "content": [
                          {"type": "text", "text": "Please analyze this image and provide a list of ingredients used in the meal. Be as specific as possible. Be straightforward and provide the ingredients and its breakdown for example cheese is made of milk. Do not provide any other additional irrelevant information."},
                          {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                      ]
                  }
              ],
              max_tokens=500,
              temperature = 0
          )

          ingredients = response.choices[0].message.content
          return ingredients
      else:
          return "No image provided for analysis."

    
    def check_allergies(self, ingredients):
        all_records = st.session_state.all_records
        allergies_data = []
        for _, record in all_records.items():
            allergies_data.append({
                "Name": record.get("Name", ""),
                "Allergies": record.get("Allergies", "")
            })
        
        ingredient_list = [ing.strip().lower() for ing in ingredients.split(',')]

        allergic_people = {}
        
        for person in allergies_data:
            name = person.get("Name")
            allergies = person.get("Allergies")

            if not isinstance(allergies, str):
                allergies = str(allergies)
                
            if allergies:
                person_allergies = [allergy.strip().lower() for allergy in allergies.split(',')]
                allergic_ingredients = set() # avoid duplicates

                for allergen in person_allergies:
                    for ingredient in ingredient_list:
                        if allergen in ingredient:
                            allergic_ingredients.add(allergen)
                            
                if allergic_ingredients:
                    allergic_people[name] = list(allergic_ingredients) # convert set back to list
                    
        return allergic_people

    
    def run(self):
      st.write("How would you want to input the meal image?")
      pic_on = st.toggle('Take a picture')
      if pic_on:
          image_bytes = self.scan_meal()
      else:
          image_bytes = self.upload_meal()
    
      if image_bytes:
          if st.button("Analyze Ingredients"):
              with st.spinner("Analyzing the meal..."):
                  ingredients = self.generate_ingredients(image_bytes)
                  st.success("Analysis complete!")
                  st.write(ingredients)

                  # Check for allergies
                  allergic_people = self.check_allergies(ingredients)
                  if allergic_people:
                      st.warning("Allergy Alert!")
                      for name, allergens in allergic_people.items():
                          st.write(f"**{name.strip()}** is allergic to: {', '.join(allergens)}")
                  else:
                      st.success("No allergies detected for any individuals.")
                  