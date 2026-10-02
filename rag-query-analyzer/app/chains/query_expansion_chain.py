from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from models.query_expansion import QueryExpansion
from prompts.query_expansion_prompt import QUERY_EXPANSION_PROMPT


# 1. Connect to Ollama
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


# 2. Create the prompt
prompt = ChatPromptTemplate.from_template(
    QUERY_EXPANSION_PROMPT
)


# 3. Tell the LLM to return QueryExpansion
structured_llm = llm.with_structured_output(QueryExpansion)


# 4. Connect prompt → LLM
query_expansion_chain = prompt | structured_llm