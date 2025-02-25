import streamlit as st
import pandas as pd

# Title of the app
st.title('Cricket Analysis Dashboard Test')

# Dropdown for format
format_option = st.selectbox('Select Format:', ['ODI', 'T20'])

# Button for testing
if st.button('Click me to display message'):
    st.write(f'You selected {format_option} format!')
