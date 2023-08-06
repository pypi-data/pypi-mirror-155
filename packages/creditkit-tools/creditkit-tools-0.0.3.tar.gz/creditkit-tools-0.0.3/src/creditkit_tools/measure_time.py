import time
import logging

def measure_time(name_function:str = ""):
    def wrapper(fn):
        def wrapped(*args, **kwargs):
            start = time.time()
            logging.warning(f"***** START MEASUREMENT OF: {name_function} *****")
            response = fn(*args, **kwargs)
            end = time.time() - start
            logging.warning(f"***** EXECUTE TIME: {end} seconds *****")
            logging.warning(f"***** END MEASUREMENT OF: {name_function} *****")
            return response
        return wrapped
    return wrapper