from kozmodb_sdk.server import Server

from kozmodb_sdk.connectors.rest_api import RestAPI

DEFAULT_LOCAL_API_URL = 'http://127.0.0.1:47334'
DEFAULT_CLOUD_API_URL = 'https://cloud.kozmodb.com'


def connect(
        url: str = None,
        login: str = None,
        password: str = None,
        api_key: str = None,
        is_managed: bool = False,
        cookies=None,
        headers=None) -> Server:
    """
    Create connection to kozmodb server

    :param url: url to kozmodb server
    :param login: user login, for cloud version it contents email
    :param password: user password to login (for cloud version)
    :param api_key: API key to authenticate (for cloud version)
    :param is_managed: whether or not the URL points to a managed instance
    :param cookies: addtional cookies to send with the connection, optional
    :param headers: addtional headers to send with the connection, optional
    :return: Server object

    Examples
    --------

    >>> import kozmodb_sdk

    Connect to local server

    >>> con = kozmodb_sdk.connect()
    >>> con = kozmodb_sdk.connect('http://127.0.0.1:47334')

    Connect to cloud server

    >>> con = kozmodb_sdk.connect('https://cloud.kozmodb.com', api_key='-')

    Connect to KozmoDB pro

    >>> con = kozmodb_sdk.connect('http://<YOUR_INSTANCE_IP>', login='a@b.com', password='-', is_managed=True)

    """
    if url is None:
        if login is not None:
            # default is cloud
            url = DEFAULT_CLOUD_API_URL
        else:
            # is local
            url = DEFAULT_LOCAL_API_URL

    api = RestAPI(url, login, password, api_key, is_managed, 
                  cookies=cookies, headers=headers)

    return Server(api)
