from PIL import Image
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma


def main():
    st.set_page_config(page_title="A Chatbot created to dive into the world of Migrant Workers!", page_icon=":robot_face:", layout="centered")
    image = Image.open('HealthServe_Logo.png')
    col1, col2, col3 = st.columns([0.2, 5, 0.2])
    col2.image(image, use_column_width=True)
    st.header("A Chatbot created to dive into the world of Migrant Workers!" + " :robot_face:")
    st.subheader("Ask a question about migrant workers in Singapore and the chatbot will try to answer it!")
    user_question = st.text_area("Ask a burning question you have 🔥")

    vector_db_path="./docs/vectordb"
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=vector_db_path
    )

    if user_question:
        docs = vectordb.search(user_question, search_type="mmr", search_kwargs={"k": 10})
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=user_question)

        st.write(response)

if __name__ == "__main__":
    main()
