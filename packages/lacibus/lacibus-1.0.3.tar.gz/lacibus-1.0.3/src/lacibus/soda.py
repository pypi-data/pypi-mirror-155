'''
This module provides access to a Soda data content management system via its web API. 
'''

import requests
api = None
session = requests.session()


def set_api(url):
    '''Set the URL for access to the API.
    
    Parameters:
      * url(str): the URL of the system's API.
    '''
    global api
    api = url

 
def login(key):
    '''Log in to the API and start an authorized session. 
    
    Authorisation is provided by a key, which is a one-time password 
    obtained by some out-of-band means, not through this module.
    
    Subsequent function calls invoke the API to read and write data.
    Unless they use a credential, the data they can read or write 
    depends on the session access level, and this depends on the 
    value of the key. 
    
    Parameters:
      * key(str): a key. 
      
    Raises:
      * SodaException: if the login fails.
    '''
    
    global api
    parms = {'command': 'set_access_level_from_key'}
    files = {'key': ('key', key, 'text/plain; charset=utf-8')}
    response = session.post(api, files=files, params=parms)
    if response.status_code != 200: __handle_http_error(response)


def logout():
    '''
    Log out of the API and close the authorized session. 
    '''
    
    session.close()
    
    
def get_session():
    '''
    Get the session for access to the API.
    
    This method enables a session that has been authenticated
    by this module to be used by vdl (or other modules) for 
    API interactions.
    
    Returns:
      * the requests session.
    '''
    
    global session
    return session
        
                        
def __handle_http_error(response):
    '''
    Handle an error that occurs during an HTTP communication
    with a virtual data lake. The error may occur in transmission
    or during execution of the request by the virtual data lake.
    
    Parameters:
      * response the response to the HTTP request returned by the 
        imported requests module   
      
    Raises:
      * SodaException
    '''
    
    msg = None
    try:
        msg = response.json()['error']
    except:
        msg = str(response.status_code) + ': ' + response.reason
    raise SodaException(msg)


class SodaException(RuntimeError):
    '''
    A run-time exception occurring during execution of a 
    virtual data lake access function.
    '''
    def __init__(self, *messages):
        super().__init__(*messages)
