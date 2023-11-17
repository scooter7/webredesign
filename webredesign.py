import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import base64

st.title("Web Page Modifier")

# Input for URL
url = st.text_input("Enter the URL of the web page:")
response = None
soup = None

# Fetching and displaying the source code of the URL
if url:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    st.text_area("Source Code", soup.prettify(), height=300)

# Input for modification instructions
modification_request = st.text_area("Describe the modifications you want:")

# Processing the modification request
if modification_request and soup:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    detailed_prompt = (
        f"Here is the HTML source code:\n{soup.prettify()}\n\n"
        f"Make the following changes to the HTML source code based on these instructions:\n{modification_request}\n\n"
        "Modified HTML:"
    )
    response = openai.completions.create(
        model="text-davinci-003",  # Replace with the correct GPT-4 model identifier
        prompt=detailed_prompt,
        max_tokens=1000
    )

    modified_html = response.choices[0].text.strip()
    if modified_html:
        st.text_area("Modified HTML/CSS", modified_html, height=300)

        # Parse the modified HTML
        modified_soup = BeautifulSoup(modified_html, 'html.parser')

        # Merging the generated code with the original HTML
        # Implementing a more sophisticated logic here based on the nature of modifications
        # This can include checking for new styles, structural changes, new elements, etc.

        # Example: If new styles are added, append them to the head
        for style in modified_soup.find_all("style"):
            soup.head.append(style)

        # Example: If new body content is added, insert it
        new_body = modified_soup.body
        if new_body:
            soup.body.replace_with(new_body)

        # Final modified HTML
        final_modified_html = soup.prettify()
        st.text_area("Final Modified Source Code", final_modified_html, height=300)

        # Providing a download link for the modified HTML
        b64 = base64.b64encode(final_modified_html.encode()).decode()
        href = f'<a href="data:file/html;base64,{b64}" download="modified_page.html">Download Modified HTML</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("No modifications were made. Please refine your instructions.")
