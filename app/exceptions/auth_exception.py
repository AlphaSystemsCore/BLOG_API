class InvalidEmailVerificationTokenError(Exception):
    """raise when the email_verification_token is invalid, when checked with the stored email_verification_token"""
    pass
class InvalidPasswordError(Exception):
    """Raised when the password, is not matching the stored password"""
    pass
class EmailNotFoundError(Exception):
    """Raised when the email, is not found in the database during the lookup"""
    pass
class RefreshTokenAlreadyConsumed(Exception):
    """Raised when the refresh_token is found to have been consumed during an attempt to verify the refresh_token"""
    pass
class FailedToCreateVerificationLinkError(Exception):
    """Raise when an attempt to create verification_link fails"""
    pass
class RegistrationError(Exception):
    """Raise when Registration of new user fails"""
    pass
class EmailLookUpError(Exception):
    """Raised when the email, is not found in the database during the lookup"""
    pass
class TokenExpiredError(Exception):
    """Raise when the token has expired, and hence invalid"""
    pass
class InvalidUserIdError(Exception):
    """Raised when the user_id is invalid hence not found in the db lookup"""
    pass
