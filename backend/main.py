from fastapi import FastAPI
from backend.schemas import ConvertRequest
from backend.agents.currency_agent import llm_with_tools
from backend.tools.currency_tool import (
    get_currency_rate_tool,
    convert_currency_tool
)
import traceback

app = FastAPI(title="Currency Converter with LangChain Tools")

@app.post("/convert")
def convert_currency(payload: ConvertRequest):
    try:
        print("USER QUERY:", payload.query)

        response = llm_with_tools.invoke(payload.query)
        print("LLM RESPONSE:", response)

        if response.tool_calls:
            tool_call = response.tool_calls[0]
            print("TOOL CALL:", tool_call)

            tool_name = tool_call["name"]
            args = tool_call["args"]

            if tool_name == "get_currency_rate_tool":
                result = get_currency_rate_tool.invoke(args)

            elif tool_name == "convert_currency_tool":
                result = convert_currency_tool.invoke(args)

            else:
                result = "Unknown tool"

            return {"result": str(result)}

        return {"result": response.content or "No content returned"}

    except Exception as e:
        print(" ERROR OCCURRED")
        traceback.print_exc()
        return {"error": str(e)}
