class InvalidEmailVerificationTokenError(Exception):
    pass
class InvalidPasswordError(Exception):
    pass
class EmailNotFoundError(Exception):
    pass
class RefreshTokenAlreadyConsumed(Exception):
    pass
class FailedToCreateVerificationLinkError(Exception):
    pass
class RegistrationError(Exception):
    pass
class EmailLookUpError(Exception):
    pass
class TokenExpiredError(Exception):
    pass
class InvalidUserIdError(Exception):
    pass
