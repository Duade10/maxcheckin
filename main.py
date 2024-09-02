import streamlit as st
from utils import google_sheets
from datetime import datetime


def display_date():
    return datetime.now().strftime("%d/%m/%Y")


def get_load_from_db():
    pass


def main():
    st.markdown("# 📋 Control Room Data Table App")
    st.subheader("Here's a description of each of the pages")
    st.write(display_date())


if __name__ == "__main__":
    main()
