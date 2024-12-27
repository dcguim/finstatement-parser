from fastapi import FastAPI, Query, File, UploadFile, HTTPException
from pyzerox import zerox
from botocore.exceptions import NoCredentialsError, ClientError
import json
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import misc
import statics as st
from typing import Optional, List
import prompts as prt
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = misc.get_apikey()
model = ChatOpenAI(model='gpt-4', temperature=0)
app = FastAPI()

from fastapi import FastAPI

app = FastAPI()

# Configure AWS S3

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file to S3.
    :param file: The uploaded file from the client
    """
    session = misc.load_aws_credentials(st.PROFILE)
    s3_client = session.client("s3")
    print(session.profile_name)  # Should print 'ddtechu'
    try:
        # Read file content
        file_content = await file.read()
        # Upload the file to S3
        s3_client.put_object(
            Bucket=st.S3_BUCKET_NAME,
            Key=file.filename,
            Body=file_content,
            ContentType=file.content_type  # Set the correct content type (e.g., application/pdf)
        )

        return {
            "message": f"File '{file.filename}' uploaded successfully to bucket '{st.S3_BUCKET_NAME}'",
            "file_url": f"https://{st.S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}",
        }
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-s3-buckets")
async def list_s3_buckets():
    """
    Endpoint to list S3 buckets for a given AWS profile.
    """
    try:
        # Load AWS credentials for the profile
        session = misc.load_aws_credentials(st.PROFILE)

        # Create S3 client using the loaded credentials
        s3_client = session.client('s3')

        # List buckets
        # List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=st.S3_BUCKET_NAME)

        # Extract object keys (blob names)
        if 'Contents' in response:
            blobs = [obj['Key'] for obj in response['Contents']]
        else:
            blobs = []
        return {"blobs": blobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        type_of_statement: str,
        file_path: str = Query(..., description="Path to the PDF file"),
        select_pages : Optional[List[int]] = Query(None, description="List of page numbers to process")):
    """
    FastAPI endpoint to process a PDF file and return markdown content.
    """
    if type_of_statement == 'income':
        output_dir="files/output/income-rep/"
    elif type_of_statement == 'balance':
        output_dir="files/output/balance-rep/"
    vision_model = "gpt-4o"
    result = await process_file(
        file_path=file_path,
        model=vision_model,
        output_dir=output_dir,
        custom_system_prompt=prt.pdf2json_omniai_prompt,
        select_pages=select_pages,
    )
    return {"result": result}

# I would like to define an endpoint here that returns whether the fields are expenses or earnings
@app.get("/retrieve_field_type_classification")
async def retrieve_field_type_classification(
        type_of_statement: str,
        document_name:str):
    if type_of_statement == 'income':
        raw_stmnt_path=f"files/input/income-rep/{document_name}.md"
        clean_stmnt_path=f"files/input/income-rep/clean_{document_name}.json"
        type_stmnt_path=f"files/input/income-rep/type_{document_name}.json"
        type_field_prompt = prt.classify_income_type_prompt
    elif type_of_statement == 'balance':
        raw_stmnt_path=f"files/input/balance-rep/{document_name}.md"
        clean_stmnt_path=f"files/input/balance-rep/clean_{document_name}.json"
        type_stmnt_path=f"files/input/balance-rep/type_{document_name}.json"
        type_field_prompt = prt.classify_balance_type_prompt
    jsonparser = JsonOutputParser()
    index_year_stmnt_prompt = ChatPromptTemplate.from_messages([
        ("system", prt.index_year_stmnt_prompt)])
    with open(raw_stmnt_path, "r") as f:
        chain = index_year_stmnt_prompt | model | jsonparser
        statement= json.load(f)
        json_stmnt = chain.invoke({"financial_statement": statement})
        with open(clean_stmnt_path, "w") as writefile:
            downcased_stmnt = misc.downcase_keys(json_stmnt)
            json.dump(downcased_stmnt, writefile, indent=4)
            classify_amount_type_prompt = ChatPromptTemplate.from_messages([
                ("system", type_field_prompt)])
            chain = classify_amount_type_prompt | model | jsonparser
            type_fin_items = chain.invoke({"financial_statement": downcased_stmnt})
            with open(type_stmnt_path, "w") as writefile:
                json.dump(type_fin_items, writefile, indent=4)
            return {"result": type_fin_items}

@app.get("/retrieve_fields_classification")
async def retrieve_field_classification(
        type_of_statement: str,
        document_name:str):
    if type_of_statement == 'income':
        type_stmnt_path=f"files/input/income-rep/type_{document_name}.json"
        known_fields = misc.retrieve_income_rep_fields()
    elif type_of_statement == 'balance':
        type_stmnt_path=f"files/input/balance-rep/type_{document_name}.json"
        known_fields = misc.retrieve_balance_rep_fields()
    print(type_stmnt_path)
    print(known_fields)
    with open(type_stmnt_path,"r") as readfile:
        types_items = json.load(readfile)
        print(types_items)
        if type_of_statement == 'income':
            known_expense_items = []
            known_earning_items = []
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
        elif type_of_statement == 'balance':
            known_asset_items = []
            known_liability_items = []
            known_equity_items = []
            provided_asset_items = misc.filter_keys_by_category(types_items, 'asset')
            provided_liability_items = misc.filter_keys_by_category(types_items, 'liability')
            provided_equity_items = misc.filter_keys_by_category(types_items, 'equity')
            for item, desc in known_fields.items():
                if desc['fin_type'] == 'asset':
                    known_asset_items.append((item, desc['description']))
                elif desc['fin_type'] == 'liability':
                    known_liability_items.append((item, desc['description']))
                elif desc['fin_type'] == 'equity':
                    known_equity_items.append((item, desc['description']))
            jsonparser = JsonOutputParser()
            unknown_to_known_prompt = ChatPromptTemplate.from_messages([
                ("system", prt.classify_fields_unknown_to_known_prompt)])
            chain = unknown_to_known_prompt | model | jsonparser
            asset_mapping_res = chain.invoke({"unknown_financial_terms": provided_asset_items,
                                                "known_financial_items": known_asset_items})
            liability_mapping_res = chain.invoke({"unknown_financial_terms": provided_liability_items,
                                                "known_financial_items": known_liability_items})
            equity_mapping_res = chain.invoke({"unknown_financial_terms": provided_equity_items,
                                                "known_financial_items": known_equity_items})
            return {"result": {
                'asset_mapping': asset_mapping_res,
                'liability_mapping': liability_mapping_res,
                'equity_mapping': equity_mapping_res}}
