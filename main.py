import streamlit as st
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain.schema import SystemMessage,HumanMessage


if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    load_dotenv()


# Page configuration
st.set_page_config(page_title="EduQuiz Generator", page_icon="🧠", layout="centered")

# App Title
st.title("🧠 EduQuiz Generator")
st.write("Create quiz questions instantly using AI")

# User Input
content = st.text_area("📘 Enter Topic or Paragraph", height=180)
quiz_type = st.selectbox("🧩 Select Quiz Type", ["MCQ", "True/False", "Fill-in-the-Blank"])
num_questions = st.number_input("🔢 Number of Questions", min_value=1, max_value=100, value=3, step=1)


# Prompt Generator
def generate_prompt(content, quiz_type, num_questions):
    if quiz_type == "MCQ":
        return (
            f"Generate {num_questions} MCQs from this content:\n\n\"\"\"{content}\"\"\"\n"
            "Each question must have 4 options (A-D) and clearly indicate the correct answer."
        )
    elif quiz_type == "True/False":
        return (
            f"Generate {num_questions} True/False questions from this content:\n\n\"\"\"{content}\"\"\"\n"
            "Indicate the correct answer after each question."
        )
    elif quiz_type == "Fill-in-the-Blank":
        return (
            f"Generate {num_questions} fill-in-the-blank questions from this content:\n\n\"\"\"{content}\"\"\"\n"
            "Put the correct answer in parentheses at the end of each question."
        )
# created the message
def message_create(prompt):
    message=[
        SystemMessage(content="You are a helpful AI tutor."),
        HumanMessage(content=prompt),
    ]
    return message

# ChatOpenAI Call
def get_quiz(prompt):
    chat_model=ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY") 
    )
    response=chat_model.invoke(message_create(prompt))
    return response.content

# Generate Button
if st.button("🚀 Generate Quiz"):
    if content.strip() == "":
        st.warning("Please enter some content to generate quiz.")
    else:
        with st.spinner("Generating quiz..."):
            prompt = generate_prompt(content, quiz_type, num_questions)
            result = get_quiz(prompt)
        st.success("✅ Quiz Generated!")
        st.markdown("### 📝 Generated Quiz:")
        st.code(result, language='markdown')
        st.download_button("📥 Download as Text", result, "quiz.txt", "text/plain")

