JWT_ERROR_MESSAGES = {
    "no_token": {"code": "NO_TOKEN", "message": "Authentication token was not found. Please log in."},
    "invalid_token": {"code": "INVALID_TOKEN", "message": "Invalid access token."},
    "token_expired": {"code": "TOKEN_EXPIRED", "message": "Access token has expired."},
    "token_error": {"code": "TOKEN_ERROR", "message": "Access token was modified or invalid."},
    "user_inactive": {"code": "USER_INACTIVE", "message": "User account is inactive or unverified."},
    "unexpected": {"code": "UNEXPECTED_ERROR", "message": "Unexpected authentication error."},
}


INTERNAL_SERVER_ERROR = {
    "server_error": {
        "error": "Internal server error"
    }
}