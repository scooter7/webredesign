import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import base64

st.title("Web Page Modifier")

url = st.text_input("Enter the URL of the web page:")
modification_request = st.text_area("Describe the modifications you want in natural language:")

if url and modification_request:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    st.text_area("Original HTML", soup.prettify(), height=300)

    html_content = soup.prettify()[:2000]  # Adjust as needed to fit within token limits

    openai.api_key = st.secrets["OPENAI_API_KEY"]
    prompt = f"Here is the HTML source code:\n{html_content}\n\nApply the following changes based on these instructions:\n{modification_request}"
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
