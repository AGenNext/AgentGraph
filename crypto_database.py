"""
Cryptocurrency & Finance Database

Crypto and finance database:
- Cryptocurrencies
- Wallets
- Exchanges
- Transactions
- DeFi

Reference:
- CoinGecko/CoinMarketCap style
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# =============================================================================
# TYPES
# =============================================================================

class CoinType(Enum):
    Cryptocurrency = "Cryptocurrency"
    Token = "Token"
    Stablecoin = "Stablecoin"
    Utility_Token = "Utility Token"
    Security_Token = "Security Token"


class WalletType(Enum):
    Hot = "Hot"
    Cold = "Cold"
    Custodial = "Custodial"
    Non_Custodial = "Non-Custodial"


class TransactionType(Enum):
    Send = "Send"
    Receive = "Receive"
    Swap = "Swap"
    Trade = "Trade"
    Stake = "Stake"
    Unstake = "Unstake"
    Reward = "Reward"


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class Cryptocurrency:
    """Cryptocurrency"""
    id: str  # coin ID
    symbol: str  # BTC
    name: str  # Bitcoin
    
    type: CoinType = CoinType.Cryptocurrency
    
    network: str = ""  # blockchain
    
    contract: str = ""  # for tokens
    
    max_supply: Optional[int] = None
    circulating_supply: int = 0
    total_supply: int = 0
    
    price_usd: float = 0.0
    price_change_24h: float = 0.0
    price_change_7d: float = 0.0
    
    market_cap: float = 0.0
    volume_24h: float = 0.0
    
    rank: int = 0
    
    ath: float = 0.0  # All-time high
    atl: float = 0.0  # All-time low
    
    description: str = ""
    
    website: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "symbol": self.symbol,
            "price": self.price_usd,
            "rank": self.rank
        }


@dataclass
class Exchange:
    """Exchange"""
    id: str
    name: str
    
    type: str = ""  # Centralized, Decentralized
    
    country: str = ""
    
    established: Optional[int] = None
    
    website: str = ""
    
    trading_fee: float = 0.0
    
    withdrawal_fee: float = 0.0
    
    volume_24h: float = 0.0
    
    coins: List[str] = field(default_factory=list)


@dataclass
class Wallet:
    """Wallet"""
    id: str
    
    user_id: str
    
    type: WalletType = WalletType.Non_Custodial
    
    address: str = ""
    
    network: str = ""  # blockchain
    
    balance: Dict[str, float] = field(default_factory=dict)  # coin_id -> amount
    
    private_key_hash: str = ""  # Not stored directly
    
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Transaction:
    """Transaction"""
    id: str
    user_id: str
    
    type: TransactionType
    
    coin_id: str
    
    amount: float = 0.0
    
    price_usd_at_time: float = 0.0
    
    value_usd: float = 0.0
    
    fee: float = 0.0
    
    from_address: str = ""
    to_address: str = ""
    
    tx_hash: str = ""
    
    status: str = "Pending"  # Pending, Confirmed, Failed
    
    timestamp: datetime = field(default_factory=datetime.now)
    
    confirmed_at: Optional[datetime] = None
    
    block_number: Optional[int] = None


@dataclass
class staking:
    """Staking position"""
    id: str
    user_id: str
    coin_id: str
    
    amount: float = 0.0
    
    reward_rate: float = 0.0  # APY
    
    start_date: datetime = field(default_factory=datetime.now)
    
    claimed_rewards: float = 0.0
    
    pending_rewards: float = 0.0


# =============================================================================
# DATABASE
# =============================================================================

class CryptoDatabase:
    """Crypto database"""
    
    def __init__(self):
        self.cryptocurrencies: Dict[str, Cryptocurrency] = {}
        self.exchanges: Dict[str, Exchange] = {}
        self.wallets: Dict[str, Wallet] = {}
        self.transactions: Dict[str, Transaction] = {}
        self.staking_positions: Dict[str, staking] = {}
    
    # Cryptocurrencies
    def add_coin(self, coin: Cryptocurrency) -> str:
        self.cryptocurrencies[coin.id] = coin
        return coin.id
    
    def get_coin(self, coin_id: str) -> Optional[Cryptocurrency]:
        return self.cryptocurrencies.get(coin_id)
    
    def get_coin_by_symbol(self, symbol: str) -> Optional[Cryptocurrency]:
        symbol = symbol.upper()
        for coin in self.cryptocurrencies.values():
            if coin.symbol.upper() == symbol:
                return coin
        return None
    
    def search_coins(
        self,
        query: str = None,
        coin_type: CoinType = None,
        network: str = None
    ) -> List[Cryptocurrency]:
        results = list(self.cryptocurrencies.values())
        
        if query:
            q = query.lower()
            results = [
                c for c in results
                if q in c.name.lower() or q in c.symbol.lower()
            ]
        
        if coin_type:
            results = [c for c in results if c.type == coin_type]
        
        if network:
            results = [c for c in results if c.network == network]
        
        return results
    
    def get_top_coins(self, limit: int = 10) -> List[Cryptocurrency]:
        return sorted(
            self.cryptocurrencies.values(),
            key=lambda c: c.market_cap,
            reverse=True
        )[:limit]
    
    def get_trending(self, limit: int = 10) -> List[Cryptocurrency]:
        return sorted(
            self.cryptocurrencies.values(),
            key=lambda c: c.price_change_24h,
            reverse=True
        )[:limit]
    
    # Exchanges
    def add_exchange(self, exchange: Exchange) -> str:
        self.exchanges[exchange.id] = exchange
        return exchange.id
    
    def get_exchange(self, exchange_id: str) -> Optional[Exchange]:
        return self.exchanges.get(exchange_id)
    
    def search_exchanges(self, query: str = None) -> List[Exchange]:
        results = list(self.exchanges.values())
        
        if query:
            q = query.lower()
            results = [
                e for e in results
                if q in e.name.lower()
            ]
        
        return results
    
    # Wallets
    def create_wallet(
        self,
        user_id: str,
        network: str,
        wallet_type: WalletType = WalletType.Non_Custodial
    ) -> Wallet:
        wallet = Wallet(
            id=f"{user_id}_{network}",
            user_id=user_id,
            network=network,
            type=wallet_type
        )
        
        self.wallets[wallet.id] = wallet
        return wallet
    
    def get_wallet(self, wallet_id: str) -> Optional[Wallet]:
        return self.wallets.get(wallet_id)
    
    def get_user_wallets(self, user_id: str) -> List[Wallet]:
        return [
            w for w in self.wallets.values()
            if w.user_id == user_id
        ]
    
    def update_balance(
        self,
        wallet_id: str,
        coin_id: str,
        amount: float
    ) -> bool:
        wallet = self.wallets.get(wallet_id)
        if not wallet:
            return False
        
        wallet.balance[coin_id] = amount
        return True
    
    # Transactions
    def add_transaction(
        self,
        tx: Transaction
    ) -> str:
        self.transactions[tx.id] = tx
        return tx.id
    
    def get_transaction(self, tx_id: str) -> Optional[Transaction]:
        return self.transactions.get(tx_id)
    
    def get_user_transactions(
        self,
        user_id: str,
        limit: int = 50
    ) -> List[Transaction]:
        txs = [
            t for t in self.transactions.values()
            if t.user_id == user_id
        ]
        
        txs.sort(key=lambda t: t.timestamp, reverse=True)
        
        return txs[:limit]
    
    def get_coin_transactions(
        self,
        coin_id: str,
        limit: int = 50
    ) -> List[Transaction]:
        txs = [
            t for t in self.transactions.values()
            if t.coin_id == coin_id
        ]
        
        txs.sort(key=lambda t: t.timestamp, reverse=True)
        
        return txs[:limit]
    
    # Staking
    def stake(
        self,
        user_id: str,
        coin_id: str,
        amount: float,
        reward_rate: float
    ) -> staking:
        position = staking(
            id=f"stake_{user_id}_{coin_id}",
            user_id=user_id,
            coin_id=coin_id,
            amount=amount,
            reward_rate=reward_rate
        )
        
        self.staking_positions[position.id] = position
        return position
    
    def get_staking_position(
        self,
        user_id: str,
        coin_id: str
    ) -> Optional[staking]:
        key = f"stake_{user_id}_{coin_id}"
        return self.staking_positions.get(key)
    
    def calculate_rewards(self, position_id: str) -> float:
        position = self.staking_positions.get(position_id)
        if not position:
            return 0.0
        
        # Simplified - actual calculation would be more complex
        days = (datetime.now() - position.start_date).days
        return position.amount * (position.reward_rate / 100) * (days / 365)
    
    # Statistics
    def stats(self) -> Dict:
        total_market_cap = sum(c.market_cap for c in self.cryptocurrencies.values())
        
        return {
            "total_coins": len(self.cryptocurrencies),
            "total_exchanges": len(self.exchanges),
            "total_wallets": len(self.wallets),
            "total_transactions": len(self.transactions),
            "total_market_cap": total_market_cap
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Cryptocurrency Database")
    print("=" * 50)
    
    db = CryptoDatabase()
    
    # Add coins
    coins = [
        Cryptocurrency(
            id="bitcoin", symbol="BTC", name="Bitcoin",
            network="Bitcoin",
            price_usd=45000.0, market_cap=850_000_000_000,
            rank=1
        ),
        Cryptocurrency(
            id="ethereum", symbol="ETH", name="Ethereum",
            network="Ethereum",
            price_usd=2500.0, market_cap=300_000_000_000,
            rank=2
        ),
        Cryptocurrency(
            id="solana", symbol="SOL", name="Solana",
            network="Solana",
            price_usd=100.0, market_cap=40_000_000_000,
            rank=3
        ),
    ]
    
    for coin in coins:
        db.add_coin(coin)
    
    print(f"\nCoins: {db.stats()['total_coins']}")
    print(f"Total market cap: ${db.stats()['total_market_cap']:,.0f}")
    
    # Top coins
    print("\nTop coins:")
    for c in db.get_top_coins():
        print(f"  {c.rank}. {c.name} ({c.symbol}): ${c.price_usd:,.2f}")
    
    # Search
    print("\nSearch 'Ethereum':")
    coin = db.get_coin_by_symbol("ETH")
    if coin:
        print(f"  {coin.name}: ${coin.price_usd}")
    
    # Create wallet
    wallet = db.create_wallet("user1", "Bitcoin")
    print(f"\nWallet: {wallet.id}")
    
    print(f"\nStats:")
    stats = db.stats()
    print(f"  {stats}")


if __name__ == "__main__":
    main()