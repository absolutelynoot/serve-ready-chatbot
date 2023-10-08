import os, openai, sys
import numpy as np
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import panel as pn
import param

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

openai.api_key = "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"

### Needed to only run once
# # 1. Load the document
# loader = PyPDFDirectoryLoader("./docs")
# pages = loader.load()

# # 2. Split the document into chuncks
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=150,
#     length_function=len
# )

# splits = text_splitter.split_documents(pages)

# # 3. Convert text chucks to embeddings
# embedding = OpenAIEmbeddings(openai_api_key = openai.api_key)

# persist_directory = "./docs/vectordb"
# vectordb = Chroma.from_documents(
#     documents=splits,
#     embedding=embedding,
#     persist_directory=persist_directory
# )

os.environ["OPENAI_API_KEY"] = "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"

persist_directory = "./docs/vectordb"
embedding = OpenAIEmbeddings(openai_api_key = openai.api_key)
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
os.environ["LANGCHAIN_PROJECT"] = "Chatbot"

dotenv_path = os.path.join("./docs/vectordb", '.env')
load_dotenv(dotenv_path)

LANGCHAIN_API_KEY='ls__92b0ffaa97be479d968b5f6f7f9c1d4d' 


# This is the only code cell which you will need for your experimentation
def load_qa():
   # Define parameters for retrival
  llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
  #retriever=vectordb.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5, "k": 5})
  retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 10})

  # Define template prompt
  template = """You are a friendly chatbot helping a migrant worker settle down in Singapore. Use the following pieces of context to answer the question at the end.
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
    return_generated_question=True
    #memory=memory
  )
  return qa

# Defines a class named cbfs with methods to handle various functions of a chatbot
class cbfs(param.Parameterized):
    chat_history = param.List([])
    answer = param.String("")
    db_query  = param.String("")
    db_response = param.List([])

# Initializers the cbfs instance and calls load_qa to return a chain
    def __init__(self,  **params):
        super(cbfs, self).__init__( **params)
        self.panels = []
        self.qa = load_qa()

# Method to handle conversation flow by taking in a query (or question),
# processes it using the qa function, updates chat history, and generates appropriate responses.
    def convchain(self, query):
        if not query:
            return pn.WidgetBox(pn.Row('User:', pn.pane.Markdown("", width=600)), scroll=True)
        result = self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        self.db_query = result["generated_question"]
        self.db_response = result["source_documents"]
        self.answer = result['answer']
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query, width=600)),
            pn.Row('ChatBot:', pn.pane.Markdown(self.answer, width=600, styles={'background-color': '#F6F6F6'}))
        ])
        inp.value = ''  #clears loading indicator when cleared
        return pn.WidgetBox(*self.panels,scroll=True)

    @param.depends('db_query ', )
    def get_lquest(self):
        if not self.db_query :
            return pn.Column(
                pn.Row(pn.pane.Markdown(f"Last question to DB:", styles={'background-color': '#F6F6F6'})),
                pn.Row(pn.pane.Str("no DB accesses so far"))
            )
        return pn.Column(
            pn.Row(pn.pane.Markdown(f"DB query:", styles={'background-color': '#F6F6F6'})),
            pn.pane.Str(self.db_query )
        )

    @param.depends('db_response', )
    def get_sources(self):
        if not self.db_response:
            return
        rlist=[pn.Row(pn.pane.Markdown(f"Result of DB lookup:", styles={'background-color': '#F6F6F6'}))]
        for doc in self.db_response:
            rlist.append(pn.Row(pn.pane.Str(doc)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    @param.depends('convchain', 'clr_history')
    def get_chats(self):
        if not self.chat_history:
            return pn.WidgetBox(pn.Row(pn.pane.Str("No History Yet")), width=600, scroll=True)
        rlist=[pn.Row(pn.pane.Markdown(f"Current Chat History variable", styles={'background-color': '#F6F6F6'}))]
        for exchange in self.chat_history:
            rlist.append(pn.Row(pn.pane.Str(exchange)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    def clr_history(self,count=0):
        self.chat_history = []
        return

pn.extension()
cb = cbfs()


button_clearhistory = pn.widgets.Button(name="Clear History and Memory", button_type='warning')
button_clearhistory.on_click(cb.clr_history)
inp = pn.widgets.TextInput( placeholder='Enter text here…')

conversation = pn.bind(cb.convchain, inp)

tab1 = pn.Column(
    pn.Row(inp),
    pn.layout.Divider(),
    pn.panel(conversation,  loading_indicator=True, height=300),
    pn.layout.Divider(),
)
tab2= pn.Column(
    pn.panel(cb.get_lquest),
    pn.layout.Divider(),
    pn.panel(cb.get_sources ),
)
tab3= pn.Column(
    pn.panel(cb.get_chats),
    pn.layout.Divider(),
    pn.Row(button_clearhistory, pn.pane.Markdown("Clears chat history and memory in the chain. Can use to start a new topic" )),
)

dashboard = pn.Column(
    pn.Row(pn.pane.Markdown('# Experiment with your Chatbot')),
    pn.Tabs(('Conversation', tab1), ('Source Documents', tab2), ('Chat History', tab3))
)
dashboard

# # Acknowledgement for panel based chatbot: Sophia Yang (https://github.com/sophiamyang/tutorials-LangChain)