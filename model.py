import os
import chromadb
import shutil
import openai
import sys
import numpy as np
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain

def getResponse(question: str) -> str:

    # Load the API keys from the .env file
    load_dotenv('./.env')
    OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
    LANGCHAIN_API_KEY = os.getenv('LANGSMITH_API_KEY')
    db_directory = "./docs/vectordb"

    
    embedding = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)

    # Load an existing Chroma vector store
    vectordb = Chroma(persist_directory=db_directory, embedding_function=embedding)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key='question',
        output_key='answer'
    )

    # Enable tracing
    print("Enabling tracing...")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
    os.environ["LANGCHAIN_PROJECT"] = "Chatbot"

    # Define parameters for retrival
    retriever=vectordb.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5, "k": 5})

    # Define llm model
    llm_name = "gpt-3.5-turbo-16k"
    llm = ChatOpenAI(model_name=llm_name, temperature=0)

    # Define template prompt
    template = """You are a friendly chatbot that helps sad university students cope with their immense stress. 
    Use the following pieces of context to answer the question at the end.
    {context}
    Question: {question}
    Helpful Answer:"""

    your_prompt = PromptTemplate.from_template(template)

    # Execute chain
    qa = ConversationalRetrievalChain.from_llm(
        llm,
        combine_docs_chain_kwargs={"prompt": your_prompt},
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
        memory=memory
    )

    # Evaluate your chatbot with questions
    result = qa({"question": question})

    print(result)
    return result['answer']
