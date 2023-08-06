"""
Constants that are used in the rest of the system
"""


class ApiEnvironment:
    """
    Which environment you are hitting. By default you should be using PROD_API_URL

    Examples
    --------
    >>> from rhino_health import ApiEnvironment.LOCALHOST_API_URL, ApiEnvironment.DEV_URL, ApiEnvironment.PROD_API_URL, ApiEnvironment.DEMO_DEV_URL
    """

    LOCALHOST_API_URL = "http://localhost:8080/api/"
    DEV_URL = "https://dev.rhinohealth.com/api/"
    DEMO_DEV_URL = "https://demo-dev.rhinohealth.com/api/"
    PROD_API_URL = "https://prod.rhinohealth.com/api/"
