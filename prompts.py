index_year_stmnt_prompt = """
Transform the the financial statement between triple backticks in JSON format. If the financial statement input is not a JSON, respond with: "Please provide a JSON input!"

    ```{financial_statement}``

1. Consider only the "Body" key of the input json and create a list of jsons where the year is the key.
2. For each year key, the output should be a json object with the name financial item name as key, and the correspondent number amount as value. The values should always be a number with it's respective sign. Try to deduce if the value if positive or negative and assign the correct sign.
3. If it's not possible to assign a number assign the json null value. 
4. Return nothing but a json containing a list of jsons with every year present in the body as a key. Ensure that all the years within the body section are present and contain the JSON value as described in steps 1 and 2.
"""

classify_amount_type_prompt = """
Transform the the financial statement between triple backticks in JSON format. If the financial statement input is not a JSON, respond with: "Please provide a JSON input!"

    ```{financial_statement}``


1. For each different item classify if it is earnings or expense, using firstly the meaning, the sign if available, and the items before and after.
2. Return should be ONLY a list of JSON objects. Each object should contain a single pair consisting of the  item's name, and either "earnings" or  "expenses". 
3. Try to classify all of the financial items! If it is absolutely not possible to classify the key assign the json "null" value.
"""

classify_fields_unknown_to_known_prompt = """
    Classify the unknown financial terms listed between triple ticks to the known financial description items listed between triple asterisks.

unknown financial terms =
    ```{unknown_financial_terms} ```

known financial items =
    ***{known_financial_items}***

Requirements: 
- Map each unknown financial term to exactly one known financial item. 
- Provide the result as a single json, only with unknown financial term as keys, and the known financial item name as value. Do not provide any explanations only the JSON result.
- Use the meaning item name and the meaning description to correctly map the financial term.
- Try to classify all unknown financial terms. If it's absolutely not possible to classify a unknown financial term to any known item using it's description and meaning  assign the JSON null value.
- Redefine the classification of nulls, and attempt to classify more terms.
"""


pdf2json_omniai_prompt="""
Convert the below PDF page into ONE JSON Object with the following properties :\n 
text : a list of dictionary of all content of all the paragraphs in the page. Do not include the components present in tables, graphs or financial statements in this section. We only want the paragraphs. Do not include superscripts or footnotes / headers. results should be in the following format : {section : The title of the section where the paragraph is present (if any otherwise "") , paragraph: The text content of each paragraph }
tables : This is a list of dictionaries. It should have all the tabular data present in the PDF in the following format: {Header: the header of the table, Body : The table's body}, 
graphs: This is a list of dictionaries. It should have a tabular representation of the graphs in the PDF page to the best of your availability in the following format: {Header: the header of the table, Body : The table's body},  
financial statements: This is a list of dictionaries. If any financial table or graph is present, they should be present in this property. It should have all the financial data present in the PDF in the following format: {Header: the header of the table, Body : The table's body}. In this content, financial data is anything sales, EBITDA,cost, debt. Anything that has to do with cash coming in or out.
FIBO entities : a list of dictionary in the following format {Entity: The entity present , Timestamp: The timestamp of the entity (if present) otherwise n.a., Value: The value of the entity } of FIBO Entites as per the ontology present in the page including a time stamp if present. The entities extracted should match the standard ontology terms 
images: images must be replaced with [Description of image].\n
summary: A detailed text summary of what is covered in the tables and the financial statements if any. We care mostly about the words here no need to mention any value apart from rate, dates and movements. If this is a continuation of another table, graph or statement provided in the context, mention briefly what were the previous ones about \n
All information should be  comma separated in a markdown format. \n 

    RULES:\n
    - If a table, graph or financial statements have no spefic headers, assume the header from the context provided carries over\n
    - Return only one JSON with no explanation text. Do not include deliminators like ```markdown. Only one JSON object should be returned, not multiple jsons in a single file!\n
    - Don't forget to extract Graphs, Financials and FIBO Entities. Don't forget to include a summary.\n
    - If the page is a table of content or a glossary of terms or a disclaimer or confidentiality or contact information/Title page (or usual end of document or beginning of pages that contain no useful information), return "".
    - You must include all information on the page. Do not exclude headers, footers, or subtext.\n
    - Return only one JSON object with the keys "text", "tables", "graphs", "FIBO entities", "images", "summary". DO NOT return multiple jsons in a single file!
"""
