"""
SlowMist-inspired feature extraction for address classification
Adapted from SlowMist's automatic-tron-address-clustering
"""
from typing import Dict, List, Tuple
from collections import defaultdict
import numpy as np

class SlowMistFeatureExtractor:
    """
    Extract features from transaction history for ML-based address classification
    Features based on SlowMist's approach:
    - Number of transfers in/out
    - Number of unique addresses transferred in/out
    - Average amount transferred in/out
    - Average transaction interval (minutes)
    - Monetary value
    """
    
    def __init__(self):
        pass
    
    def extract_features(self, address: str, transactions: List[Dict]) -> Dict[str, float]:
        """
        Extract features for address classification
        
        Args:
            address: Wallet address
            transactions: List of transaction dictionaries
            
        Returns:
            Dictionary of extracted features
        """
        if not transactions:
            return self._empty_features()
        
        # Separate incoming and outgoing transactions
        incoming = [tx for tx in transactions if tx.get('to', '').strip() == address]
        outgoing = [tx for tx in transactions if tx.get('from', '').strip() == address]
        
        # Basic counts
        out_count = len(outgoing)
        in_count = len(incoming)
        
        # Unique address counts
        out_addr_count = len(set(tx.get('to', '') for tx in outgoing)) if outgoing else 0
        in_addr_count = len(set(tx.get('from', '') for tx in incoming)) if incoming else 0
        
        # Average amounts
        out_avg = self._average_amount(outgoing)
        in_avg = self._average_amount(incoming)
        
        # Transaction interval (time between transactions)
        gap_time = self._min_gap_time(transactions)
        
        # Monetary value (total volume)
        total_volume = sum(self._get_amount(tx) for tx in transactions)
        
        # Additional features
        # Transaction frequency (transactions per day)
        if transactions:
            timestamps = sorted([self._get_timestamp(tx) for tx in transactions if self._get_timestamp(tx) > 0])
            if len(timestamps) > 1:
                time_span_days = (timestamps[-1] - timestamps[0]) / (24 * 60 * 60 * 1000)
                frequency = len(transactions) / max(time_span_days, 1)
            else:
                frequency = 0
        else:
            frequency = 0
        
        # Balance change pattern
        net_flow = in_avg * in_count - out_avg * out_count
        
        return {
            'out_count': out_count,
            'in_count': in_count,
            'out_addr_count': out_addr_count,
            'in_addr_count': in_addr_count,
            'out_avg_amount': out_avg,
            'in_avg_amount': in_avg,
            'min_gap_time_minutes': gap_time,
            'total_volume': total_volume,
            'transaction_frequency': frequency,
            'net_flow': net_flow,
            'total_transactions': len(transactions)
        }
    
    def classify_address(self, features: Dict[str, float]) -> Tuple[str, float]:
        """
        Classify address as Hot Wallet, Cold Wallet, or Common User
        Based on SlowMist's feature-based approach (simplified)
        
        Args:
            features: Extracted features dictionary
            
        Returns:
            Tuple of (classification, confidence_score)
        """
        out_count = features.get('out_count', 0)
        in_count = features.get('in_count', 0)
        out_addr_count = features.get('out_addr_count', 0)
        in_addr_count = features.get('in_addr_count', 0)
        total_txns = features.get('total_transactions', 0)
        frequency = features.get('transaction_frequency', 0)
        total_volume = features.get('total_volume', 0)
        
        # Scoring based on SlowMist's patterns
        hot_score = 0
        cold_score = 0
        common_score = 0
        
        # Hot wallet indicators:
        # - High transaction count
        # - High unique address count
        # - High frequency
        # - Large volume
        if total_txns > 1000:
            hot_score += 3
        elif total_txns > 100:
            hot_score += 2
        elif total_txns > 10:
            hot_score += 1
        
        if out_addr_count > 50 or in_addr_count > 50:
            hot_score += 3
        elif out_addr_count > 10 or in_addr_count > 10:
            hot_score += 2
        
        if frequency > 10:  # More than 10 txns per day
            hot_score += 2
        elif frequency > 1:
            hot_score += 1
        
        if total_volume > 1000000:  # > $1M
            hot_score += 2
        
        # Cold wallet indicators:
        # - Low transaction count
        # - Low frequency
        # - Large individual amounts
        if total_txns < 10 and frequency < 0.1:
            cold_score += 3
        elif total_txns < 50:
            cold_score += 1
        
        if features.get('min_gap_time_minutes', 0) > 10080:  # > 1 week between txns
            cold_score += 2
        
        # Common user (default)
        if hot_score < 3 and cold_score < 2:
            common_score = 5
        
        # Determine classification
        scores = {
            'hot': hot_score,
            'cold': cold_score,
            'common': common_score
        }
        
        max_score = max(scores.values())
        classification = max(scores, key=scores.get)
        
        # Calculate confidence (0-1)
        total_score = sum(scores.values())
        confidence = max_score / max(total_score, 1)
        
        return classification, confidence
    
    def _get_amount(self, tx: Dict) -> float:
        """Extract amount from transaction"""
        value = tx.get('value', '0')
        if isinstance(value, str):
            try:
                return int(value) / 1e6
            except:
                return 0.0
        return float(value) / 1e6
    
    def _get_timestamp(self, tx: Dict) -> float:
        """Extract timestamp from transaction"""
        return float(tx.get('block_timestamp', 0))
    
    def _average_amount(self, transactions: List[Dict]) -> float:
        """Calculate average transaction amount"""
        if not transactions:
            return 0.0
        amounts = [self._get_amount(tx) for tx in transactions]
        return sum(amounts) / len(amounts)
    
    def _min_gap_time(self, transactions: List[Dict]) -> float:
        """Calculate minimum time gap between transactions in minutes"""
        if len(transactions) < 2:
            return 0.0
        
        timestamps = sorted([self._get_timestamp(tx) for tx in transactions if self._get_timestamp(tx) > 0])
        if len(timestamps) < 2:
            return 0.0
        
        gaps = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        min_gap_ms = min(gaps)
        return min_gap_ms / (60 * 1000)  # Convert to minutes
    
    def _empty_features(self) -> Dict[str, float]:
        """Return empty feature set"""
        return {
            'out_count': 0,
            'in_count': 0,
            'out_addr_count': 0,
            'in_addr_count': 0,
            'out_avg_amount': 0.0,
            'in_avg_amount': 0.0,
            'min_gap_time_minutes': 0.0,
            'total_volume': 0.0,
            'transaction_frequency': 0.0,
            'net_flow': 0.0,
            'total_transactions': 0
        }


