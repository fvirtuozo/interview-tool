AI Interview Chatbot - Project Overview and Code Explanation

📌 Project Overview
The AI Interview Chatbot is an interactive Streamlit application designed to help users practice for IT job interviews. It simulates a real interview experience by asking dynamic AI-generated questions, evaluating responses, and providing structured feedback.

This chatbot is particularly useful for individuals preparing for Software Engineering, Data Science, and Product Management roles.

🔹 Features
✅ Personalized Interview Experience – Users input their name, experience, and skills, and the AI tailors the interview accordingly.
✅ Role & Company Customization – Users select the job level (Junior, Mid, Senior) and company for a more realistic simulation.
✅ Real-Time AI Conversation – The chatbot asks one question at a time, allowing users to respond naturally.
✅ Scored Feedback System – After five interactions, AI provides an interview score (1-10) along with detailed feedback.
✅ Restart Option – Users can reset the chatbot and start a new interview.

🛠️ Technologies Used
Python – Main programming language.
Streamlit – Used to build the interactive UI.
OpenAI API – Powers the AI interview questions and feedback.
streamlit-js-eval – Used to reload the app for a new interview session.

## Installation  

### Prerequisites  
- Python 3.8+  
- OpenAI API key  

### Steps  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/ai-interview-chatbot.git
   cd ai-interview-chatbot
