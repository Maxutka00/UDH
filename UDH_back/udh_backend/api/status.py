from enum import Enum, auto


class StatusEnumerator(Enum):
    UserDoesNotExists = auto()
    UserInvalidToken = auto()
    UserSuccess = auto()
    UserTokenExpired = auto()
    UserLoginDoesNotMatch = auto()
    DataTooLong = auto()
