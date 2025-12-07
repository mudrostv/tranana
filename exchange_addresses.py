"""
Known exchange hot wallet addresses on Tron network
This list can be expanded with more addresses as needed
"""
# Major exchange hot wallet addresses (examples - should be updated with actual addresses)
EXCHANGE_ADDRESSES = {
    # Binance hot wallets (examples)
    'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t',  # USDT contract (not exchange, but commonly used)
    # Add more known exchange addresses here
    # These would typically be obtained from:
    # - Public exchange deposit addresses
    # - Tron-Connection-Finder database
    # - Chainalysis or other analytics platforms
}

def load_exchange_addresses_from_file(filepath: str = None) -> set:
    """
    Load exchange addresses from a file if provided
    Format: one address per line
    """
    if not filepath:
        return EXCHANGE_ADDRESSES.copy()
    
    try:
        with open(filepath, 'r') as f:
            addresses = {line.strip() for line in f if line.strip().startswith('T')}
        return addresses
    except FileNotFoundError:
        return EXCHANGE_ADDRESSES.copy()

def is_exchange_address(address: str) -> bool:
    """Check if an address is a known exchange address"""
    return address in EXCHANGE_ADDRESSES


