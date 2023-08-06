from ..rupine_db import herokuDbAccess
from ..DataStructures.ObjViewEvmTokenLiqPool import ObjViewEvmTokenLiqPool
from psycopg2 import sql

def ParseObjViewEvmTokenLiqPool(data):
    retObj = ObjViewEvmTokenLiqPool()
    retObj.token_address = data[0]
    retObj.chain_id = data[1] 
    retObj.abi = data[2]
    retObj.symbol = data[3]
    retObj.name = data[4]
    retObj.decimals = data[5]
    retObj.token_class = data[6]
    retObj.totalsupply = data[7]
    retObj.keywords = data[8]
    retObj.telegram_link = data[9] 
    retObj.creator_address = data[10] 
    retObj.creation_timestamp = data[11] 
    retObj.creation_block_number = data[12] 
    retObj.creation_tx_hash = data[13] 
    retObj.max_tx_amount_percent = data[14]
    retObj.max_wallet_size_percent = data[15]
    retObj.is_verified = data[16]
    retObj.is_honeypot = data[17]
    retObj.buy_tax = data[18]
    retObj.sell_tax = data[19]
    retObj.latest_timestamp_token_history = data[20]
    retObj.liquidity_pool_address = data[21] 
    retObj.exchange_name = data[22] 
    retObj.latest_timestamp_lp = data[23] 
    retObj.created_at_lp = data[24] 
    retObj.modified_at_lp = data[25] 
    retObj.token_side = data[26] 
    retObj.reserve_a = data[27] 
    retObj.reserve_b = data[28] 
    retObj.is_sellable = data[29] 
    retObj.holder_count = data[30] 
    retObj.volume_daily = data[31] 
    return retObj

def getEvmLatestTokenLiquidityPools(connection, schema, chain_id):
    
    # query database    
    query = sql.SQL("SELECT token_address, chain_id, abi, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, max_tx_amount_percent, max_wallet_size_percent, is_verified, is_honeypot, buy_tax, sell_tax, latest_timestamp_token_history, liquidity_pool_address, exchange_name, latest_timestamp_lp, created_at_lp, modified_at_lp, token_side, reserve_a, reserve_b, is_sellable, holder_count, volume_daily \
        FROM {}.v_evm_latest_token_liquidity_pools WHERE chain_id = %s").format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id], connection)  

    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjViewEvmTokenLiqPool(tok)
        rows.append(addRow)

    # return objects
    return rows

def getEvmLatestTokenLiquidityPoolsWithoutName(connection, schema, chain_id, gteCreatedAt):

    # query database    
    query = sql.SQL("SELECT token_address, chain_id, abi, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, max_tx_amount_percent, max_wallet_size_percent, is_verified, is_honeypot, buy_tax, sell_tax, latest_timestamp_token_history, liquidity_pool_address, exchange_name, latest_timestamp_lp, created_at_lp, modified_at_lp, token_side, reserve_a, reserve_b, is_sellable, holder_count, volume_daily \
        FROM {}.v_evm_latest_token_liquidity_pools WHERE chain_id = %s AND name = 'n/a' AND creation_timestamp >= %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,gteCreatedAt], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjViewEvmTokenLiqPool(tok)
        rows.append(addRow)
    
    # return objects
    return rows

def getEvmLatestTokenLiquidityPoolsNotLaunched(connection, schema, chain_id, gteCreatedAt):
    
    # query database    
    query = sql.SQL("SELECT token_address, chain_id, abi, symbol, name, decimals, token_class, totalsupply, keywords, telegram_link, creator_address, creation_timestamp, creation_block_number, creation_tx_hash, max_tx_amount_percent, max_wallet_size_percent, is_verified, is_honeypot, buy_tax, sell_tax, latest_timestamp_token_history, liquidity_pool_address, exchange_name, latest_timestamp_lp, created_at_lp, modified_at_lp, token_side, reserve_a, reserve_b, is_sellable, holder_count, volume_daily \
         FROM {}.v_evm_latest_token_liquidity_pools WHERE chain_id = %s AND liquidity_pool_address is NULL AND creation_timestamp >= %s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,gteCreatedAt], connection) 

    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseObjViewEvmTokenLiqPool(tok)
        rows.append(addRow)

    # return objects
    return rows