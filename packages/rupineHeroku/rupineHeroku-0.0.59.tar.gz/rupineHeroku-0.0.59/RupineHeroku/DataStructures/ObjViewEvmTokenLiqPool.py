
from unicodedata import decimal


class ObjViewEvmTokenLiqPool:
    token_address = None
    chain_id = None 
    abi = None
    symbol = None
    name = None
    decimals = 0
    token_class = ''
    totalsupply = 0
    keywords = ''
    telegram_link = ''
    creator_address = ''
    creation_timestamp = 0 
    creation_block_number = 0 
    creation_tx_hash = '' 
    max_tx_amount_percent = 0 
    max_wallet_size_percent = 0 
    is_verified = False 
    is_honeypot = False 
    buy_tax = 0 
    sell_tax = 0  
    latest_timestamp_token_history = 0 
    liquidity_pool_address = ''
    exchange_name = ''
    latest_timestamp_lp = 0
    created_at_lp = 0
    modified_at_lp = 0
    token_side = ''
    reserve_a = 0
    reserve_b = 0
    is_sellable = ''
    holder_count = 0
    volume_daily = 0

    def __init__(self):
        pass

    def __eq__(self, other): 
        if not isinstance(other, ObjViewEvmTokenLiqPool):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.token_address == other.token_address and
                self.chain_id == other.chain_id and
                self.abi == other.abi and
                self.symbol == other.symbol and
                self.name == other.name and
                self.decimals == other.decimals and
                self.token_class == other.token_class and
                self.totalsupply == other.totalsupply and
                self.keywords == other.keywords and
                self.telegram_link == other.telegram_link and
                self.creator_address == other.creator_address and
                self.creation_timestamp == other.creation_timestamp and
                self.creation_block_number == other.creation_block_number and
                self.creation_tx_hash == other.creation_tx_hash and
                self.max_tx_amount_percent == other.max_tx_amount_percent and
                self.max_wallet_size_percent == other.max_wallet_size_percent and
                self.is_verified == other.is_verified and
                self.is_honeypot == other.is_honeypot and
                self.buy_tax == other.buy_tax and
                self.sell_tax == other.sell_tax and
                self.latest_timestamp_token_history == other.latest_timestamp_token_history and
                self.liquidity_pool_address == other.liquidity_pool_address and
                self.exchange_name == other.exchange_name and
                self.latest_timestamp_lp == other.latest_timestamp_lp and
                self.created_at_lp == other.created_at_lp and
                self.modified_at_lp == other.modified_at_lp and
                self.token_side == other.token_side and
                self.reserve_a == other.reserve_a and
                self.reserve_b == other.reserve_b and
                self.is_sellable == other.is_sellable and
                self.holder_count == other.holder_count and
                self.volume_daily == other.volume_daily)

    def clone(self):
        retTok = ObjViewEvmTokenLiqPool()
        retTok.token_address = self.token_address
        retTok.chain_id = self.chain_id
        retTok.abi = self.abi
        retTok.symbol = self.symbol
        retTok.name = self.name
        retTok.decimals = self.decimals
        retTok.token_class = self.token_class
        retTok.totalsupply = self.totalsupply
        retTok.keywords = self.keywords
        retTok.telegram_link = self.telegram_link
        retTok.creator_address = self.creator_address
        retTok.creation_timestamp = self.creation_timestamp
        retTok.creation_block_number = self.creation_block_number
        retTok.creation_tx_hash = self.creation_tx_hash
        retTok.max_tx_amount_percent = self.max_tx_amount_percent
        retTok.max_wallet_size_percent = self.max_wallet_size_percent
        retTok.is_verified = self.is_verified
        retTok.is_honeypot = self.is_honeypot
        retTok.buy_tax = self.buy_tax
        retTok.sell_tax = self.sell_tax
        retTok.latest_timestamp_token_history = self.latest_timestamp_token_history
        retTok.liquidity_pool_address = self.liquidity_pool_address
        retTok.exchange_name = self.exchange_name
        retTok.latest_timestamp_lp = self.latest_timestamp_lp
        retTok.created_at_lp = self.created_at_lp
        retTok.modified_at_lp = self.modified_at_lp
        retTok.token_side = self.token_side
        retTok.reserve_a = self.reserve_a
        retTok.reserve_b = self.reserve_b
        retTok.is_sellable = self.is_sellable
        retTok.holder_count = self.holder_count
        retTok.volume_daily = self.volume_daily
        return retTok