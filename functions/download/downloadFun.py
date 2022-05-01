import streamlit as st


def download(art_start, convert_df, key):
    csv = convert_df(art_start.reset_index(drop=True))
    st.download_button(
        label="Download",
        data=csv,
        file_name='treatment_new.csv',
        mime='text/csv',
        key=key
    )
