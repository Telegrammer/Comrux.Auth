from .transaction import Transaction


class UnitOfWork:
    def __init__(self):
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        print(transaction)
        self._transactions.append(transaction)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            for transaction in self._transactions:
                await transaction.complete()
        else:
            for transaction in self._transactions:
                await transaction.cancel()
