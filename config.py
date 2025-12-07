import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the application"""
    
    # TronGrid API Configuration
    TRONGRID_API_KEY = os.getenv('TRONGRID_API_KEY', '')
    TRONGRID_BASE_URL = 'https://api.trongrid.io'
    
    # TronScan API Configuration (optional)
    TRONSCAN_API_KEY = os.getenv('TRONSCAN_API_KEY', '')
    TRONSCAN_BASE_URL = 'https://apilist.tronscanapi.com/api'
    
    # USDT TRC20 Contract Address
    USDT_CONTRACT = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'
    
    # Analysis Configuration
    MAX_DEPTH = 2  # Reduced to 2 for faster analysis
    MAX_TRANSACTIONS_PER_ADDRESS = 200  # Limit transactions per address for performance
    MAX_EXCHANGE_WALLET_LOOKUP = 50  # Limit exchange hot wallets
    MAX_ADDRESSES_TO_EXPLORE = 200  # Increased for deeper search (prevents runaway)
    MAX_CONNECTIONS_PER_ADDRESS = 30  # Increased to explore more connections per address
    MAX_NEIGHBORS_TO_EXPAND = 30  # Number of direct neighbors to expand at each level
    MAX_SECOND_LEVEL_NEIGHBORS = 20  # Number of second-level neighbors to explore
    MIN_TRANSACTION_AMOUNT = 10.0  # Filter transactions < $10 USDT (research recommendation)
    MAX_NODE_CONNECTIONS = 500  # Prune nodes with >500 connections (likely exchange/mixer/contract)
    
    # Exchange Addresses (major exchanges - will be loaded from API/data)
    from exchange_addresses import EXCHANGE_ADDRESSES
    EXCHANGE_ADDRESSES = EXCHANGE_ADDRESSES
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

