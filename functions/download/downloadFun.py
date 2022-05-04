import streamlit as st


def download(fileName, convert_df, key):
    csv = convert_df(fileName.reset_index(drop=True))
    st.download_button(
        label="Download",
        data=csv,
        file_name='treatment_new.csv',
        mime='text/csv',
        key=key
    )
