from .enums import url_values

def url_creator(page=None, search=None):
    
    """
    Create a URL for accessing book resources based on provided page number and search query.

    Args:
        page (int or None): The page number to navigate to (optional).
        search (str or None): The search query to filter book results (optional).

    Returns:
        str: The generated URL for accessing book resources.

    Example:
        # Generate URL for page 2 with search query "and"
        url = url_creator(page=2, search="and")
        url = "https://gutendex.com/books/?page=2&search=and"
    """
    
    if (page and search):
        url = url_values["url"] + "?" + url_values["page_parameter"] + "=" + page + "&" + url_values["search_parameter"] + "=" + search
    elif ((page is None) and (search)):
        url = url_values["url"] + "?" + url_values["search_parameter"] + "=" + search
    elif ((page) and (search is None)):
        url = url_values["url"] + "?" + url_values["page_parameter"] + "=" + page
    else:
        url = url_values["url"]
        
    return url