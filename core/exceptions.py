class Error(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return self.args[0]


class InvalidTransactionAmount(Error):
    pass


class SameTransferId(Error):
    pass


class UserDoesNotExist(Error):
    pass


class WeakPasswordEntered(Error):
    pass


class TransactionUndefinedError(Error):
    pass


class InsufficientFundsToCompleteTransaction(Error):
    pass


class CrossTransactionError(Error):
    pass


class TransactionAmountNotWithinRange(Error):
    pass


class WrongPassword(Error):
    pass


class EmptyQueryResultError(Error):
    pass
