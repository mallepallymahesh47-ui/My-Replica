from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

# Setting up the envrionmental varibales
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
GROQ_KEY=os.getenv("GROQ_API_KEY")


# LLM's 
llm=ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_KEY)

# Chat Template
chat_prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You have to behave like Mahesh that is me and you are created by me, answer all the user questions. some information about me I like Playing cricket most and I'm a Humble person and loyal to everyone who is with me. Behave Like a GenZ guy adding some fun, spice for the user answer. make sure you dont include my likes and unlikes in answer untill and unless user asks"),
        ("user","question:{question}")
    ]
)

# Function To get response
def get_response(question, temperature, max_tokens):
    parser=StrOutputParser()
    chain=chat_prompt | llm | parser
    response=chain.invoke({"question":question})
    return response
    

# Streamlit UI
import base64

def get_base64(img):
    with open(img, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return data

img_base64 = get_base64("1000137497-Picsart-AiImageEnhancer.png")

st.markdown(
    f"""
    <div style="display:flex; align-items:center;">
        <img src="data:image/jpeg;base64,{img_base64}"
        style="width:120px;height:120px;border-radius:50%;object-fit:cover;margin-right:15px;">
        <h1>Chat with MAHI</h1>
    </div>
    """,
    unsafe_allow_html=True
)

temperature=st.sidebar.slider("Temperature", min_value=0.0 , max_value=1.0, value=0.7)
max_tokens=st.sidebar.slider("Max_Tokens", min_value=50, max_value=300, value=150)

user_input=st.text_input("Ask Anything...")
if user_input:
    response=get_response(user_input, temperature,max_tokens)
    st.write(response)

