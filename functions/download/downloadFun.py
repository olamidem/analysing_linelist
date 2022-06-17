import streamlit as st


def download(fileName, convert_df, key):
    csv = convert_df(fileName.reset_index(drop=True))
    st.download_button(
        label="Download Report",
        data=csv,
        file_name='report.csv',
        mime='text/csv',
        key=key
    )