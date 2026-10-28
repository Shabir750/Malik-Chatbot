
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ==========================================
# Load environment variables
# ==========================================
# Locally, settings come from your .env file.
# On Azure, settings come from App Service
# environment variables.
load_dotenv()

# ==========================================
# Streamlit page configuration
# ==========================================
st.set_page_config(
    page_title="Malik Chatbot",
    page_icon="🤖",
    layout="centered",
)

# ==========================================
# Azure AI Foundry configuration
# ==========================================
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# ==========================================
# Page styling
# ==========================================
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

# ==========================================
# Chatbot header
# ==========================================
st.markdown(
    """
    <div class="hero">
        <h1>🤖 Malik Chatbot</h1>
        <p>
            Your AI assistant for Python, technology,
            learning, coding, and everyday questions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# Check Azure configuration
# ==========================================
if not endpoint or not api_key or not deployment_name:
    st.error(
        "Azure AI settings are missing. Please configure "
        "AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, "
        "and AZURE_OPENAI_DEPLOYMENT."
    )
    st.stop()

# ==========================================
# Initialize Azure AI Foundry client
# ==========================================
client = OpenAI(
    base_url=endpoint,
    api_key=api_key,
)

# ==========================================
# Initial chat message
# ==========================================
WELCOME_MESSAGE = (
    "Hello! I'm Malik Chatbot, powered by GPT-5 mini. "
    "How can I help you today?"
)

# ==========================================
# Initialize chat history
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE,
        }
    ]

# ==========================================
# Sidebar
# ==========================================
with st.sidebar:
    st.title("🤖 Malik Chatbot")
    st.caption("Powered by Azure AI Foundry")

    st.markdown("---")

    st.markdown("**AI Model**")
    st.write("GPT-5 mini")

    st.markdown("**Features**")
    st.markdown(
        """
        - Ask questions
        - Learn Python and AI
        - Get coding assistance
        - Explore technology
        - Continue conversations
        """
    )

    st.markdown("---")

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True,
    ):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE,
            }
        ]
        st.rerun()

# ==========================================
# Display existing chat history
# ==========================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# Chat input
# ==========================================
prompt = st.chat_input("Message Malik Chatbot...")

if prompt:
    # Save the user's message.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Display the user's message.
    with st.chat_message("user"):
        st.markdown(prompt)

    # ======================================
    # System instructions
    # ======================================
    # These instructions define the chatbot's
    # identity and response style.
    conversation = [
        {
            "role": "system",
            "content": (
                "You are Malik Chatbot, a helpful, friendly AI assistant "
                "developed by Muhammad Shabir. "

                "If anyone asks who developed you, who created you, "
                "who built you, who made you, or who your developer is, "
                "clearly answer: 'I was developed by Muhammad Shabir.' "

                "You may explain that Muhammad Shabir developed this "
                "chatbot application using Azure AI Foundry and GPT-5 mini. "

                "Do not claim that Muhammad Shabir created or trained "
                "the underlying GPT-5 mini model. Distinguish between "
                "the developer of this chatbot application and the "
                "creators of the underlying AI model. "

                "Give clear, accurate answers. Explain technical topics "
                "in beginner-friendly steps when appropriate. "
                "Be polite, professional, and helpful. "
                "If you do not know an answer, say so rather than "
                "inventing information."
            ),
        }
    ]

    # Include recent messages to preserve context.
    # The system instructions are added separately above.
    conversation.extend(
        st.session_state.messages[-21:]
    )

    # ======================================
    # Generate the assistant's response
    # ======================================
    with st.chat_message("assistant"):
        with st.spinner("Malik Chatbot is thinking..."):
            try:
                response = client.responses.create(
                    model=deployment_name,
                    input=conversation,
                )

                answer = response.output_text

                if not answer:
                    answer = (
                        "I couldn't generate a text response. "
                        "Please try again."
                    )

                # Display the answer.
                st.markdown(answer)

                # Save the answer to chat history.
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception:
                st.error(
                    "I couldn't connect to the AI model. "
                    "Please check your Azure endpoint, deployment name, "
                    "API key, and deployment availability."
                )

                st.info(
                    "For troubleshooting, check your Azure App Service "
                    "logs. Never share your API key publicly."
                )
