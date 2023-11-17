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
    detailed_prompt = (
        "Generate complete and functional HTML/CSS code for the following modification: "
        f"'{modification_request}'."
    )
    response = openai.completions.create(
        model="text-davinci-003",  # Replace with the correct GPT-4 model identifier
        prompt=detailed_prompt,
        max_tokens=150
    )

    generated_code = response.choices[0].text.strip()
    st.text_area("Generated HTML/CSS", generated_code)

    if soup:
        if "<style>" in generated_code or "css" in modification_request.lower():
            style_tag = soup.new_tag("style")
            style_tag.string = generated_code
            soup.head.append(style_tag)
        else:
            new_content = BeautifulSoup(generated_code, 'html.parser')
            soup.body.insert(0, new_content)

        modified_html = soup.prettify()
        st.text_area("Modified Source Code", modified_html, height=300)

        b64 = base64.b64encode(modified_html.encode()).decode()
        href = f'<a href="data:file/html;base64,{b64}" download="modified_page.html">Download Modified HTML</a>'
        st.markdown(href, unsafe_allow_html=True)
