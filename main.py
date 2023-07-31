import streamlit as st
from read_doc import read_doc
from open_ai import prompt_open_ai

st.set_page_config(
    page_title="Main",
    layout="wide"
)

# Initialize session state variables
if 'saved_paragraphs' not in st.session_state:
    st.session_state.saved_paragraphs = []

# Initialize session state variables
if 'long_response' not in st.session_state:
    st.session_state.long_response = ""

# Initialize session state variables
if 'option' not in st.session_state:
    st.session_state.option = ""

response_short = ""
response_long = ""

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    section_paragraph = read_doc(uploaded_file)
    titles = [i for i in section_paragraph.keys()]

    option = st.selectbox(
        'Paragraphs identified',
        (titles))

    st.write(section_paragraph[option])

    text_input_long = st.text_area('OpenAI Long Shot','''
    Rewrite below paragraph with the following rules:
    - If present, do not exclude any sub-paragraph and keep the number and title.
    - Make it more high level, principle-based and reader friendly.
    - Improve language and grammar.
    - Improve logical articulation of contents.
    - Do not add any new information on top of what's provided.
    - Do not change the meaning of the paragraph.
    ''', height=250)

    if st.button('Generate') and option is not None and text_input_long is not None:
        response_long = prompt_open_ai(text_input_long, section_paragraph[option])

        if response_long is not None:
            st.markdown(response_long)
            st.session_state.long_response = response_long
            st.session_state.option = option

    if st.button('Save'):
        # Save the paragraph and response to session state
        saved_paragraph = {
            'title': st.session_state.option,
            'response': st.session_state.long_response
        }
        st.session_state.saved_paragraphs.append(saved_paragraph)

    if st.button('Show Saved'):
        # Show saved paragraphs
        st.write('Saved Paragraphs:')
        for paragraph in st.session_state.saved_paragraphs:
            st.markdown(f"**Title:** {paragraph['title']}")
            st.markdown(f"**Response:** {paragraph['response']}")
            st.markdown('---')

    if st.button('Clear Saved'):
        # Clear saved paragraphs
        st.session_state.saved_paragraphs = []
        st.session_state.long_response = ""
        st.session_state.option = ""

else:
    st.write('Please upload a document')
