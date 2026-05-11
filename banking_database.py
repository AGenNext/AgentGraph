"""
Banking Database - Financial Institutions

Banking database:
- Banks, Credit Unions
- Accounts, Transactions
- Loans, Mortgages

Reference:
- FDIC BankFind: https://www.fdic.gov/bank-fail/
- OCC: https://www.occ.gov/

Schema.org: BankAccount, FinancialProduct

Data Sources:
- FDIC Bank Database
- NCUA Credit Unions
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class AccountType(Enum):
    Checking = "Checking"
    Savings = "Savings"
    Money_Market = "Money Market"
    CD = "CD"


@dataclass
class Bank:
    id: str
    name: str
    
    charter: str = ""  # FDIC Charter Number
    
    assets: float = 0.0
    
    headquarters: str = ""
    
    website: str = ""


@dataclass
class Account:
    id: str
    bank_id: str
    account_type: AccountType
    
    balance: float = 0.0
    interest_rate: float = 0.0


class BankingDatabase:
    def __init__(self):
        self.banks: Dict[str, Bank] = {}
        self.accounts: Dict[str, Account] = {}
    
    def add_bank(self, b: Bank) -> str:
        self.banks[b.id] = b
        return b.id
    
    def stats(self) -> Dict:
        return {"banks": len(self.banks), "accounts": len(self.accounts)}


def main():
    db = BankingDatabase()
    b = Bank(id="b1", name="Chase", assets=5000000000)
    db.add_bank(b)
    print(f"Bank: {b.name}, Assets: ${b.assets:,}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()