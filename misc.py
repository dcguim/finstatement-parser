import income_rep_model as im
import balance_rep_model as bm
import netrc
import os

authinfo_filepath = "~/.authinfo"

def get_apikey():
    # Path to the authinfo file (default is ~/.netrc or ~/.authinfo)
    authinfo_path = os.path.expanduser(authinfo_filepath)
    try:
        # Parse the authinfo file
        credentials = netrc.netrc(authinfo_path)
        # Extract the password (API key) for the machine
        api_key = credentials.authenticators("api.openai.com")[2]
        if not api_key:
            raise ValueError("No API key found for 'api.openai.com' in the authinfo file.")
        return api_key
    except FileNotFoundError:
        raise FileNotFoundError(f"Authinfo file not found at {authinfo_path}.")
    except TypeError:
        raise ValueError("No entry for 'api.openai.com' found in the authinfo file.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the authinfo file: {e}")

def retrieve_income_rep_fields():
    print('enter retrieve_income_rep')
    # create a dict with the field and it's description
    st_income_fields = {}
    fields = im.COGS.__fields__ | im.OperatingExpenses.__fields__ | im.IncomeStatement.__fields__
    for field_name, field_info in fields.items():
        field_info = field_info
        description = field_info.description if field_info.description else 'No description'
        field_schema_extra = field_info.json_schema_extra or {}
        if not field_schema_extra:
            continue
        fin_type = field_schema_extra.get('fin_type', 'Not specified')
        st_income_fields[field_name] = {'description': description,
                                        'fin_type': fin_type}
    print(st_income_fields)
    return st_income_fields

def retrieve_balance_rep_fields():
    print('enter retrieve_balance_rep')
    # create a dict with the field and it's description
    st_balance_fields = {}
    fields = bm.CurrentAssets.__fields__ | bm.LongTermAssets.__fields__ | bm.CurrentLiabilities.__fields__ | bm.LongTermLiabilities.__fields__ | bm.Equity.__fields__ | bm.BalanceStatement.__fields__
    for field_name, field_info in fields.items():
        field_info = field_info
        description = field_info.description if field_info.description else 'No description'
        field_schema_extra = field_info.json_schema_extra or {}
        if not field_schema_extra:
            continue
        fin_type = field_schema_extra.get('fin_type', 'Not specified')
        st_balance_fields[field_name] = {'description': description,
                                         'fin_type': fin_type}
    return st_balance_fields


def downcase_keys(obj):
    if isinstance(obj, dict):
        # Recurse into each key-value pair and convert keys to lowercase
        return {k.lower(): downcase_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # If the object is a list, recurse into each item
        return [downcase_keys(item) for item in obj]
    else:
        # For other data types, return the object as-isb
        return obj

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
