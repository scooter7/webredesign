import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import base64

st.title("Web Page Modifier")

url = st.text_input("Enter the URL of the web page:")
modification_request = st.text_area("Describe the modifications you want:")

if url:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    st.text_area("Source Code", soup.prettify(), height=300)

if modification_request:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    response = openai.completions.create(
        model="text-davinci-003",
        prompt=f"Translate this into HTML/CSS: {modification_request}",
        max_tokens=150
    )

    response_content = response.choices[0].text.strip()
    st.text_area("Generated HTML/CSS", response_content)

    if soup:
        # Assuming the response_content is CSS, you can create a new <style> tag and append it
        # If it's HTML, you might need to parse it and integrate it appropriately
        new_style = soup.new_tag('style')
        new_style.string = response_content
        soup.head.append(new_style)

        modified_html = soup.prettify()
        st.text_area("Modified Source Code", modified_html, height=300)

        b64 = base64.b64encode(modified_html.encode()).decode()
        href = f'<a href="data:file/html;base64,{b64}" download="modified_page.html">Download Modified HTML</a>'
        st.markdown(href, unsafe_allow_html=True)
