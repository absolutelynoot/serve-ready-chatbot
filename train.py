import os
import chromadb
import shutil
import openai
import sys
import numpy as np
import boto3
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


# Function to upload a directory to S3
def upload_directory_to_s3(local_path, s3_bucket, s3_prefix='', s3=None):
    for root, _, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            s3_object = os.path.join(s3_prefix, os.path.relpath(local_file, local_path))
            s3.upload_file(local_file, s3_bucket, s3_object)

def main():

    # Load the API keys from the .env file
    load_dotenv('./.env')
    OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
    LANGCHAIN_API_KEY = os.getenv('LANGSMITH_API_KEY')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        
    # Load the document
    print("Loading documents...")
    loader = PyPDFDirectoryLoader("./docs")
    pages = loader.load()
    print(pages[0].page_content)

    # Split the document into chuncks
    print("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    splits = text_splitter.split_documents(pages)

    # Convert text chucks to embeddings
    print("Converting to embeddings...")

    embedding = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)

    # Delete vector db if it exists
    print("Storing into vector db...")

    db_directory = "./docs/vectordb"

    if os.path.exists(db_directory):
        shutil.rmtree(db_directory)

    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=db_directory
    )

    # Print the number of vectors stored
    print(f"Number of vectors stored: {vectordb._collection.count()}")

    # Create an S3 client+
    print("Initializing S3 client...")
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Path to the directory you want to upload
    local_directory = "./docs/vectordb"

    # Delete existing objects in the S3 bucket that start with 'vectordb/'
    objects = s3.list_objects_v2(Bucket=AWS_BUCKET_NAME)
    for obj in objects.get('Contents', []):
        if obj['Key'].startswith('vectordb/'):
            s3.delete_object(Bucket=AWS_BUCKET_NAME, Key=obj['Key'])

    # Upload the local directory to S3
    upload_directory_to_s3(local_directory, AWS_BUCKET_NAME, 'vectordb/', s3)

    print("Uploading vectordb to S3 completed!")

    # Train success
    print("Model Training success!")


if __name__ == "__main__":
    main()