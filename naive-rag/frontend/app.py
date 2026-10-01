import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


st.title("Cognition AI Assistant")

st.write(
    "Ask questions about the Cognition AI employee handbook."
)


question = st.text_input(
    "Enter your question:"
)


if st.button("Ask Question"):

    if question.strip():

        response = requests.post(
            API_URL,
            json={
                "question": question
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.subheader("Answer")

            st.write(data["answer"])

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

    else:

        st.warning("Please enter a question.")