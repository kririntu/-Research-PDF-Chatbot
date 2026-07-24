import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="PDF Reader Chatbot")

st.title("PDF Reader Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False


# -----------------------
# Upload PDFs
# -----------------------

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type="pdf",
    accept_multiple_files=True
)

if st.button("Upload PDFs"):

    if not uploaded_files:
        st.warning("Please select at least one PDF.")
    else:

        files = [
            (
                "files",
                (file.name, file.getvalue(), "application/pdf")
            )
            for file in uploaded_files
        ]

        with st.spinner("Processing PDFs..."):

            response = requests.post(
                f"{API_URL}/uploadfile/",
                files=files
            )

        if response.status_code == 200:
            st.success(response.json()["message"])
            st.session_state.uploaded = True

        else:
            try:
                st.error(response.json()["detail"])
            except:
                st.error(response.text)


st.divider()


# -----------------------
# Display Chat
# -----------------------

for msg in st.session_state.messages:

    with st.chat_message("user"):
        st.write(msg["user"])

    with st.chat_message("assistant"):
        st.write(msg["bot"])


# -----------------------
# Chat Input
# -----------------------

question = st.chat_input(
    "Ask a question about the uploaded PDFs",
    disabled=not st.session_state.uploaded
)

if question:

    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Thinking..."):

        response = requests.post(
            f"{API_URL}/chat",
            json={"question": question}
        )

    if response.status_code == 200:

        answer = response.json()["answer"]

    else:

        try:
            answer = response.json()["detail"]
        except:
            answer = response.text

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {
            "user": question,
            "bot": answer
        }
    )

    st.rerun()
