# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: finapp-kernel
#     language: python
#     name: finapp-kernel
# ---

# + jupyter={"outputs_hidden": false}
# %load_ext autoreload
# %autoreload 2
import json
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import pdb
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
os.environ["OPENAI_API_KEY"] = ##API KEY
model = ChatOpenAI(model='gpt-4',
                  temperature=0)

# + jupyter={"outputs_hidden": false}
import income_rep_model as im
# create a dict with the field and it's description
st_income_fields = {}
fields = im.COGS.__fields__ | im.OperatingExpenses.__fields__ | im.IncomeStatement.__fields__
for field_name, field_info in fields.items():
    field_metadata = field_info.field_info
    description = field_metadata.description if field_metadata.description else 'No description'
    fin_type = field_metadata.extra.get('fin_type', 'Not specified')  # Access `fin_type` from the `extra` dictionary
    st_income_fields[field_name] = {'description': description, 'fin_type': fin_type}


# + jupyter={"outputs_hidden": false}
def downcase_keys(obj):
    if isinstance(obj, dict):
        # Recurse into each key-value pair and convert keys to lowercase
        return {k.lower(): downcase_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # If the object is a list, recurse into each item
        return [downcase_keys(item) for item in obj]
    else:
        # For other data types, return the object as-is
        return obj


# + jupyter={"outputs_hidden": false}
# convert to a known json structure indexed by the year
prompt = ChatPromptTemplate.from_messages([(
    "system", """
    Transform the the financial statement between triple backticks in JSON format. If the financial statement input is not a JSON, respond with: "Please provide a JSON input!"

    ```{financial_statement}``


1. Consider only the "Body" key of the input json and create a list of jsons where the year is the key.
2. For each year key, the output should be a json object with the name financial item name as key, and the correspondent number amount as value. The values should always be a number with it's respective sign. Try to deduce if the value if positive or negative and assign the correct sign.
3. If it's not possible to assign a number assign the json null value. 
4. Return nothing but a json containing a list of jsons with every year present in the body as a key. Ensure that all the years within the body section are present and contain the JSON value as described in steps 1 and 2.
    """
                  )])
jsonparser = JsonOutputParser()
json_res = ""
income_stmt_path = 'files/input/income-rep/leighs_statement.json'
with open(income_stmt_path, "r") as f:
    chain = prompt | model | jsonparser
    statement= json.load(f)
    json_res = chain.invoke({"financial_statement": statement})
    with open(f'files/input/income-rep/clean_leighs_statement.json',"w") as writefile:
        downcased_res = downcase_keys(json_res)
        json.dump(downcased_res, writefile, indent=4)

# + jupyter={"outputs_hidden": false}
# convert to a known json structure indexed by the year
prompt = ChatPromptTemplate.from_messages([(
    "system", """
    Transform the the financial statement between triple backticks in JSON format. If the financial statement input is not a JSON, respond with: "Please provide a JSON input!"

    ```{financial_statement}``


1. For each different item classify if it is earnings or expense, using firstly the meaning, the sign if available, and the items before and after.
2. Return should be ONLY a list of JSON objects. Each object should contain a single pair consisting of the  item's name, and either "earnings" or  "expenses". 
3. Try to classify all of the financial items! If it is absolutely not possible to classify the key assign the json "null" value.
             """
                  )])
jsonparser = JsonOutputParser()
json_res = ""
with open('files/input/income-rep/clean_leighs_statement.json',"r") as readfile:
    chain = chain = prompt | model | jsonparser
    statement= json.load(readfile)
    json_res = chain.invoke({"financial_statement": statement})
    with open(f'files/input/income-rep/type_leighs_statement.json',"w") as writefile:
        json.dump(json_res, writefile, indent=4)

# + jupyter={"outputs_hidden": false}
# filter all the earnings from all the expenses from the income statement
expense_items = []
earning_items = []
undefined_items = []
def filter_keys_by_category(data, category):
    """
    Filters the keys in the given JSON data based on the specified category.

    Parameters:
        data (list of dict): The JSON data to filter.
        category (str or None): The category to filter by ("expenses", "earnings", or None).

    Returns:
        list: A list of keys matching the specified category, or all keys with null values if category is None.
    """
    if category is None:
        return [key for item in data for key, value in item.items() if value is None]
    
    return [key for item in data for key, value in item.items() if value == category]
with open(f'files/input/income-rep/type_leighs_statement.json',"r") as readfile:
    types_items = json.load(readfile)
    expense_items = filter_keys_by_category(type_items, 'expenses')
    earnings_items = filter_keys_by_category(type_items, 'earnings')
    undefined_items = filter_keys_by_category(type_items, None)

with open(f'files/input/income-rep/type_leighs_statement.json',"r") as readfile:
    types_items = json.load(readfile)


# + jupyter={"outputs_hidden": false}
prompt = ChatPromptTemplate.from_messages([(
    "system", """Classify each item in a JSON financial statement to match known \
    income statement fields.
                 If the financial statement input is not a JSON, respond with: \
    "Please provide a JSON input!"
                 Consider the (key, description value) pairs of the known income \
    statement fields between the triple backticks below :
                 
                 Known income statement keys and descriptions: ```{st_income_fields}```

                 These are the steps you need to follow:
                 
                 1. The output If the financial statement input is not a JSON, respond with: \
    "Please provide a JSON input!"
                 Consider the (key, description value) pairs of the known income \
    statement fields between the triple backticks below :should be a JSON in PLAIN TEXT, containing the same \
    keys existing in the input JSON.
                                  
                 2. The value for each key should be a JSON object containing the \
    original currency amount "amount", "type", and fields "1match", "1match-type" "2match", "3match".
                 
                 3. Classify for every item in the JSON financial statement input \
    if it is earnings or expense, assign it to "type", using the item's name, the items \
    before and after, and the item's amount sign
                 
                 4. Use the description values, and the type to determine what is the best \
    matching known income statement field. Classify the known income statement key's description \
    as earnings or expense. The type of the item in the JSON financial statement input and the type
    in the known income income statment should be the same.
                 
                 5. Use the description values, and type to determine what is the \
    second best matching known income statement field.  The known field's initial \
    description type should completely match the classified input's type. Set null, \
    if there is no adequate match.
                 6. Use the description values, and type to determine what is the \
    third best matching known income statement field.  The known field's initial \
    description type should completely match the classified input's type. Set null, \
    if there is no adequate match.
             """
                  ),(
        "user", "{input}")])
jsonparser = JsonOutputParser()
# Opening JSON file
res = {}
with open('files/input/income-rep/leighs_statement.json',"r") as readfile:
    chain = chain = prompt | model | jsonparser
    leighs_statements= json.load(readfile)
    for statement in leighs_statements['leighs income statements']:
        print(statement)
        [(year, stmnt),] = statement.items()
        json_res = chain.invoke({"input": stmnt, "st_income_fields": st_income_fields})
        res[year] = json_res
print(res)        
#    with open(f'app/valuation/clf-leighs-income-statement.json',"w") as writefile:


# + jupyter={"outputs_hidden": false}
from pydantic import BaseModel, Field

class ExampleModel(BaseModel):
    interest_expenses: float = Field(0.0, description="Interest expenses")
    tax_expenses: float = Field(..., description="Tax expenses")
    extraordinary_expenses: float = Field(0.0, description="Non-recurring extraordinary items")

# Retrieve field names and descriptions
fields = ExampleModel.__fields__
print(type(fields))
for field_name, field_info in fields.items():
    description = field_info.field_info.description if field_info.field_info.description else 'No description'
    print(f"Field Name: {field_name}, Description: {description}")
