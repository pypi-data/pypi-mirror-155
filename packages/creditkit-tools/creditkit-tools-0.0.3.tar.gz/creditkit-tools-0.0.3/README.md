# creditkit-tools

Creditkit-tools is a package with the most commons and frequents functions and operations in our creditkit project.

If you need more information about the project please verify the github repository
[Github-repository](https://github.com/JanoBourian/utils-creditkit)
or contact me like as @janobourian in almost social networks.

## About

This packages was born of one necessity by apply standard, reduct code and have disponibility to consume in any project into the corporation or for future develops.

## Included functions

    - measure_time: 
        - measure_time: is a decorator where its function is does measure execute times.

    - auxiliar_message:
        - RequestsMessage: class for management the requests methods, request and logs
            - __init__(): 
                - method: 'GET', 'POST', ...
                - url: url for the request
                - endpoint_name: The name or tag for the request
                - **kwargs: All kwargs of each one requests
            - make_response(): create the requests and sendt the info
    
    - format_text:
        - return_binary_result: This function takes a argument if this exist return value_true else value_false. value_true and value_false are strings, those can be like "yes" and "no".
        - join_list_strings: This function takes a list of arguments and concatenates each value (not empty) and return one string 