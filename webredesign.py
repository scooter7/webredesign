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
modified_html = ""

if fetch_button and url:
    response = requests.get(url)
    html_content = response.text
    st.text_area("Original HTML:", html_content, height=300)

instructions = st.text_area("Enter your modification instructions:", height=100)

if instructions and html_content:
    modify_button = st.button("Modify Webpage")

    if modify_button:
        # Creating a prompt for OpenAI
        prompt = f"Here is a webpage HTML source code:\n{html_content}\n\nMake the following changes to the HTML source code based on these instructions:\n{instructions}\n\nModified HTML:"

        # Process instructions with OpenAI
        response = openai.completions.create(
            model="text-davinci-004", 
            prompt=prompt, 
            max_tokens=500
        )

        modified_html = response.choices[0].text.strip()

        # Check if the model provided a modification
        if modified_html:
            st.text_area("Modified HTML:", modified_html, height=300)
            st.download_button("Download Modified HTML", modified_html, "modified.html")
        else:
            st.error("No modifications were made. Please refine your instructions.")
