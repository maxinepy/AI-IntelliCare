import streamlit as st
import database as db
import datetime 
import pandas as pd
from zoneinfo import ZoneInfo

# Create a GMT+8 timezone object
gmt_plus_8 = ZoneInfo("Asia/Hong_Kong")

dw = db.DataWriter()

def calculate_next_time(last_time, frequency):
    if not last_time or not frequency:
        return None

    try:
        last_time = datetime.datetime.strptime(last_time, "%d-%m-%Y %H:%M")
        frequency = float(frequency)
        if frequency <= 0:
            return f"Invalid frequency: {frequency}"
        hours_to_add = 24 / frequency

        next_time = last_time + datetime.timedelta(hours=hours_to_add)

        return next_time.strftime("%d-%m-%y %H:%M")
    except ValueError as e:
        return f"Error: {str(e)}"

def medi_reminder():
    if 'medi_dict' not in st.session_state:
        st.session_state.medi_dict = dw.get_medications(st.session_state.user['Worksheet Name'])

    for child_name in st.session_state.medi_dict:
        st.write(child_name)
        medi_dict = st.session_state.medi_dict[child_name]

        if f'df_{child_name}' not in st.session_state:
            medi_names = medi_dict.get("medi_name", [])
            dosages = medi_dict.get("dosage", [None] * len(medi_names))
            frequencies = medi_dict.get("frequency", [None] * len(medi_names))
            last_times_taken = medi_dict.get("last_time_taken", [None] * len(medi_names))

            max_length = max(len(medi_names), len(dosages), len(frequencies), len(last_times_taken), 2)
            medi_names = medi_names + [None] * (max_length - len(medi_names))
            dosages = dosages + [None] * (max_length - len(dosages))
            frequencies = frequencies + [None] * (max_length - len(frequencies))
            last_times_taken = last_times_taken + [None] * (max_length - len(last_times_taken))

            next_times_to_take = [calculate_next_time(last, freq) for last, freq in zip(last_times_taken, frequencies)]
            next_times_to_take = next_times_to_take + [None] * (max_length - len(next_times_to_take))

            st.session_state[f'df_{child_name}'] = pd.DataFrame({
                "Name of Medicine": medi_names,
                "Dosage": dosages,
                "Frequency in a day": frequencies,
                "Last Time Taken": last_times_taken,
                "Next Time to Take": next_times_to_take,
                "Take Now": [False] * max_length
            })

        edited_df = st.data_editor(
            st.session_state[f'df_{child_name}'],
            key=f"editor_{child_name}",
            column_config={
                "Take Now": st.column_config.CheckboxColumn(
                    "Take Now",
                    help="Check to mark as taken now",
                    default=False,
                ),
                "Next Time to Take": st.column_config.Column(
                    "Next Time to Take",
                    disabled=True
                )
            }
        )

        # Process "Take Now" actions
        changes_made = False
        for i in range(len(edited_df)):
            if edited_df.at[i, 'Take Now']:
                current_time = datetime.datetime.now(gmt_plus_8).strftime("%d-%m-%Y %H:%M")
                frequency = edited_df.at[i, 'Frequency in a day']
                next_time = calculate_next_time(current_time, frequency)
    
                edited_df.at[i, 'Last Time Taken'] = current_time
                edited_df.at[i, 'Next Time to Take'] = next_time
                edited_df.at[i, 'Take Now'] = False
                changes_made = True

        # Update the session state with the edited DataFrame
        st.session_state[f'df_{child_name}'] = edited_df
    
        # Update the medi_dict with the changes from the edited dataframe
        st.session_state.medi_dict[child_name]['medi_name'] = edited_df['Name of Medicine'].dropna().tolist()
        st.session_state.medi_dict[child_name]['dosage'] = edited_df['Dosage'].dropna().tolist()
        st.session_state.medi_dict[child_name]['frequency'] = edited_df['Frequency in a day'].dropna().tolist()
        st.session_state.medi_dict[child_name]['last_time_taken'] = edited_df['Last Time Taken'].dropna().tolist()
    
        if changes_made:
            st.rerun()
        
    if st.button("Save Changes"):
        dw.update_medications(st.session_state.user['Worksheet Name'], st.session_state.medi_dict)
        st.success("Changes saved successfully!")

