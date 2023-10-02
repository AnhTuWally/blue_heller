# Create your views here.
def process_ajax_request(request, method='POST'):
    """
    Process an AJAX request and return the data if the request is valid 

    Args:
        request (HttpRequest): The request object
        method (str): The method to check for, defaults to POST

    Returns:
        data (dict): The data from the request
    
    Raises:
        ValueError: If the request is not AJAX or the method is not valid

    # TODO: Add support for GET requests

    Example:

    The request is processed and a dictionary is retured        
    >>> data = process_ajax_request(request)

    The dictionary can be used to access the data 
    >>> active_task_id = data.get('active_task_id', None)
    >>> start_time = data.get('start_time', None)
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == method:
            data = request.POST
            return data

    raise(ValueError("Invalid AJAX request"))

