from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputKeyOutputParser,
    StructuredOutputParser
)
from pydantic import BaseModel, Field

# 1. StrOutputParser 
str_parser = StrOutputParser()
output_str = str_parser.invoke("This is a simple string.")
print("🔹 StrOutputParser Output:\n", output_str)

#2. JsonOutputKeyOutputParser 
json_parser = JsonOutputKeyOutputParser(key_name="answer")
json_input = '{"answer": "The capital of India is New Delhi."}'
output_json = json_parser.invoke(json_input)
print("\n🔹 JsonOutputKeyOutputParser Output:\n", output_json)

#3. StructuredOutputParser 
class CapitalInfo(BaseModel):
    country: str = Field(description="Name of the country")
    capital: str = Field(description="Capital of the country")

structured_parser = StructuredOutputParser(pydantic_schema=CapitalInfo)
structured_input = '{"country": "India", "capital": "New Delhi"}'
output_structured = structured_parser.invoke(structured_input)
print("\n🔹 StructuredOutputParser Output:\n", output_structured)
