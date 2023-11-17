import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import base64

st.title("Web Page Modifier")

url = st.text_input("Enter the URL of the web page:")
modification_request = st.text_area("Describe the modifications you want in natural language:")

if url:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    full_html_content = soup.prettify()
    st.text_area("Original HTML", full_html_content, height=300)

if url and modification_request:
    # Limiting the HTML content to fit within the token limits of the OpenAI API
    limited_html_content = full_html_content[:2000]  # Adjust as needed

    openai.api_key = st.secrets["OPENAI_API_KEY"]
    prompt = f"Here is a portion of the HTML source code:\n{limited_html_content}\n\nApply the following changes based on these instructions:\n{modification_request}"
    response = openai.completions.create(
        model="text-davinci-003",  # Use the correct GPT model identifier
        prompt=prompt,
        max_tokens=1000  # Adjust based on your needs
    )

    modified_html = response.choices[0].text.strip()
    
    if modified_html:
        st.text_area("Modified HTML", modified_html, height=300)
        
        b64 = base64.b64encode(modified_html.encode()).decode()
        href = f'<a href="data:file/html;base64,{b64}" download="modified_page.html">Download Modified HTML</a>'
        st.markdown(href, unsafe_allow_html=True)
