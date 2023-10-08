import os, openai, sys
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

openai.api_key = "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"
#print(openai.api_key)

#Load the document
loader = PyPDFDirectoryLoader("./docs")
pages = loader.load()

#Split the document into chuncks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len
)

splits = text_splitter.split_documents(pages)


