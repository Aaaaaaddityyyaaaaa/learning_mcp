from mcp.server.fastmcp import FastMCP
from pydantic import Field
from langchain_community.tools import DuckDuckGoSearchRun
import httpx
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("OPEN_METEOR_API_KEY")

server = FastMCP(name="demo_mcp")

@server.tool(name="Web_search_tool" , 
             description="This tool will be used when my llm has to do a websearch")
async def web_search_tool(search_input:str=Field(description="This is the search string that will be searched on the internet")):
  search = DuckDuckGoSearchRun()
  result = await search.ainvoke(search_input)
  return result

@server.tool(name="Weather_tool" ,description="The tool will be used if the user queries about weather")
async def weather_tool(input_city:str=Field(description="This is the name of the cty we want to know the temprature off.")):
  url = "https://api.openweathermap.org/data/2.5/weather"
  params={"q":input_city ,
           "appid": API_KEY ,  
           "units" :"metric" }
  try :
    async with httpx.AsyncClient() as client:
      response = await client.get(url , params=params)
  except Exception as e: 
    return e
  if response.status_code == 200:
    data = response.json()
    try:
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The temperature in {input_city} is {temp}°C with {description}."
    except (KeyError, IndexError) as e:
        return f"Unexpected response format: {e} | raw={data}"
  else:
    return "City not found or invalid API key."
  
@server.resource(uri="resource://Info_Aditya",
                 name="Info_Aditya",
                 description="This resource is used only when we need certain information about aditya"
                 )
def Facts_About_Aditya() :
   data = json.dumps({"full name":"Aditya Pandey" , 
           "height" : "5feet 6in" , 
           "weight"  : "180 kg",  
           "schooling":"MDS",
           "adress":"Dehradun" , 
           "University":"DoonUniversity"} )
   return data
   

if __name__ == "__main__":
    server.run()
