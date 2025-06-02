"""
Author: Ben Xiao

Requirements:

1. Log a mood with an emoji dropdown
    - optional: add free text box
    - append to Google sheet
2. Construct a bar chart of mood counts for today


Notes

- Using streamlit
- use datetime for today
- Load google sheet from account benjamin.y.xiao@gmail.com

"""
from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file("credentials.json", scopes = scopes)
client = gspread.authorize(creds)

# Google sheet location
sheet_id = "14O9Vhrlotm00ueDidCt3Ud6Kq3vZg_NdKTwIti04Vo8"
sheet = client.open_by_key(sheet_id)


def create_day_hist(data, date):
    """
    Create bar chart a single day's data
    """
    today_data = data.loc[data["date"] == date]

    return px.histogram(today_data, x="mood")

def load_sheet(sheet) -> pd.DataFrame:
    """
    Load a sheet's data into a pandas dataframe
    """
    values = sheet.sheet1.get_all_values()

    return pd.DataFrame(data=values[1:], columns=values[0])

def update_sheet(sheet, values):
    """
    Update existing sheet by appending new row of inputs from user
    """
    sheet.sheet1.append_row(values)

"""
Create streamlit app to take emoji as input
    - make a small free text box for any special notes
"""
TODAY_DATE = str(datetime.today().strftime("%Y-%m-%d"))

# Streamlit elements
with st.form("mood_log"):
    st.write("Log your mood today")
    mood = st.selectbox(
        "How are you feeling today?",
        ("Happy", "Neutral", "Sad", "Frustrated")
    )

    notes = st.text_input(
        label="Log any notes"
    )
    submitted = st.form_submit_button("Submit")

    if submitted: # when submitted
        data = [TODAY_DATE, mood, notes]
        update_sheet(sheet, data)

# Draw bar chart
mood_data = load_sheet(sheet)
st.write(mood_data)
chart = create_day_hist(mood_data, TODAY_DATE)

st.plotly_chart(chart)
