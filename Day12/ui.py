import streamlit as st
from agent_app import ask

st.set_page_config(page_title="Academic Research Assistant 🤖")
st.title("📚 Academic Research Assistant")
st.markdown("Ask a question related to research papers:")

query = st.text_input("Enter your query:")

if st.button("Ask"):
    with st.spinner("Thinking..."):
        answer = ask(query)
        st.success("Here's what I found:")
        st.write(answer)
