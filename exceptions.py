# Base class for exceptions

class ChallengeBotException(Exception):
    def __init__(self, message, *, expire_in=0):
        super().__init__(message)
        self._message = message
        self.expire_in = expire_in

    @property
    def message(self):
        return self._message

class CommandNotFoundException(ChallengeBotException):
    def __init__(self, message, *, expire_in=0):
        super().__init__(message, expire_in=expire_in)