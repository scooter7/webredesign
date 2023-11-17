import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import base64

# Initialize Streamlit app
st.title("Web Page Modifier")

# Input fields for URL and modifications
url = st.text_input("Enter the URL of the web page:")
modification_request = st.text_area("Describe the modifications you want:")

if url:
    # Fetch and display web page source
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    st.text_area("Source Code", soup.prettify(), height=300)

if modification_request:
    # Use OpenAI API for natural language processing
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    response = openai.chat.completions.create(
        model="text-davinci-003",  # Updated model name
        prompt=f"Translate this into HTML/CSS: {modification_request}",
        max_tokens=150
    )
    generated_code = response.choices[0].text.strip()
    st.text_area("Generated Code", generated_code)

        # Apply and display modifications (simplified example)
        new_style = soup.new_tag('style')
        new_style.string = generated_code
        soup.head.append(new_style)
        modified_html = soup.prettify()
        st.text_area("Modified Source Code", modified_html, height=300)

        # Create downloadable file
        b64 = base64.b64encode(modified_html.encode()).decode()
        href = f'<a href="data:file/html;base64,{b64}" download="modified_page.html">Download Modified HTML</a>'
        st.markdown(href, unsafe_allow_html=True)
