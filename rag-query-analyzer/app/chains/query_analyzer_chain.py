from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from models.query_analysis import QueryAnalysis
from prompts.query_analyzer_prompt import QUERY_ANALYZER_PROMPT


# 1. Connect to Ollama
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


# 2. Create the prompt
prompt = ChatPromptTemplate.from_template(
    QUERY_ANALYZER_PROMPT
)


# 3. Tell the LLM to return QueryAnalysis
structured_llm = llm.with_structured_output(QueryAnalysis)


# 4. Connect everything together
query_analyzer_chain = prompt | structured_llm