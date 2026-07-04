from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc


@mcp.tool(name="Read_tool" , description="This tool helps us read a document")
def read(filename:str = Field(description="This contains the name of the file")) :
    if(docs.get(filename) is None):
        raise ValueError("File doesnt exist")
    return docs[filename] 
# TODO: Write a tool to edit a doc

@mcp.tool(name="Write_tool" , description="This tool helps us write in a document")
def write(filename:str = Field(description="This contains the name of the file") , 
          old_str:str =Field(description="old string to be replaced"),
          new_str:str=Field(description="New string that needs to be put")):
    if(docs.get(filename) is None):
        raise ValueError("File doesnt exist")
    docs[filename]=new_str
    
# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
