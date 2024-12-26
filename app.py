from fastapi import FastAPI, Query
from pyzerox import zerox
import json
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import misc
from typing import Optional, List
import prompts as prt
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = misc.get_apikey()
model = ChatOpenAI(model='gpt-4', temperature=0)
app = FastAPI()

async def process_file(file_path: str, model, output_dir, custom_system_prompt = None, select_pages = None, **kwargs):
    """
    Processes the given PDF file, converting it to markdown and saving the output.
    
    Args:
        file_path (str): Path to the PDF file.
        model: Model to use for processing.
        output_dir (str): Directory to save the consolidated markdown file.
        custom_system_prompt (str, optional): Custom prompt for zerox.
        select_pages (int or list of int, optional): Pages to process (1-indexed). None for all pages.
        **kwargs: Additional arguments for zerox function.
        
    Returns:
        result: The processed result from zerox.
    """
    # Call the zerox function with provided parameters
    if select_pages:
        maintain = False
    else:
        maintain = True
    print(select_pages)
    result = await zerox(
        file_path=file_path,
        model=model,
        output_dir=output_dir,
        maintain_format= maintain, 
        custom_system_prompt=custom_system_prompt,
        select_pages=select_pages,
        **kwargs
    )
    return result

# Create a FastAPI route for the process_file function
@app.get("/process-file")
async def process_file_endpoint(
    file_path: str = Query(..., description="Path to the PDF file"),
    select_pages : Optional[List[int]] = Query(None, description="List of page numbers to process")
):
    """
    FastAPI endpoint to process a PDF file and return markdown content.
    """
    result = await process_file(
        file_path=file_path,
        model=model,
        output_dir="files/input/income-rep/",
        custom_system_prompt=prt.pdf2json_omniai_prompt,
        select_pages=select_pages,
    )
    print(result)
    return {"result": result}

# I would like to define an endpoint here that returns whether the fields are expenses or earnings
@app.get("/retrieve_earnings_expenses_classification")
async def retrieve_earnings_expenses_classification():
    jsonparser = JsonOutputParser()
    index_year_stmnt_prompt = ChatPromptTemplate.from_messages([
        ("system", prt.index_year_stmnt_prompt)])
    income_stmt_path = 'files/input/income-rep/leighs_statement.json'
    with open(income_stmt_path, "r") as f:
        chain = index_year_stmnt_prompt | model | jsonparser
        statement= json.load(f)
        json_stmnt = chain.invoke({"financial_statement": statement})
        with open(f'files/input/income-rep/clean_leighs_statement.json',"w") as writefile:
            downcased_stmnt = misc.downcase_keys(json_stmnt)
            json.dump(downcased_stmnt, writefile, indent=4)
            classify_amount_type_prompt = ChatPromptTemplate.from_messages([
                ("system", prt.classify_amount_type_prompt)])
            chain = classify_amount_type_prompt | model | jsonparser
            type_fin_items = chain.invoke({"financial_statement": downcased_stmnt})
            with open(f'files/input/income-rep/type_leighs_statement.json',"w") as writefile:
                json.dump(type_fin_items, writefile, indent=4)
            return {"result": type_fin_items}

@app.get("/retrieve_fields_classification")
async def retrieve_fields_classification():
    provided_expense_items = []
    provided_earning_items = []
    provided_undefined_items = []
    known_expense_items = []
    known_earning_items = []
    with open(f'files/input/income-rep/type_leighs_statement.json',"r") as readfile:
        types_items = json.load(readfile)
        provided_expense_items = misc.filter_keys_by_category(types_items, 'expenses')
        provided_earnings_items = misc.filter_keys_by_category(types_items, 'earnings')
        income_fields = misc.retrieve_income_rep_fields()
        for item, desc in income_fields.items():
            if desc['fin_type'] == 'expense':
                known_expense_items.append((item, desc['description']))
            elif desc['fin_type'] == 'earning':
                known_earning_items.append((item, desc['description']))
        jsonparser = JsonOutputParser()
        index_year_stmnt_prompt = ChatPromptTemplate.from_messages([
            ("system", prt.classify_fields_unknown_to_known_prompt)])
        chain = index_year_stmnt_prompt | model | jsonparser
        expense_mapping_res = chain.invoke({"unknown_financial_terms": provided_expense_items,
                                            "known_financial_items": known_expense_items})
        earning_mapping_res = chain.invoke({"unknown_financial_terms": provided_earnings_items,
                                            "known_financial_items": known_earning_items})
        return {"result": {
            'expenses_mapping': expense_mapping_res,
            'earnings_mapping': earning_mapping_res}}
