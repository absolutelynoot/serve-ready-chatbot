import os
import streamlit as st
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

# 1. Load the document
loader = PyPDFDirectoryLoader("./docs")
pages = loader.load()

# 2. Split the document into chuncks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

splits = text_splitter.split_documents(pages)

# 3. Convert text chucks to embeddings
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
embedding = OpenAIEmbeddings(openai_api_key=key)

persist_directory = "./docs/vectordb"
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

def main():
    st.set_page_config(page_title="A Chatbot created to dive into the world of Migrant Workers!", page_icon=":robot_face:", layout="wide")
    st.header("A Chatbot created to dive into the world of Migrant Workers!" + " :robot_face:")
    st.subheader("Ask a question about migrant workers in Singapore and the chatbot will try to answer it!")
    user_question = st.text_area("Ask a burning question you have 🔥")

    if user_question:
        docs = vectordb.search(user_question, search_type="mmr")
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=user_question)

        st.write(response)

if __name__ == "__main__":
    main()
