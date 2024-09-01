import streamlit as st


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Google Sheet Processor", "Max Checkin"])

    if page == "Home":
        home_page()
    elif page == "Google Sheet Processor":
        google_sheet_processor_page()
    elif page == "Max Checkin":
        max_check_in()


def home_page():
    st.title("Welcome to the Multi-page App")
    st.write("This is the home page. Use the sidebar to navigate to different features.")


def google_sheet_processor_page():
    st.title("Google Sheet Data Processor")

    sheet_id = st.text_input("Enter Google Sheet ID")
    worksheet = st.text_input("Enter Worksheet Name")

    if st.button("Process Sheet"):
        if sheet_id and worksheet:
            process_sheet(sheet_id, worksheet)
        else:
            st.error("Please enter both Sheet ID and Worksheet Name")


def max_check_in():
    st.title("New Feature")
    st.write("This is where you can add your new feature.")
    # Add your new feature functionality here


if __name__ == "__main__":
    main()
