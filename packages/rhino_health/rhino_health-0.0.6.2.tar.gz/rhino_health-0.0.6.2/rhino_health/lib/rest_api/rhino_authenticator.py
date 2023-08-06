import logging
from typing import Optional

import arrow
import requests

from rhino_health.lib.rest_api.api_request import APIRequest
from rhino_health.lib.rest_api.api_response import APIResponse
from rhino_health.lib.rest_api.request_adapter import RequestAdapter
from rhino_health.lib.utils import url_for


class RhinoAuthenticator(RequestAdapter):
    """
    Keeps track of authenticating with our backend API
    """

    AUTHORIZATION_KEY = "authorization"
    UNAUTHENTICATED_STATUS_CODE = 401
    DEFAULT_MAX_RETRY_COUNT = 2

    def __init__(
        self,
        base_url: str,
        email: str,
        password: str,
        otp_code: Optional[str] = None,
        max_retry_count: int = DEFAULT_MAX_RETRY_COUNT,
    ):
        # TODO: Include active_workgroup in the future
        self.base_url = base_url
        self.email = email
        self.password = password
        self.otp_code = otp_code
        self.max_retry_count = max_retry_count
        self.login_token: Optional[str] = None
        self.login_timeout: Optional[arrow.Arrow] = None
        self.refresh_token: Optional[str] = None
        self.refresh_timeout: Optional[arrow.Arrow] = None

    def _login(self):
        data = {"email": self.email, "password": self.password}
        if self.otp_code:
            data["otp_code"] = self.otp_code
        raw_response = requests.post(
            url_for(self.base_url, "auth/obtain_token"),
            data=data,
        ).json()
        if "access" in raw_response:
            self.login_token = raw_response["access"]
            self.login_timeout = arrow.utcnow().shift(minutes=5)
            self.refresh_token = raw_response["refresh"]
            self.refresh_timeout = arrow.utcnow().shift(hours=10)
        else:
            raise Exception(raw_response.get("detail", "Error occurred trying to connect"))

    def _refresh_token(self):
        raw_response = requests.post(
            url_for(self.base_url, "auth/refresh_token"),
            data={"refresh": self.refresh_token},
        ).json()
        self.login_token = raw_response.get("access")
        if not self.login_token:
            raise ValueError("Invalid email or password")

    def _should_reauthenticate(self):
        return (self.login_token is None) or (arrow.utcnow() > self.login_timeout)

    def _can_refresh(self):
        refresh_expired = (self.refresh_timeout is None) or (arrow.utcnow() > self.refresh_timeout)
        return self._refresh_token is not None and not refresh_expired

    def authenticate(self):
        if self._can_refresh():
            self._refresh_token()
        else:
            self._login()

    def before_request(self, api_request: APIRequest, adapter_kwargs: dict):
        if self._should_reauthenticate():
            self.authenticate()
        api_request.headers[self.AUTHORIZATION_KEY] = f"Bearer {self.login_token}"

    def after_request(
        self, api_request: APIRequest, api_response: APIResponse, adapter_kwargs: dict
    ):
        unauthenticated = api_response.status_code == self.UNAUTHENTICATED_STATUS_CODE
        retry_allowed = api_request.request_count <= self.max_retry_count
        if unauthenticated and retry_allowed:
            api_request.request_status = APIRequest.RequestStatus.RETRY
            logging.debug("Refreshing login token")
            self.authenticate()
            api_request.request_count += 1
        return
