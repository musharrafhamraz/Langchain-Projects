from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

# Step 1: Initialize the LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192"
)

# Step 2: Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["transcript"],
    template="""
You are an emotionally intelligent assistant helping therapy patients reflect on their sessions.

Given the following therapy session transcript, generate a concise, emotionally attuned reflection. Your goal is to:
- Identify the emotional tone
- Highlight key insights or breakthroughs
- Suggest one thoughtful question or reflection the client can consider between sessions

Transcript:
{transcript}

== OUTPUT ==
Summary:
"""
)

# Step 3: Create the LLMChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Step 4: Function to generate summary
def generate_summary(transcript: str) -> str:
    result = chain.invoke({"transcript": transcript})
    return result["text"].strip()
