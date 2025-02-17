import os
from openai import OpenAI
import streamlit as st

api_key = os.getenv("OPENAI_API_KEY")  

st.set_page_config(page_title='Streamlit Chat', page_icon=':left_speech_bubble:')
st.title('Chatbot')

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False

if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0

if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False

def complete_setup():
    st.session_state.setup_complete = True

def show_feedback():
    st.session_state.feedback_shown = True

if not st.session_state.setup_complete:

    #Add personal Information
    st.subheader('Personal Information', divider='rainbow')

    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "Experience" not in st.session_state:
        st.session_state["Experience"] = ""
    if "Skills" not in st.session_state:
        st.session_state["Skills"] = ""

    st.session_state["name"]= st.text_input('Name', max_chars=40, placeholder='Enter your name')

    st.session_state["Experience"] = st.text_area('Experience', value='', height=None, max_chars=200, placeholder='Describe your experience')

    st.session_state["Skills"]= st.text_area('Skills', value='', height=None,max_chars=200, placeholder='List your skills')

    st.write(f"**Your Name**: {st.session_state['name']}")
    st.write(f"**Your Experience**: {st.session_state['Experience']}")
    st.write(f"**Your Skills**: {st.session_state['Skills']}")

    st.subheader('Company and Position', divider='rainbow')


    col1, col2 = st.columns(2)

    with col1 :
        st.session_state['level'] = st.radio(
        "Choose Level",
        key = 'Visibility',
        options=['Junior', 'Mid-Level', 'Senior'],
    )

    with col2 :
        st.session_state['position'] = st.selectbox(
            "Choose Position",
            options=['Software Engineer', 'Data Scientist', 'Product Manager']
        )

    st.session_state['company'] = st.selectbox(
            "Choose Company",
            options=['ABC Corp', 'XYZ Inc', 'DEF Industries']
        )
    if st.button('Start Interview', on_click = complete_setup):
        st.write("Setup Complete. Strating Interview...")

if st.session_state.setup_complete and not st.session_state.chat_complete and not st.session_state.feedback_shown:
    st.info(
        '''Start by introducing yourself.''',
        icon = "👋"
    )

    #Initiating OpenAI
    client = OpenAI()
    if 'openai_model' not in st.session_state:
        st.session_state['openai_model'] = 'gpt-4o-mini'

    # Streamlit Interface
    if not st.session_state.messages:
        st.session_state.messages.append([{'role': 'system', 
        'content': 
            f"You are an HR executive that interviews and interviewee called   {st.session_state['name']} "
            f"with experience   {st.session_state['Experience']}  and skills {st.session_state['Skills']}."
            f"You should interview them for the position {st.session_state['level']}{ st.session_state['position']} at {st.session_state['company']} "}])

    for message in st.session_state.messages:
        if message['role'] != 'system':
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    if st.session_state.user_message_count < 5:

        if prompt:=st.chat_input("How can I help you today?", max_chars=200):
            # Ading user message to History
            st.session_state.messages.append({'role': 'user', 'content': prompt})

            # Show user input in chat
            with st.chat_message('user'):
                st.markdown(prompt)
            
            if st.session_state.user_message_count < 4:

                # Request to model

                with st.chat_message('assistant'):
                    response_text = ""
                    stream = client.chat.completions.create(
                        model=st.session_state['openai_model'],
                        messages=[
                                {'role': m['role'], 
                                'content': m['content']}
                                for m in st.session_state.messages]
                                        ,
                                stream=True
                            )
                    

                        # Capturar a resposta do modelo
                    
                    response_container = st.empty()
                    for chunk in stream:
                        if chunk.choices and chunk.choices[0].delta.content:
                            response_text += chunk.choices[0].delta.content
                            response_container.st.write(response_text)  # Atualiza dinamicamente a interface

                # Adicionar a resposta do assistente ao histórico
                st.session_state.messages.append({'role': 'assistant', 'content': response_text})

                st.session_state.user_message_count += 1

            if st.session_state.user_message_count >= 5:
                st.write("Interview Complete")
                st.session_state.chat_complete = True