"""Entry point to using the Rhino Health Python SDK."""

__version__ = "0.0.6.2"

import rhino_health.lib.endpoints
import rhino_health.lib.metrics
from rhino_health.lib.constants import ApiEnvironment
from rhino_health.lib.rhino_client import SDKVersion
from rhino_health.lib.rhino_session import RhinoSession

# Which modules to autogenerate documentation for
__api__ = [
    "rhino_health.lib.metrics",
    "rhino_health.lib.endpoints",
    "rhino_health.lib.constants",
    "rhino_health.lib.rhino_session",
    "rhino_health.lib.rest_api",
]


def login(
    username,
    password,
    otp_code=None,
    rhino_api_url=ApiEnvironment.PROD_API_URL,
    sdk_version=SDKVersion.PREVIEW,
):
    """
    Login to the Rhino platform and get a RhinoSession to interact with the rest of the system.

    Parameters
    ----------
    username: str
        The email you are logging in with
    password: str
        The password you are logging in with
    otp_code: Optional[str]
        If 2FA is enabled for the account, the One Time Password code from your 2FA device
    rhino_api_url: Optional[ApiEnvironment]
        Which rhino environent you are working in.
    sdk_version: Optional[SDKVersion]
        Used internally for future backwards compatibility. Use the default

    Returns
    -------
    session: RhinoSession
        A session object to interact with the cloud API

    Examples
    --------
    >>> import rhino_health
    >>> my_username = "rhino_user@rhinohealth.com" # Replace me
    >>> my_password = "ASecurePasswordYouSet321" # Replace me
    >>> session = rhino_health.login(username=my_username, password=my_password, otp_code=otp_code)
    RhinoSession()

    See Also
    --------
    rhino_health.lib.constants.ApiEnvironment : List of supported environments
    rhino_health.lib.rhino_session.RhinoSession : Session object with accessible endpoints
    """
    return RhinoSession(username, password, otp_code, rhino_api_url, sdk_version)
