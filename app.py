
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load local .env settings when running on your computer.
# Azure App Service settings are available as environment variables.
load_dotenv()

st.set_page_config(
    page_title="Malik Chatbot",
    page_icon="🤖",
    layout="centered",
)

# -----------------------------
# Azure AI Foundry configuration
# -----------------------------
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")


# -----------------------------
# Page styling
# -----------------------------
st.markdown(
    """
    <style>
    .block-container {
        max-width: 850px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.5rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #123b70, #1769aa);
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        color: white;
        margin-bottom: 0.4rem;
    }
    .hero p {
        color: #e6f1ff;
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🤖 Malik Chatbot</h1>
        <p>Your AI assistant for Python, technology, learning, and everyday questions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Check configuration
# -----------------------------
if not endpoint or not api_key or not deployment_name:
    st.error(
        "Azure AI settings are missing. Configure "
        "AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, "
        "and AZURE_OPENAI_DEPLOYMENT."
    )
    st.stop()

# Create the client without exposing the key.
client = OpenAI(
    base_url=endpoint,
    api_key=api_key,
)

# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm Malik Chatbot, powered by GPT-5 mini. "
                "How can I help you today?"
            ),
        }
    ]

with st.sidebar:
    st.title("Malik Chatbot")
    st.caption("Powered by Azure AI Foundry")
    st.markdown("---")
    st.markdown("**Model:** GPT-5 mini")
    st.markdown("**Features:**")
    st.markdown("- Ask questions")
    st.markdown("- Learn Python and AI")
    st.markdown("- Get help with coding")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I'm Malik Chatbot, powered by GPT-5 mini. "
                    "How can I help you today?"
                ),
            }
        ]
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Send a message to GPT-5 mini
# -----------------------------
prompt = st.chat_input("Message Malik Chatbot...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Keep the previous conversation for context.
    conversation = [
        {
            "role": "system",
            "content": (
                "You are Malik Chatbot, a helpful, friendly AI assistant. "
                "Give clear, accurate answers and explain technical topics "
                "in beginner-friendly steps when appropriate."
            ),
        }
    ]

    conversation.extend(
        st.session_state.messages[-21:]
    )

    with st.chat_message("assistant"):
        with st.spinner("Malik Chatbot is thinking..."):
            try:
                response = client.responses.create(
                    model=deployment_name,
                    input=conversation,
                )

                answer = response.output_text

                if not answer:
                    answer = "I couldn't generate a text response. Please try again."

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception:
                st.error(
                    "I couldn't connect to the AI model. "
                    "Please check your Azure endpoint, deployment name, "
                    "API key, and deployment availability."
                )
                st.exception(
                    "Request failed. Check the Azure App Service logs "
                    "for diagnostic details. Do not share API keys."
                )
