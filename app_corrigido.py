import streamlit as st
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title='AI Interview Chatbot', page_icon=':left_speech_bubble:')
st.title('AI Interview Chatbot')

api_key = st.text_input("Enter your OpenAI API Key", type="password")
if not api_key:
    st.warning("Please enter an API key to proceed.")
    st.stop()

client = OpenAI(api_key=api_key)

# Initialize session state
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "messages" not in st.session_state:
    st.session_state.messages = []

def complete_setup():
    st.session_state.setup_complete = True

if not st.session_state.setup_complete:
    st.subheader('Personal Information', divider='rainbow')

    st.session_state["name"] = st.text_input('Name', max_chars=40, placeholder='Enter your name')
    st.session_state["experience"] = st.text_area('Experience', max_chars=200, placeholder='Describe your experience')
    st.session_state["skills"] = st.text_area('Skills', max_chars=200, placeholder='List your skills')

    st.subheader('Company and Position', divider='rainbow')
    
    st.session_state['level'] = st.radio("Choose Level", options=['Junior', 'Mid-Level', 'Senior'])
    st.session_state['position'] = st.selectbox("Choose Position", options=['Software Engineer', 'Data Scientist', 'Product Manager'])
    st.session_state['company'] = st.selectbox("Choose Company", options=['ABC Corp', 'XYZ Inc', 'DEF Industries'])

    if st.button('Start Interview', on_click=complete_setup):
        st.write("Setup Complete. Starting Interview...")

if st.session_state.setup_complete:
    st.info("Start by introducing yourself.", icon="👋")

    if not st.session_state.messages:
        st.session_state.messages.append({
            'role': 'system',
            'content': (
                f"You are an HR executive interviewing {st.session_state['name']} "
                f"who has experience: {st.session_state['experience']} and skills: {st.session_state['skills']}. "
                f"Interview them for the {st.session_state['level']} {st.session_state['position']} role at {st.session_state['company']}."
                "Send one question at a time and let the candidate respond naturally."
            )
        })

    for message in st.session_state.messages:
        if message['role'] != 'system':
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    if prompt := st.chat_input("Your response..."):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
            response_text = ""
            stream = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{'role': m['role'], 'content': m['content']} for m in st.session_state.messages],
                stream=True
            )
            
            response_container = st.empty()
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content
                    response_container.write(response_text)

        st.session_state.messages.append({'role': 'assistant', 'content': response_text})
    
    if st.button("Restart Interview"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
