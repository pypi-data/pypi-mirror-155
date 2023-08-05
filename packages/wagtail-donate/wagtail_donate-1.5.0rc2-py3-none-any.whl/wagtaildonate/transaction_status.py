class TransactionStatus:
    provider_transaction_status: str
    transaction_status: str

    def __init__(self, *, provider_transaction_status: str, transaction_status: str):
        self.provider_transaction_status = provider_transaction_status
        self.transaction_status = transaction_status
