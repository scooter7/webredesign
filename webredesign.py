import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import base64

def chunk_string(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

st.title("Web Page Modifier")

url = st.text_input("Enter the URL of the web page:")
response = None
soup = None

if url:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    st.text_area("Source Code", soup.prettify(), height=300)

modification_request = st.text_area("Describe the modifications you want:")

if modification_request and soup:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    html_chunks = list(chunk_string(soup.prettify(), 1000))
    modified_html = ""

    for chunk in html_chunks:
        detailed_prompt = (
            f"Modify this HTML code based on the instructions:\n\n"
            f"HTML Code:\n{chunk}\n\n"
            f"Instructions: {modification_request}\n\n"
            "Modified HTML:"
        )
        response = openai.completions.create(
            model="text-davinci-003",  # Replace with the correct GPT-4 model identifier
            prompt=detailed_prompt,
            max_tokens=1000
        )

        generated_code = response.choices[0].text.strip()
        modified_html += generated_code

    st.text_area("Modified HTML/CSS", modified_html, height=300)

    b64 = base64.b64encode(modified_html.encode()).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="modified_page.html">Download Modified HTML</a>'
    st.markdown(href, unsafe_allow_html=True)
