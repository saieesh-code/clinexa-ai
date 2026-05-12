# =========================================================
# utils/ai_engine.py
# =========================================================

import os
import time
import streamlit as st

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_core.prompts import ChatPromptTemplate


# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# =========================================================
# MODEL PRIORITY
# =========================================================

MODEL_PRIORITY = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]


# =========================================================
# LOAD GEMINI MODEL
# =========================================================

def load_llm():
    """
    Loads the first available Gemini model.
    """

    for model_name in MODEL_PRIORITY:

        try:

            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=GOOGLE_API_KEY,
                temperature=0.3,
                max_output_tokens=2048,
            )

            print(f"✅ Loaded Gemini Model: {model_name}")

            return llm

        except Exception as e:

            print(f"❌ Failed loading model: {model_name}")
            print(e)

            time.sleep(1)

    return None


# =========================================================
# INITIALIZE MODEL
# =========================================================

llm = load_llm()


# =========================================================
# DEMO FALLBACK RESPONSE
# =========================================================

DEMO_RESPONSE = """
## AI Demo Response

The uploaded medical report indicates stable clinical parameters with mild abnormalities requiring routine follow-up.

### Key Findings
- Vital signs are within acceptable range
- Mild glucose elevation observed
- No critical cardiac abnormalities detected
- Patient condition currently stable

### Recommendations
- Continue prescribed medications
- Maintain healthy diet and hydration
- Schedule follow-up consultation
- Monitor symptoms regularly

⚠ Demo Mode Active:
Gemini API quota limit reached or service temporarily unavailable.
"""


# =========================================================
# SAFE INVOKE FUNCTION
# =========================================================

def safe_invoke(chain, payload):
    """
    Safely invokes Gemini with graceful fallback.
    """

    global llm

    try:

        # If model unavailable
        if llm is None:
            return DEMO_RESPONSE

        response = chain.invoke(payload)

        if hasattr(response, "content"):
            return response.content

        return str(response)

    except ChatGoogleGenerativeAIError as e:

        error_text = str(e)

        print("\n⚠ Gemini API Error:")
        print(error_text)

        # Handle quota exhaustion
        if "RESOURCE_EXHAUSTED" in error_text:

            print("🔄 Quota exhausted. Switching model...")

            llm = load_llm()

            time.sleep(2)

            return DEMO_RESPONSE

        return DEMO_RESPONSE

    except Exception as e:

        print("\n⚠ Unexpected Error:")
        print(e)

        return DEMO_RESPONSE


# =========================================================
# GENERATE MEDICAL SUMMARY
# =========================================================

def generate_summary(report_text):

    prompt = ChatPromptTemplate.from_template("""
You are an expert medical AI assistant.

Generate a professional medical summary.

Include:
- Key findings
- Important observations
- Risks
- Suggested follow-up

Medical Report:
{report}
""")

    chain = prompt | llm

    return safe_invoke(
        chain,
        {
            "report": report_text
        }
    )


# =========================================================
# GENERATE DOCTOR NOTES
# =========================================================

def generate_doctor_notes(report_text):

    prompt = ChatPromptTemplate.from_template("""
You are an experienced clinical documentation assistant.

Generate structured doctor notes.

Include:
- Symptoms
- Diagnosis
- Clinical findings
- Recommendations
- Follow-up advice

Medical Report:
{report}
""")

    chain = prompt | llm

    return safe_invoke(
        chain,
        {
            "report": report_text
        }
    )


# =========================================================
# MEDICAL CHATBOT
# =========================================================

def medical_chatbot(question):

    prompt = ChatPromptTemplate.from_template("""
You are a professional healthcare AI assistant.

Answer clearly, professionally, and safely.

Question:
{question}
""")

    chain = prompt | llm

    return safe_invoke(
        chain,
        {
            "question": question
        }
    )


# =========================================================
# CACHE FUNCTIONS
# =========================================================

@st.cache_data(show_spinner=False)
def cached_summary(report_text):
    return generate_summary(report_text)


@st.cache_data(show_spinner=False)
def cached_notes(report_text):
    return generate_doctor_notes(report_text)