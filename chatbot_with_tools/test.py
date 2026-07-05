from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio


client = MultiServerMCPClient(
  {"demo_mcp" : 
    {
      "transport":"stdio",
      "command" :"python",
      "args": ["D:/cliproj/chatbot_with_tools/mcpserver.py"]
    }
  }
  
)

async def get_resources():
  resorces = await client.get_resources()
  for r in resorces : 
    uri_str = str(r.metadata.get("uri", ""))
    resource_name = uri_str.split("/")[-1]
    print(resource_name)
if __name__ =="__main__" :
  asyncio.run(get_resources())