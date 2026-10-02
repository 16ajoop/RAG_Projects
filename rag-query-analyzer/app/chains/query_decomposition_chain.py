from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from models.query_decomposition import QueryDecomposition
from prompts.query_decomposition_prompt import QUERY_DECOMPOSITION_PROMPT


# 1. Connect to Ollama
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


# 2. Create the prompt
prompt = ChatPromptTemplate.from_template(
    QUERY_DECOMPOSITION_PROMPT
)


# 3. Tell the LLM to return QueryDecomposition
structured_llm = llm.with_structured_output(QueryDecomposition)


# 4. Connect prompt → LLM
query_decomposition_chain = prompt | structured_llm