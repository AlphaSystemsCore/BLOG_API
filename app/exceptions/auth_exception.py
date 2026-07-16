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