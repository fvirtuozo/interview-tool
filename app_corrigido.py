import os
from openai import OpenAI
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

api_key = os.getenv("OPENAI_API_KEY")  

st.set_page_config(page_title='Streamlit Chat', page_icon=':left_speech_bubble:')
st.title('Chatbot')

# Initialize session state variables
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

    # Add Personal Information
    st.subheader('Personal Information', divider='rainbow')

    st.session_state["name"] = st.text_input('Name', max_chars=40, placeholder='Enter your name')
    st.session_state["Experience"] = st.text_area('Experience', value='', max_chars=200, placeholder='Describe your experience')
    st.session_state["Skills"] = st.text_area('Skills', value='', max_chars=200, placeholder='List your skills')



    st.subheader('Company and Position', divider='rainbow')

    col1, col2 = st.columns(2)

    with col1:
        st.session_state['level'] = st.radio("Choose Level", options=['Junior', 'Mid-Level', 'Senior'])

    with col2:
        st.session_state['position'] = st.selectbox("Choose Position", options=['Software Engineer', 'Data Scientist', 'Product Manager'])

    st.session_state['company'] = st.selectbox("Choose Company", options=['ABC Corp', 'XYZ Inc', 'DEF Industries'])

    if st.button('Start Interview', on_click=complete_setup):
        st.write("Setup Complete. Starting Interview...")

if st.session_state.setup_complete and not st.session_state.chat_complete and not st.session_state.feedback_shown:
    st.info("Start by introducing yourself.", icon="👋")

    # Initialize OpenAI client
    client = OpenAI()
    if 'openai_model' not in st.session_state:
        st.session_state['openai_model'] = 'gpt-4o-mini'

    # Prepare initial system message
    if not st.session_state.messages:
        st.session_state.messages.append({
            'role': 'system',
            'content': (
                f"You are an HR executive interviewing {st.session_state['name']} "
                f"who has experience: {st.session_state['Experience']} and skills: {st.session_state['Skills']}. "
                f"Interview them for the {st.session_state['level']} {st.session_state['position']} role at {st.session_state['company']}."
                f"Send one question each time, do not send everything at once, let the candidate answer as if he was in the real process"
            )
        })

    for message in st.session_state.messages:
        if message['role'] != 'system':
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    if st.session_state.user_message_count < 5:
        if prompt := st.chat_input("How can I help you today?", max_chars=200):
            st.session_state.messages.append({'role': 'user', 'content': prompt})

            with st.chat_message('user'):
                st.markdown(prompt)

            if st.session_state.user_message_count < 4:
                with st.chat_message('assistant'):
                    response_text = ""
                    stream = client.chat.completions.create(
                        model=st.session_state['openai_model'],
                        messages=[{'role': m['role'], 'content': m['content']} for m in st.session_state.messages],
                        stream=True
                    )
                    
                    # Stream response
                    response_container = st.empty()
                    for chunk in stream:
                        if chunk.choices and chunk.choices[0].delta.content:
                            response_text += chunk.choices[0].delta.content
                            response_container.write(response_text)

                st.session_state.messages.append({'role': 'assistant', 'content': response_text})
            
            st.session_state.user_message_count += 1

    if st.session_state.user_message_count >= 5:
        st.write("Interview Complete")
        st.session_state.chat_complete = True
        

if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("Get Feedback", on_click=show_feedback):
        st.write("Fetching feedback...")
    

        
if st.session_state.feedback_shown:
    st.subheader('feedback')
    conversation_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

    feedback_client = OpenAI()
    
    feedback_completion = feedback_client.chat.completions.create(
        model='gpt-4o-mini',
        temperature=0.7,
        max_tokens=100,
        messages=[
            {"role": "system", "content": """You are a helpful tool that provides feedback on an interviewee performance
             Before the Feedback give a score of 1 to 10
             Follow this format:
             Overwall Score: //Your score
             Feedback: //Here you put your feedback
             Give only the feedback do not ask aditional questions."""},
            { "role": "user", "content": f"""This is the interview you need to evaluate. Keep in mind that you are only a tool.
             and you shouldn't engage in conversation. {conversation_history}"""}])

    st.write(feedback_completion.choices[0].message.content)

    if st.button("Restart Interview", type="primary"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
  
