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

def getResponse(question: str, chat_history) -> str:

    embedding = OpenAIEmbeddings()

    # Load the API keys from the .env file
    print("Reading configuration")
    load_dotenv('./.env')
    db_directory = "./docs/vectordb"
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY") or os.environ.get("LANGCHAIN_API_KEY")

    # Enable tracing
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
    os.environ["LANGCHAIN_PROJECT"] = "Serve Ready Chatbot"

    # Load an existing Chroma vector store
    vectordb = Chroma(persist_directory=db_directory, embedding_function=embedding)
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key='question', 
        output_key='answer'
    )

    # Define template prompt
    template = """You are a friendly chatbot that helps HealthServe employees for onboarding process and handle day-to-day work serving migrant workers in Singapore. Use the following pieces of context to answer the question at the end. Your response should be in english by default but if mentioned in the user query/question, please reply in their desired language. If the question cannot be answered using the information provided, please respond with "I'm not sure how to answer that, please seek your manager/supervisor or official HealthServe documentation." 

    Context:
    HealthServe is a non-profit organization based in Singapore dedicated to serving the needs of migrant workers in the country. The organization is committed to providing essential healthcare, social, and legal support to these workers, many of whom come from various countries seeking employment opportunities in Singapore. HealthServe aims to ensure the well-being and rights of these migrant workers are protected, and they receive the necessary support to lead dignified lives during their time in Singapore.

    The onboarding process for new employees at HealthServe is a crucial aspect of ensuring that they understand the organization's mission, values, and the specific responsibilities related to serving migrant workers. This process includes training on relevant healthcare procedures, legal requirements, and best practices for working with this specific population. New employees are expected to gain a thorough understanding of HealthServe's services, the challenges faced by migrant workers, and the importance of providing empathetic and quality care.

    Day-to-day work at HealthServe includes activities such as medical check-ups, legal consultations, social support services, and general assistance to migrant workers who seek help from the organization. Employees are expected to maintain a high level of professionalism, cultural sensitivity, and empathy while interacting with clients. It is essential to keep up-to-date with the latest guidelines, procedures, and policies related to providing support to migrant workers.

    Question: {question}

    Helpful Answer:"""

    your_prompt = PromptTemplate.from_template(template)

    # Define llm model
    llm_name = "gpt-3.5-turbo-16k"
    llm = ChatOpenAI(model_name=llm_name, temperature=0)

    # Define parameters for retrival
    retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 10})

    # Execute chain
    qa = ConversationalRetrievalChain.from_llm(
        llm,
        combine_docs_chain_kwargs={"prompt": your_prompt},
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
        # memory=memory,
    )
    
    # Evaluate your chatbot with questions
    result = qa({"question": question, "chat_history": chat_history})

    print(result)

    return { 
        "answer": result['answer'],
        "source_documents": result['source_documents'],
    }
