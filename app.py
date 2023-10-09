import os, openai, sys
import numpy as np
import streamlit as st
from flask import Flask, render_template, request
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from PyPDF2 import PdfReader

## Needed to only run once
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

# Facebook AI Similarity Search (FAISS) is a library for efficient similarity search and clustering of dense vectors.
persist_directory = "./docs/vectordb"
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

# os.environ["OPENAI_API_KEY"] = "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" # need to replace already got disabled

# persist_directory = "./docs/vectordb"
# embedding = OpenAIEmbeddings(openai_api_key = openai.api_key)
# vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
# os.environ["LANGCHAIN_PROJECT"] = "Chatbot"

# dotenv_path = os.path.join("./docs/vectordb", '.env')
# load_dotenv(dotenv_path)

# LANGCHAIN_API_KEY='ls__92b0ffaa97be479d968b5f6f7f9c1d4d' # need to replace already got disabled

def main():
    st.set_page_config(page_title="A Chatbot created to dive into the world of Migrant Workers!", page_icon=":robot_face:", layout="wide")
    st.header("A Chatbot created to dive into the world of Migrant Workers!")

    pdf = st.file_uploader("Upload a PDF file", type="pdf")

    user_question = st.text_input("Ask a burning question you have !")

    if user_question:
        docs = vectordb.search(user_question, search_type="mmr")
        st.write(docs)

if __name__ == "__main__":
    main()
