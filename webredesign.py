import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import base64

def chunk_string(string, length):
    for i in range(0, len(string), length):
        yield string[i:i + length]

def get_modifications(chunk, instructions, api_key):
    openai.api_key = api_key
    prompt = f"Modify this HTML chunk based on these instructions:\nInstructions: {instructions}\nHTML Chunk:\n{chunk}"
    response = openai.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )
    return response.choices[0].text.strip()

st.title("Web Page Modifier")

url = st.text_input("Enter the URL of the web page:")
modification_request = st.text_area("Describe the modifications you want in natural language:")

if url and modification_request:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    full_html_content = soup.prettify()
    st.text_area("Original HTML", full_html_content, height=300)

    # Retrieve the OpenAI API key from Streamlit secrets
    api_key = st.secrets["OPENAI_API_KEY"]

    html_chunks = list(chunk_string(full_html_content, 2000))
    modified_html_chunks = []

    for chunk in html_chunks:
        modified_chunk = get_modifications(chunk, modification_request, api_key)
        modified_html_chunks.append(modified_chunk)

    final_modified_html = ''.join(modified_html_chunks)
    st.text_area("Modified HTML", final_modified_html, height=300)
    
    b64 = base64.b64encode(final_modified_html.encode()).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="modified_page.html">Download Modified HTML</a>'
    st.markdown(href, unsafe_allow_html=True)
