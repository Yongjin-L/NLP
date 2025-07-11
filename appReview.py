import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Selfstudy_reviewed_Papers",
    page_icon="💆",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- Application Title and Description ---
st.title("💆 RAG-Powered Chat Application")
st.markdown("""
Welcome to our AI supporter.<br>
Enter your question below to get a response from the model.<br>
우리 리뷰하는 51개 논문을 바탕으로 질문에 답변할 수 있도록 바꿔놨습니다.<br>
Try "How does Baker use a critical friend in the 2022 paper?"<br>
Use author names and publication year to improve the response quality.
""", unsafe_allow_html=True)

# --- API Configuration ---
# Use Streamlit secrets to manage sensitive data securely
try:
    API_URL = st.secrets["API_URL"]
    API_TOKEN = st.secrets["API_TOKEN"]
    MODEL_NAME = st.secrets.get(
        "REVIEW_MODEL_NAME", "selfstudyreviewedpaper")  # fallback value
except KeyError as e:
    st.error(f"Missing required secret: {e}")
    st.error("Please configure your secrets in Streamlit Cloud or create a .streamlit/secrets.toml file locally.")
    st.stop()


# --- Session State Initialization ---
# This ensures that the chat history is maintained across user interactions.
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
# Iterate through the existing messages in the session state and display them.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If the message is from the assistant and has sources, display them in an expander
        if message["role"] == "assistant" and "sources" in message and message["sources"]:
            with st.expander("View Sources"):
                for i, source in enumerate(message["sources"]):
                    source_title = source.get("source_title", f"Source {i+1}")
                    snippet = source.get("snippet", "No snippet available.")
                    st.info(f"**{source_title}**")
                    st.markdown(f"> {snippet}")


# --- User Input Handling ---
if prompt := st.chat_input("What do you want to know about these papers?"):
    # 1. Add user's message to session state and display it
    user_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_message)
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Prepare the request to the RAG API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json",
        }

        # We send the last user message to the API
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            # 3. Call the API
            response = requests.post(
                API_URL, headers=headers, data=json.dumps(payload), timeout=120)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            response_data = response.json()

            # 4. Parse and display the response
            # IMPORTANT: This assumes a specific response structure. You may need to adjust this
            # based on the actual JSON your API returns.
            # Assumed structure: {"choices": [{"message": {"content": "..."}, "sources": [...]}]}
            if "choices" in response_data and response_data["choices"]:
                assistant_content = response_data["choices"][0]["message"]["content"]

                # We are making an assumption that sources are part of the choice object.
                # If not, you might need to find where they are in `response_data`.
                sources = response_data["choices"][0].get("sources", [])

                message_placeholder.markdown(assistant_content)

                # Display sources if they exist
                if sources:
                    with st.expander("View Sources"):
                        for i, source in enumerate(sources):
                            source_title = source.get(
                                "source_title", f"Source {i+1}")
                            snippet = source.get(
                                "snippet", "No snippet available.")
                            st.info(f"**{source_title}**")
                            st.markdown(f"> {snippet}")

                # 5. Add assistant's message and sources to session state
                assistant_message = {
                    "role": "assistant",
                    "content": assistant_content,
                    "sources": sources
                }
                st.session_state.messages.append(assistant_message)

            else:
                message_placeholder.error(
                    "Received an unexpected response format from the API.")
                st.error(f"Full Response: `{response_data}`")

        except requests.exceptions.RequestException as e:
            message_placeholder.error(f"Failed to connect to the API: {e}")
        except Exception as e:
            message_placeholder.error(f"An unexpected error occurred: {e}")
