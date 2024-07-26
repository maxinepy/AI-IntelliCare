from annotated_types import Len
import streamlit as st
import database as db

class Info:

    def __init__(self):
        self.dw = db.DataWriter()
        self.worksheet_name = st.session_state.user['Worksheet Name']
        self.role = st.session_state.user['Role']
        self.name = ''
        self.age = 0
        self.gender = ''
        self.medical_conditions_str = ''
        self.medical_conditions = []
        self.allergies_str = ''
        self.allergies = []
        self.medication_str = ''
        self.medication = []
        self.current_parenting_style = ''
        self.pref_parenting_style = ''
        
        self.medi_dict = self.dw.get_medications(self.worksheet_name)

        if self.name not in self.medi_dict:
            self.medi_dict[self.name] = {}

        self.medi_dict[self.name]["medi_name"] = self.medication
        self.medi_dict[self.name]["last_time_taken"] = [
            None
        ] * len(self.medication)
        self.medi_dict[self.name]["take_now"] = [False
                                             ] * len(self.medication)
        self.medi_dict[self.name]["dosage"] = [None
                                           ] * len(self.medication)
        self.medi_dict[self.name]["frequency"] = [None
                                              ] * len(self.medication)


    def info(self):
        keyword = 'Children' if self.role == 'Parent' else 'Student(s)'
            
        st.subheader(f"Getting to Know Your {keyword} More")
        worksheet_name = st.session_state.user["Worksheet Name"]
        username = st.session_state.user['Username']
        st.subheader(f"{' '.join(word.capitalize() for word in username.split())}'s {keyword}")
        self.dw.display_sheet(worksheet_name)

        if st.button('Refresh'):
            st.rerun()

    def popover_explanation(self):
      with st.popover("Explanation on Parenting Styles"):
        st.markdown("**Parenting Styles**")
        st.caption("Gentle")
        st.write("Emphasizes empathy, respect, and understanding. It focuses on fostering a strong, positive relationship between parent and child, encouraging cooperation rather than using punishment or strict discipline.")

        st.caption("Authoritarian")
        st.write("Low responsiveness and high demands. Parents enforce strict rules and expect obedience without much warmth or feedback. Communication is usually one-way, from parent to child.")       

        st.caption("Authorative")
        st.write("High responsiveness and high demands. Parents are both supportive and demanding, setting clear standards and expectations while being attentive to their child's needs and feelings.")

        st.caption("Permissive")
        st.write("High responsiveness and low demands. Parents are indulgent and lenient, often acting more like friends than authority figures. They set few boundaries and allow considerable self-regulation.")

        st.caption("Uninvolved")
        st.write("Low responsiveness and low demands. Parents are detached and uninvolved, providing little guidance, nurturing, or attention. This style often results from various factors, including stress, depression, or a lack of parenting skills.")
                    
    @st.experimental_dialog(title="Add")
    def add_dialog(self):
        self.name = st.text_input("Name")
        self.age = st.slider('Age', min_value=0, max_value=21)
        self.gender = st.radio('Gender', ['Male', 'Female'])
        self.medical_conditions_str = st.text_input("Medical Conditions")
        self.medical_conditions = self.medical_conditions_str.split(',')
        self.allergies_str = st.text_input("Allergies")
        self.allergies = self.allergies_str.split(',')
        self.medication_str = st.text_input("Current Medication")
        self.medication = self.medication_str.split(',')
        self.current_parenting_style = None
        self.pref_parenting_style  = None

        if st.session_state.user["Role"] == "Parent":
            # parenting styles
            self.current_parenting_style = st.radio('Your Current Parenting Style', [
                'Gentle', 'Authoritarian', 'Authoritative', 'Permissive',
                'Uninvolved'
            ])
    
            self.popover_explanation()
    
            self.pref_parenting_style = st.radio(
                'Your Preferred Parenting Style',
                ['Gentle', 'Authoritarian', 'Authoritative', 'Permissive'])

        button = st.button('Submit')
        
        if button:
            if len(self.name) == 0:
                st.write("Name, age and gender is required.")
                
            else:
                # Show details
                st.markdown(f"""
                  Here are the details you provided: 
                  - Name: **{self.name}**
                  - Age: **{self.age}**
                  - Gender: **{self.gender}**
                  """)
                
                if self.role == 'Parent':
                    st.markdown(f"""
                    - Current Parenting Style: **{self.current_parenting_style}**
                    - Preferred Parenting Style: **{self.pref_parenting_style}** """)

                st.write("Medical Conditions:")
                for conditions in self.medical_conditions:
                    if conditions == '':
                        st.markdown('- None')
                    else:
                        st.markdown(f"""- {conditions}""")

                st.write("Allergies:")
                for allergies in self.allergies:
                    if allergies == '':
                        st.markdown('- None')
                    else:
                        st.markdown(f"""- {allergies}""")

                st.write("Current Medication:")
                for medication in self.medication:
                    if medication == '':
                        st.markdown('- None')
                    else:
                        st.markdown(f"""- {medication}""")

                # Write to database
                with st.spinner("Adding to database..."):
                    if self.role == "Teacher":
                        added = self.dw.write_sheet(worksheet_name= self.worksheet_name,
                                       data=[
                                           self.name, self.age, self.gender,
                                           self.medical_conditions_str,
                                           self.allergies_str, self.medication_str
                                       ])
                    else:
                        added = self.dw.write_sheet(worksheet_name= self.worksheet_name,
                                    data = [self.name, self.age, self.gender,                 self.medical_conditions_str, self.allergies_str, self.medication_str, "", "", "", self.current_parenting_style, self.pref_parenting_style])
    
                    if added == "Data updated successfully":
                        st.success("Added successfully!")
                        st.success("Please close this pop up and hit the refresh button! :)")
                    else:
                        st.error("Add Failed :( Please try again.")
         
    
    @st.experimental_dialog(title="Update")
    def update_dialog(self):
        total_records = st.session_state.all_records
        id = st.text_input("Row number of student to update")
        
        if len(id) != 0 and int(id) > -1 and int(id) < len(total_records):
            st.write("What would you like to update?")
            update_name = st.checkbox("Name")
            update_age = st.checkbox('Age')
            update_gender = st.checkbox('Gender')
            update_medical_conditions = st.checkbox('Medical Conditions')
            update_allergies = st.checkbox('Allergies')
            update_medications = st.checkbox('Medications')
            update_current_parenting_style = None
            update_preferred_parenting_style = None
            if self.role == "Parent":
                update_current_parenting_style = st.checkbox('Current Parenting Style')
                update_preferred_parenting_style = st.checkbox('Preffered Parenting Style')

            new_name = ""
            new_age = -1
            new_gender = ""
            new_medical_cond = ""
            new_allergies = ""
            new_medications = ""
            new_current_parenting_style = ""
            new_preferred_parenting_style = ""
            
            if update_name:
                new_name = st.text_input('New Name')
                
            if update_age:
                new_age = st.slider('New Age', min_value=0, max_value=21)


            if update_gender:
                new_gender = st.radio('New Gender', ['Male', 'Female'])
                
                    
            if update_medical_conditions:
                new_medical_cond = st.text_input('New Medical Condition(s) (Please include all current medical condition(s))')
                
                    
            if update_allergies:
                new_allergies = st.text_input('New Allergies (Please include all allergies)')
                
                    
            if update_medications:
                new_medications = st.text_input('New Medication(s) (Please include all medications)')

            if update_current_parenting_style:
                new_current_parenting_style = st.radio(
                    'Your Current Parenting Style',
                    ['Gentle', 'Authoritarian', 'Authoritative', 'Permissive'])

            if update_preferred_parenting_style:
                new_preferred_parenting_style = st.radio(
                    'Your Preferred Parenting Style',
                    ['Gentle', 'Authoritarian', 'Authoritative', 'Permissive'])
                
            done = st.button('Done')
            updated = ''
            
            if done:
                with st.spinner("Updating..."):
                    if len(new_name) != 0:
                        updated = self.dw.update_cell(worksheet_name=self.worksheet_name,
                                             row=int(id) + 2,
                                             col='Name',
                                             value=new_name)
                    if new_age >= 0:
                        updated = self.dw.update_cell(worksheet_name=self.worksheet_name,
                             row=int(id) + 2,
                             col='Age',
                             value=str(new_age))
                    if new_gender == 'Male' or new_gender == 'Female':
                        updated = self.dw.update_cell(worksheet_name=self.worksheet_name,
                             row=int(id) + 2,
                             col='Gender',
                             value=new_gender)
                    if len(new_medical_cond) != 0:
                        updated = self.dw.update_cell(worksheet_name=self.worksheet_name,
                             row=int(id) + 2,
                             col='Medical Conditions',
                             value=new_medical_cond)
                    if len(new_allergies) != 0:
                       updated = self.dw.update_cell(worksheet_name=self.worksheet_name,
                             row=int(id) + 2,
                             col='Allergies',
                             value=new_allergies)
                    if len(new_medications) != 0:
                        updated = self.dw.update_cell(worksheet_name=self.worksheet_name,
                             row=int(id) + 2,
                             col='Medications',
                             value=new_medications)
    
                    if len(str(new_current_parenting_style)) > 0:
                        updated = self.dw.update_cell(worksheet_name=self.worksheet_name,
                             row=int(id) + 2,
                             col='Current Parenting Style',
                             value=str(new_current_parenting_style))
    
                    if len(str(new_preferred_parenting_style)) > 0:
                        updated = self.dw.update_cell(worksheet_name=self.worksheet_name,
                             row=int(id) + 2,
                             col='Preffered Parenting Style',
                             value=str(new_preferred_parenting_style))
    
                    if updated == "Cell updated successfully.":
                        st.success("Updated successfully!")
                        st.success("Please close this pop up and hit the refresh button! :)")
                    else:
                        st.error("Update Failed :( Please try again.")
    
    @st.experimental_dialog(title="Delete")
    def delete_dialog(self):
        total_records = st.session_state.all_records
        id = st.text_input("Namelist row of student to delete")
        
        if len(id) == 0:
            st.error("Row Number is required for deleting data.")
        elif int(id) < 0 or int(id) > len(total_records) -1:
            st.error("Row Number is out of range.")
        else:
            with st.spinner("Deleting..."):
                deleted = self.dw.delete_row(worksheet_name=self.worksheet_name,
                                      row_number=int(id) + 2)
                if deleted == "Individual deleted successfully":
                    st.success("Deleted successfully!")
                    st.success("Please close this pop up and hit the refresh button! :)")
                else:
                    st.error("Delete Failed :( Please try again.")
            