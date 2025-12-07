"""
Tron API client for fetching transaction data and checking blacklist status
"""
import requests
import time
from typing import List, Dict, Optional, Set
from config import Config

class TronAPI:
    def __init__(self):
        self.api_key = Config.TRONGRID_API_KEY
        self.tronscan_api_key = Config.TRONSCAN_API_KEY
        self.base_url = Config.TRONGRID_BASE_URL
        self.tronscan_url = Config.TRONSCAN_BASE_URL
        self.usdt_contract = Config.USDT_CONTRACT
        
    def _make_request(self, url: str, params: Dict = None, headers: Dict = None) -> Optional[Dict]:
        """Make HTTP request with error handling and rate limiting"""
        if headers is None:
            headers = {}
            
        if self.api_key:
            headers['TRON-PRO-API-KEY'] = self.api_key
            
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            time.sleep(1)  # Rate limiting
            return None
    
    def get_usdt_transactions(self, address: str, limit: int = 200, 
                             fingerprint: str = None, direction: str = 'both') -> Dict:
        """
        Fetch USDT transactions for an address
        
        Args:
            address: Tron address to query
            limit: Max transactions per request (max 200)
            fingerprint: Pagination token
            direction: 'from', 'to', or 'both'
        """
        url = f"{self.base_url}/v1/accounts/{address}/transactions/trc20"
        params = {
            'contract_address': self.usdt_contract,
            'limit': min(limit, 200),
            'only_confirmed': True
        }
        
        if fingerprint:
            params['fingerprint'] = fingerprint
            
        if direction == 'from':
            params['only_from'] = True
        elif direction == 'to':
            params['only_to'] = True
            
        return self._make_request(url, params=params) or {}
    
    def get_all_usdt_transactions(self, address: str, direction: str = 'both', 
                                  max_transactions: Optional[int] = None) -> List[Dict]:
        """
        Fetch all USDT transactions for an address with pagination
        
        Args:
            address: Tron address
            direction: 'from', 'to', or 'both'
            max_transactions: Maximum number of transactions to fetch (None = all)
        """
        all_transactions = []
        fingerprint = None
        total_fetched = 0
        
        while True:
            if max_transactions and total_fetched >= max_transactions:
                break
                
            result = self.get_usdt_transactions(address, limit=200, 
                                               fingerprint=fingerprint, 
                                               direction=direction)
            
            if not result or 'data' not in result:
                break
                
            transactions = result['data']
            if not transactions:
                break
                
            all_transactions.extend(transactions)
            total_fetched += len(transactions)
            
            # Get next page token
            meta = result.get('meta', {})
            fingerprint = meta.get('fingerprint')
            
            if not fingerprint:
                break
                
            # Rate limiting
            time.sleep(0.2)
            
        return all_transactions
    
    def check_blacklist_status(self, address: str) -> Dict:
        """Check if address is blacklisted using TronScan API"""
        url = f"{self.tronscan_url}/security/account/data"
        params = {'address': address}
        
        result = self._make_request(url, params=params)
        if result:
            return {
                'is_blacklisted': result.get('is_black_list', False),
                'has_fraud_transaction': result.get('has_fraud_transaction', False),
                'fraud_token_creator': result.get('fraud_token_creator', False),
                'risk_score': result.get('risk_score', 0)
            }
        return {'is_blacklisted': False, 'risk_score': 0}
    
    def get_account_info(self, address: str) -> Dict:
        """Get account information"""
        url = f"{self.base_url}/v1/accounts/{address}"
        return self._make_request(url) or {}
    
    def get_transaction_details(self, tx_hash: str) -> Dict:
        """Get detailed transaction information"""
        url = f"{self.base_url}/v1/transactions/{tx_hash}"
        return self._make_request(url) or {}


