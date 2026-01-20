import os
from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from backend.tools.currency_tool import (
    get_currency_rate_tool,
    convert_currency_tool
)

# Step 1: Create base LLM WITH API KEY
base_llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=0,
    timeout=120,
)

#  Step 2: Wrap as chat model (Qwen IS a chat model)
llm = ChatHuggingFace(llm=base_llm)

#  Step 3: Bind tools
llm_with_tools = llm.bind_tools(
    [
        get_currency_rate_tool,
        convert_currency_tool
    ]
)
