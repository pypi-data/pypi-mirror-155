import logging

def return_binary_result(value_to_evaluate, value_true:str = "", value_false:str = "")->str:
    return value_true if value_to_evaluate else value_false

def join_list_strings(values:list=[])->str:
    result = ""
    for item in values:
        if isinstance(item,str):
            result = result + item + " "
        else: 
            try:
                value_string = str(item)
                result = result + value_string + " "
            except Exception as e: 
                logging.warning(f"Is not possible convert {item} to string")
                continue
    return result