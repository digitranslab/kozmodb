from pydantic_settings import BaseSettings


class KozmoEndpointHandlerConfig(BaseSettings):
    """
    Configuration for Kozmo Endpoint handler.

    Attributes
    ----------

    BASE_URL : str
        Base URL for the Kozmo Endpoint API.
    """

    BASE_URL: str = "https://llm.mdb.ai/"


kozmo_endpoint_handler_config = KozmoEndpointHandlerConfig()
