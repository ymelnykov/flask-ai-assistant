import os
from flask import Flask, request, make_response, render_template
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models.openai import ChatOpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma


app = Flask(__name__)

# Set database directory
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ABS_PATH, 'db')
# Initialize vectorstore and retriever
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    "langchain_store", 
    embeddings,
    persist_directory=DB_DIR
    )
vectorstore.persist()
retriever = vectorstore.as_retriever(search_kwargs=dict(k=5))
# Set a vectorstore based memory
memory = VectorStoreRetrieverMemory(retriever=retriever)
# Initialize memory with a sample context
memory.save_context(
    {"input": "What is your name?"}, 
    {"output": "I am ChatGPT, a language model developed by OpenAI."}
)
# Set required LLM parameters
llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
# Build the prompt
_DEFAULT_TEMPLATE = """
The following is a friendly conversation between a human and an AI. 
If the AI does not know the answer to a question, 
it truthfully says it does not know.

Relevant pieces of previous conversation:
{history}

(You do not need to use these pieces of information if not relevant)

Current conversation:
Human: {input}
AI:"""
PROMPT = PromptTemplate(
    input_variables=["history", "input"], template=_DEFAULT_TEMPLATE
)
# Set conversation chain
conversation = ConversationChain(
    llm=llm,
    prompt=PROMPT,
    memory=memory,
    # verbose=True
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api')
def my_api():
    query = request.args.get('query')
    # process the input string here
    output_string = conversation.run(query)

    response = make_response(output_string, 200)
    response.mimetype = "text/plain"
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run()