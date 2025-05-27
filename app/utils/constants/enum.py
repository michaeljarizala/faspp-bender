from enum import Enum

class TransactionStatus(str, Enum):
    all = "all"
    open = "open"
    cancelled = "cancelled"