import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import base64

def get_modifications(html_snippet, instructions, api_key):
    openai.api_key = api_key
    prompt = f"Modify the following HTML snippet based on these instructions:\nInstructions: {instructions}\nHTML Snippet:\n{html_snippet}"
    response = openai.completions.create(
        model="text-davinci-003",  # Use the correct GPT model identifier
        prompt=prompt,
        max_tokens=500  # Adjust based on your needs
    )
    return response.choices[0].text.strip()

st.title("Web Page Modifier")

url = st.text_input("Enter the URL of the web page:")
modification_request = st.text_area("Describe the modifications you want:")

if url and modification_request:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    st.text_area("Original HTML", soup.prettify(), height=300)

    html_snippet = st.text_area("Enter the HTML snippet you want to modify:", height=150)

    if html_snippet:
        modified_html = get_modifications(html_snippet, modification_request, st.secrets["OPENAI_API_KEY"])
        
        if modified_html:
            st.text_area("Modified HTML", modified_html, height=300)
            
            b64 = base64.b64encode(modified_html.encode()).decode()
            href = f'<a href="data:file/html;base64,{b64}" download="modified_page.html">Download Modified HTML</a>'
            st.markdown(href, unsafe_allow_html=True)
