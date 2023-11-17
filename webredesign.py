import streamlit as st
import requests
import openai

# Fetch the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI
st.title("Webpage Modifier")
url = st.text_input("Enter the URL of the webpage:")
fetch_button = st.button("Fetch Webpage")
html_content = ""

if fetch_button and url:
    response = requests.get(url)
    html_content = response.text
    st.text_area("Original HTML:", html_content, height=300)

instructions = st.text_area("Enter your modification instructions:", height=100)
modify_button = st.button("Modify Webpage")

if modify_button and instructions and html_content:
    # Structuring the prompt for OpenAI in a more directive manner
    prompt = f"Given the HTML code:\n\n{html_content}\n\nApply these changes: {instructions}\n\nThe modified HTML should look like this:"

    # Process instructions with OpenAI
    try:
        response = openai.completions.create(
            model="text-davinci-004", 
            prompt=prompt, 
            max_tokens=1000
        )
        modified_html = response.choices[0].text.strip()

        # Check if the response is valid and display it
        if modified_html and modified_html != html_content:
            st.text_area("Modified HTML:", modified_html, height=300)
            st.download_button("Download Modified HTML", modified_html, "modified.html")
        else:
            st.warning("The model did not return any modifications. Please refine your instructions.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
