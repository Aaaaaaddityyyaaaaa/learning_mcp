import asyncio
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph ,START,END
from dotenv import load_dotenv
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
import operator
from typing import List ,Annotated ,TypedDict
from langchain_core.messages import BaseMessage , HumanMessage
from langgraph.prebuilt.tool_node import ToolNode , tools_condition
import re

load_dotenv()
API_GROQ = os.getenv("GROQ_API_KEY")
llm  =ChatGroq(api_key=API_GROQ, model="openai/gpt-oss-120b", temperature=0.7 , timeout=12 , max_retries=2 )


class ChatState(TypedDict) : 
  messages : Annotated[List[BaseMessage ], operator.add]

client = MultiServerMCPClient(
  {
    "demo_mcp":{"transport":"stdio" , 
                "command":"python" , 
                "args":["D:/cliproj/chatbot_with_tools/mcpserver.py"]
    }
  }
)

async def build_graph() : 
  tools = await client.get_tools()
  resources = await client.get_resources()

  resource_map  = {}
  for r in resources:
        uri_str = str(r.metadata.get("uri", ""))
        name = uri_str.split("/")[-1]
        resource_map[name] = r.data if isinstance(r.data, str) else r.data.decode()

  llm_with_tools = llm.bind_tools(tools)


  async def chat_node(state:ChatState) :
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    return {"messages":[response]}

  tool_node = ToolNode(tools)
  
  
  graph = StateGraph(ChatState)
  graph.add_node("chat_node", chat_node)
  graph.add_node("tools", tool_node)
  graph.add_edge(START , "chat_node")
  graph.add_conditional_edges("chat_node",tools_condition)
  graph.add_edge("tools","chat_node")

  Chat_Bot = graph.compile()
  return Chat_Bot , resource_map

     

async def main() :
  chatbot ,resource_map = await build_graph()
  
  while(True) :

    message = input("Chat : ")
    mentions = check_at(message)
    for r in resource_map :
      if(r in mentions) :
        message = message.replace(f"@{r}",resource_map[r])
        

    result = await chatbot.ainvoke({"messages":[HumanMessage(content=message)]})
    print(result["messages"][-1].content)

def check_at(text) :
  pattern= r"@(\w+)"
  mentions = re.findall(pattern, text)
  return mentions



if __name__ == "__main__" :
  result = asyncio.run(main())
  print(result)
  