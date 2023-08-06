import json
from typing import Optional, List, Dict, Type
from httpx import Response


class RobloxException(Exception):
    """
    Base exception.
    """
    pass

class ResponseError:
    """
    Represents an error returned by a Roblox game server.
    Attributes:
        code: The error code.
        message: The error message.
        user_facing_message: A more simple error message intended for frontend use.
        field: The field causing this error.
        retryable: Whether retrying this exception could supress this issue.
    """

    def __init__(self, data: dict):
        self.code: int = data["code"]
        self.message: Optional[str] = data.get("message")
        self.user_facing_message: Optional[str] = data.get("userFacingMessage")
        self.field: Optional[str] = data.get("field")
        self.retryable: Optional[str] = data.get("retryable")




class HTTPException(RobloxException):
    """
    Exception that's raised when an HTTP request fails.
    Attributes:
        response: The HTTP response object.
        status: The HTTP response status code.
        errors: A list of Roblox response errors.
    """

    def __init__(self, response: Response, errors: Optional[list] = None):
        """
        Arguments:
            response: The raw response object.
            errors: A list of errors.
        """
        self.response: Response = response
        self.status: int = response.status_code
        self.errors = [' ', ]
        if self.errors:
            try:
                error = response.json()["error"]
                error_detail = response.json()["errorDetails"][0]
                super().__init__(
                    f"{response.status_code} {response.reason_phrase}: {response.url}.\n\nError: {error}\nError detail: {error_detail}\nResponse JSON:\n{response.json()}")
            except json.decoder.JSONDecodeError:
                super().__init__(f"{response.status_code} {response.reason_phrase}: {response.url}]\nResponse JSON:\nUnloadable JSON.")
        else:
            super().__init__(f"{response.status_code} {response.reason_phrase}: {response.url}")


class BadRequest(HTTPException):
    """HTTP exception raised for status code 400."""
    pass


class Unauthorized(HTTPException):
    """HTTP exception raised for status code 401. This usually means you aren't properly authenticated."""


class Forbidden(HTTPException):
    """HTTP exception raised for status code 403. This usually means the X-CSRF-Token was not properly provided."""
    pass


class NotFound(HTTPException):
    """
    HTTP exception raised for status code 404.
    This usually means we have an internal URL issue - please make a GitHub issue about this!
    """
    pass


class TooManyRequests(HTTPException):
    """
    HTTP exception raised for status code 429.
    This means that Roblox has [ratelimited](https://en.wikipedia.org/wiki/Rate_limiting) you.
    """
    pass


class InternalServerError(HTTPException):
    """
    HTTP exception raised for status code 500.
    This usually means that there was an issue on Roblox's end, but due to faulty coding on Roblox's part this can
    sometimes mean that an endpoint used internally was disabled or that invalid parameters were passed.
    """
    pass

class BadGateway(HTTPException):
    """HTTP exception raised for status code 502.
    This means that Roblox servers gave a invbalid response.
    """
    pass


_codes_exceptions: Dict[int, Type[HTTPException]] = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    429: TooManyRequests,
    500: InternalServerError,
    502: BadGateway
}


def get_exception_from_status_code(code: int) -> Type[HTTPException]:
    """
    Gets an exception that should be raised instead of the generic HTTPException for this status code.
    """
    return _codes_exceptions.get(code) or HTTPException