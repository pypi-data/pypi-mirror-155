from requests.models import Response
import requests 
import logging 

class RequestsMessage:
    def __init__(self, method:str= '', url:str='', endpoint_name:str='', **kwargs):
        self.method = method
        self.url = url
        self.endpoint_name = endpoint_name
        self.kwargs = kwargs
    
    def __validate_minimum_information(self) -> bool:
        return self.method and self.url
    
    def make_request(self):
        has_minimum_info = self.__validate_minimum_information()
        if has_minimum_info:
            try:
                logging.warning(f"START {self.method} for {self.endpoint_name}")
                logging.warning(f"URL {self.url}")
                for k,v in self.kwargs.items():
                    logging.warning(f"{k.upper()}: {v}")
                response = requests.request(method = self.method, url = self.url, **self.kwargs)
                logging.warning(f"RESPONSE_STATUS_CODE: {response.status_code}")
                logging.warning(f"CONTENT: {response.content}")
                logging.warning(f"RESPONSE: {response}")
                logging.warning(f"END {self.method} for {self.endpoint_name}")
            except requests.exceptions.RequestException as e:
                logging.warning(f"ERROR in request: {e}")
                response = Response()
                response.code ='Request Error'
                response.status_code = 500
                response._content = b'{"message": "Internal Error of Request", "error": "error in requests"}'
                return response
        else:
            logging.warning(f"You don't have enough info for make request at {self.endpoint_name}. Please verify that the url or method are correct")
            response = Response()
            response.code ='Bad Request'
            response.status_code = 400
            response._content = b'{"message": "You do not have enough info for make this requests. Please verify that the url or method are correct", "error": "error in requests"}'
        return response 