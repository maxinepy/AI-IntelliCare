import gspread
from gspread import worksheet
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
# from streamlit_gsheets import GSheetsConnection
import pandas as pd
from typing import List

class DataWriter:
    def __init__(self):
        self.sheet_name = "IntelliCareSheet"
        
    # Function to authenticate and get the Google Sheets client
    def get_google_sheets_client(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        return client

    def get_db(self, worksheet_name):
        return self.get_google_sheets_client().open(self.sheet_name).worksheet(worksheet_name)

    def get_worksheet_name(self, username, role):
        role_prefix = 'T_' if role == 'Teacher' else 'P_'
        worksheet_name = f"{role_prefix}{username}"
        return worksheet_name

    def create_new_worksheet(self, username, role):
        try:
            client = self.get_google_sheets_client()
            sheet = client.open(self.sheet_name)

            worksheet_name = self.get_worksheet_name(username, role)

            try:
                sheet.worksheet(worksheet_name)
                return f"Worksheet '{worksheet_name}' already exists."
            except gspread.exceptions.WorksheetNotFound:

                # create a new worksheet with the username
                new_worksheet = sheet.add_worksheet(title=worksheet_name, rows=100, cols=20)
    
                common_headers = ["Name", "Age", "Gender", "Medical Conditions", "Allergies", "Medications", "Medication Dosage", "Medication Frequency", "Medication Last Taken"]
                if role == 'Teacher':
                    headers = common_headers
                else:  # Parent
                    headers = common_headers + ['Current Parenting Style', 'Preferred Parenting Style']
    
                # Add headers to the new worksheet
                new_worksheet.update('A1', [headers]) # type: ignore
    
                return f"New worksheet '{worksheet_name}' created successfully."
    
        except Exception as e:
            return f"An error occcured while creating the worksheet: {str(e)}"

    # Function to read data from Google Sheets
    def read_sheet(self, worksheet_name):
        client = self.get_google_sheets_client()
        sheet = client.open(self.sheet_name).worksheet(worksheet_name)
        data = sheet.get_all_records()
        return data

    # Function to read data and store in a dictionary
    def get_all_records_as_dict(self, worksheet_name):
        records = self.read_sheet(worksheet_name)
        records_dict = {}
        for index, record in enumerate(records, start=1):
            records_dict[index] = record
        return records_dict
    
    # Function to write data to Google Sheets
    def write_sheet(self, worksheet_name, data):
        client = self.get_google_sheets_client()
        sheet = client.open(self.sheet_name).worksheet(worksheet_name)
        sheet.append_row(data)
        return "Data updated successfully"

    def update_row(self, worksheet_name, row_number, updated_values):
        if row_number <= 1 or not self.get_row(worksheet_name, row_number):
            return f"Individual at row {row_number - 2} not found"
        client = self.get_google_sheets_client()
        sheet = client.open(self.sheet_name).worksheet(worksheet_name)

        # Get the number of columns in the sheet
        num_cols = len(sheet.row_values(1))

        # Ensure updated_values has the correct number of columns
        if len(updated_values) < num_cols:
            updated_values.extend([''] * (num_cols - len(updated_values)))
        elif len(updated_values) > num_cols:
            updated_values = updated_values[:num_cols]

        # Update the row
        cell_range = f'A{row_number}:{chr(64+num_cols)}{row_number}'
        updated_values = [updated_values]
        sheet.update(cell_range, updated_values)

        return f"Row {row_number - 2} updated successfully"


    def delete_row(self, worksheet_name, row_number):
        client = self.get_google_sheets_client()
        sheet = client.open(self.sheet_name).worksheet(worksheet_name)

        if row_number <= 1:
            return f"Individual at row {row_number - 2} not found"
        row = self.get_row(worksheet_name, row_number)
        if row and row_number > 1:
            sheet.delete_rows(row_number)
            return "Individual deleted successfully"
        else:
            return f"Individual at row {row_number - 2} not found"

    
    def get_row(self, worksheet_name, row_index):
        client = self.get_google_sheets_client()
        sheet = client.open(self.sheet_name).worksheet(worksheet_name)

        st.write(sheet.cell(row_index, 1).value)
        if sheet.cell(row_index, 1).value:
            return sheet.row_values(row_index)
        else:
            return None

    def get_medications(self, worksheet_name):
        ret = {}
        for row in self.read_sheet(worksheet_name):
            if row.get("Medications"):
                ret[row.get("Name")] = {}
                medications = str(row.get("Medications")).split(',')
                frequencies = str(row.get("Medication Frequency")).split(',')
                dosages = str(row.get("Medication Dosage")).split(',')
                times = str(row.get("Medication Last Taken")).split(',')
                ret[row.get("Name")]["medi_name"] = medications
                ret[row.get("Name")]["frequency"] = frequencies
                ret[row.get("Name")]["dosage"] = dosages
                ret[row.get("Name")]["last_time_taken"] = times
        #st.write(ret)
        return ret

    def update_medications(self, worksheet_name, updated_medications):
        client = self.get_google_sheets_client()
        sheet = client.open(self.sheet_name).worksheet(worksheet_name)

        # Get all current data
        data = sheet.get_all_records()

        for student_name, med_info in updated_medications.items():
            # Find the row for the student
            student_row = None
            for index, row in enumerate(data):
                if row['Name'].strip().lower() == student_name.strip().lower():
                    student_row = index
                    break

            if student_row is not None:
                # Update the row with new medication information
                medications = ','.join(med_info['medi_name'])
                dosages = ','.join(med_info['dosage'])
                frequencies = ','.join(map(str, med_info['frequency']))
                last_times_taken = ','.join(med_info['last_time_taken'])

                # Update the cells
                sheet.update_cell(student_row + 2, sheet.find('Medications').col, medications)
                sheet.update_cell(student_row + 2, sheet.find('Medication Dosage').col, dosages)
                sheet.update_cell(student_row + 2, sheet.find('Medication Frequency').col, frequencies)
                sheet.update_cell(student_row + 2, sheet.find('Medication Last Taken').col, last_times_taken)

                st.write(f"Updated medication info for {student_name}")
            else:
                st.write(f"Student {student_name} not found in the sheet.")

        st.write("Medications update process completed.")

    def display_sheet(self, worksheet_name):
        dw = DataWriter()
        data = dw.read_sheet(worksheet_name)
        df = pd.DataFrame(data)

        st.dataframe(df)  # For an interactive dataframe

    def username_exists(self, username, role):
        login_data = self.read_sheet("Login")
        return any(record.get('username') == username and record.get('role') == role for record in login_data)
        
    def check_login(self, input_username: str, input_password: str, input_role):
        worksheet_name = "Login"
       
        # Get the login data from the Google Sheet
        login_data = self.read_sheet(worksheet_name)

        # Check if the input username and password match any in the sheet
        for row in login_data:
            role_data = row.get('role')
            if row.get('username') == input_username and str(row.get('password')) == input_password and role_data == input_role:
                return [True, role_data]
                
        # If no match is found after checking all rows
        return False

    def update_cell(self, worksheet_name, row, col, value):
        try:
            client = self.get_google_sheets_client()
            sheet = client.open(self.sheet_name).worksheet(worksheet_name)

            # If col is a string (column name), find its corresponding column number
            if isinstance(col, str):
                col_values = sheet.row_values(1)  # Get the first row (header)
                col = col_values.index(col) + 1  # Find the index of the column name and add 1 (as sheets are 1-indexed)
                
            # Update the specific cell
            sheet.update_cell(row, col, value)
    
            return "Cell updated successfully."
        except Exception as e:
            return f"An error occurred: {str(e)}"

        