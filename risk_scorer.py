"""
Advanced Risk Scoring Module for Blockchain Wallet Analysis

Implements comprehensive risk scoring based on:
- Blacklist/sanctions status
- Transaction pattern analysis
- Graph-based proximity metrics
- Behavioral analysis
- Exchange/service connections
- Volume analysis
- Time-based patterns
- Path complexity

Based on research from Chainalysis, TRM Labs, SlowMist, and academic papers.
"""

from typing import Dict, List, Set, Optional, Tuple
import networkx as nx
from collections import Counter, defaultdict
from datetime import datetime
import statistics
from config import Config


class RiskScorer:
    """
    Advanced risk scoring engine for wallet connection paths
    """
    
    # Risk thresholds and weights
    RISK_WEIGHTS = {
        'blacklist': 50.0,           # Highest priority
        'sanctions': 45.0,            # OFAC/SDN lists
        'mixer_tumbler': 40.0,        # Mixing services
        'known_scam': 35.0,           # Known scam addresses
        'unregulated_exchange': 30.0, # Unregulated exchanges
        'velocity_anomaly': 25.0,     # Rapid transactions
        'structuring': 22.0,          # Amount structuring
        'high_connectivity': 18.0,    # Money laundering patterns
        'path_complexity': 15.0,      # Complex paths (>6 hops)
        'volume_anomaly': 12.0,       # Unusual transaction sizes
        'time_anomaly': 10.0,         # Suspicious timing
        'exchange_risk': 8.0,         # Exchange connections (mixed)
        'hot_wallet': 5.0,            # High activity indicators
        'community_risk': 7.0,        # High-risk communities
    }
    
    # Volume thresholds (in USDT)
    VOLUME_THRESHOLDS = {
        'very_large': 1000000.0,      # $1M+
        'large': 100000.0,            # $100K+
        'medium': 10000.0,            # $10K+
        'small': 1000.0,              # $1K+
    }
    
    # Velocity thresholds (transactions per hour)
    VELOCITY_THRESHOLDS = {
        'very_high': 60,              # 60+ tx/hour
        'high': 30,                   # 30+ tx/hour
        'moderate': 10,               # 10+ tx/hour
    }
    
    # Known risky service patterns (partial list - should be expanded)
    MIXER_PATTERNS = [
        'tornado',
        'mixer',
        'tumbler',
        'blender',
    ]
    
    def __init__(self, graph: nx.DiGraph, exchange_addresses: Set[str] = None):
        """
        Initialize risk scorer
        
        Args:
            graph: NetworkX directed graph of transactions
            exchange_addresses: Set of known exchange addresses
        """
        self.graph = graph
        self.exchange_addresses = exchange_addresses or set()
        self.blacklisted_addresses = set()
        self.sanctioned_addresses = set()
        self.known_scam_addresses = set()
        self.mixer_addresses = set()
        
        # Cache for risk scores to avoid recalculation
        self._address_risk_cache = {}
        self._path_risk_cache = {}
    
    def score_path(self, path: List[str], path_data: Dict = None) -> Dict:
        """
        Calculate comprehensive risk score for a connection path
        
        Args:
            path: List of addresses in the path
            path_data: Additional path metadata (transactions, amounts, etc.)
            
        Returns:
            Dictionary with risk score and detailed breakdown
        """
        if not path or len(path) < 2:
            return {
                'total_risk_score': 0,
                'risk_level': 'low',
                'breakdown': {},
                'warnings': []
            }
        
        path_data = path_data or {}
        transactions = path_data.get('transactions', [])
        total_amount = path_data.get('total_amount', 0)
        
        risk_components = {}
        warnings = []
        
        # 1. Blacklist and Sanctions Risk (Highest Priority)
        blacklist_risk, blacklist_warnings = self._calculate_blacklist_risk(path)
        risk_components['blacklist'] = blacklist_risk['score']
        warnings.extend(blacklist_warnings)
        
        # 2. Transaction Pattern Analysis
        pattern_risk, pattern_warnings = self._analyze_transaction_patterns(
            path, transactions, total_amount
        )
        risk_components.update(pattern_risk)
        warnings.extend(pattern_warnings)
        
        # 3. Graph-Based Proximity Risk
        proximity_risk, proximity_warnings = self._calculate_proximity_risk(path)
        risk_components.update(proximity_risk)
        warnings.extend(proximity_warnings)
        
        # 4. Behavioral Analysis
        behavioral_risk, behavioral_warnings = self._analyze_behavior(
            path, transactions
        )
        risk_components.update(behavioral_risk)
        warnings.extend(behavioral_warnings)
        
        # 5. Path Complexity Risk
        complexity_risk, complexity_warnings = self._analyze_path_complexity(
            path, transactions
        )
        risk_components.update(complexity_risk)
        warnings.extend(complexity_warnings)
        
        # 6. Volume Analysis
        volume_risk, volume_warnings = self._analyze_volume_patterns(
            transactions, total_amount
        )
        risk_components.update(volume_risk)
        warnings.extend(volume_warnings)
        
        # Calculate total risk score (sum of weighted components)
        total_risk_score = sum(risk_components.values())
        
        # Cap at 100
        total_risk_score = min(100.0, total_risk_score)
        
        # Determine risk level
        risk_level = self._determine_risk_level(total_risk_score)
        
        return {
            'total_risk_score': round(total_risk_score, 2),
            'risk_level': risk_level,
            'breakdown': risk_components,
            'warnings': warnings,
            'recommendation': self._get_recommendation(total_risk_score, warnings)
        }
    
    def _calculate_blacklist_risk(self, path: List[str]) -> Tuple[Dict, List[str]]:
        """
        Calculate blacklist and sanctions risk
        
        Returns:
            Tuple of (risk_dict, warnings_list)
        """
        risk_score = 0.0
        warnings = []
        
        blacklisted_count = 0
        sanctioned_count = 0
        
        for addr in path:
            if addr in self.blacklisted_addresses:
                blacklisted_count += 1
                risk_score += self.RISK_WEIGHTS['blacklist']
                warnings.append(f"🚫 BLACKLISTED ADDRESS: {addr[:12]}...")
            elif addr in self.sanctioned_addresses:
                sanctioned_count += 1
                risk_score += self.RISK_WEIGHTS['sanctions']
                warnings.append(f"⚠️ SANCTIONED ADDRESS: {addr[:12]}...")
        
        # Add mixer/tumbler detection
        for addr in path:
            if addr in self.mixer_addresses:
                risk_score += self.RISK_WEIGHTS['mixer_tumbler']
                warnings.append(f"🌀 MIXER/TUMBLER DETECTED: {addr[:12]}...")
        
        # Known scam addresses
        for addr in path:
            if addr in self.known_scam_addresses:
                risk_score += self.RISK_WEIGHTS['known_scam']
                warnings.append(f"⚠️ KNOWN SCAM ADDRESS: {addr[:12]}...")
        
        return {
            'score': min(risk_score, 100.0),
            'blacklisted_count': blacklisted_count,
            'sanctioned_count': sanctioned_count
        }, warnings
    
    def _analyze_transaction_patterns(
        self, path: List[str], transactions: List[Dict], total_amount: float
    ) -> Tuple[Dict, List[str]]:
        """
        Analyze transaction patterns for suspicious behavior
        
        Patterns detected:
        - Velocity anomalies (rapid transactions)
        - Structuring (breaking large amounts)
        - Rapid consolidation
        """
        risk_components = {}
        warnings = []
        
        if not transactions:
            return risk_components, warnings
        
        # Extract transaction timestamps and amounts
        timestamps = []
        amounts = []
        
        for tx in transactions:
            tx_list = tx.get('tx_hashes', [])
            if tx_list:
                # Use transaction timestamps if available
                # For now, we'll use edge count as proxy
                pass
            
            amount = tx.get('total_amount', 0)
            count = tx.get('count', 0)
            
            if amount > 0:
                amounts.append(amount)
            
            if count > 0:
                timestamps.extend([None] * count)  # Placeholder
        
        # Velocity Analysis
        # If we have multiple transactions in short time, flag as velocity anomaly
        if len(transactions) > 1:
            total_tx_count = sum(tx.get('count', 1) for tx in transactions)
            # Estimate: if >10 transactions per hop, likely velocity anomaly
            if total_tx_count > 30:  # Adjust based on path length
                velocity_risk = self.RISK_WEIGHTS['velocity_anomaly']
                risk_components['velocity_anomaly'] = velocity_risk
                warnings.append(f"⚡ VELOCITY ANOMALY: {total_tx_count} transactions detected")
        
        # Structuring Detection
        # Look for patterns where amounts are just below thresholds
        if amounts:
            struct_count = 0
            for amount in amounts:
                # Check if amount is just below common thresholds (structuring pattern)
                if 9000 <= amount < 10000 or 90000 <= amount < 100000:
                    struct_count += 1
            
            if struct_count >= 3:
                struct_risk = self.RISK_WEIGHTS['structuring']
                risk_components['structuring'] = struct_risk
                warnings.append(f"📊 STRUCTURING DETECTED: {struct_count} transactions just below thresholds")
        
        # High Connectivity (Potential Money Laundering)
        # Check if any address in path has very high degree
        for addr in path:
            if addr in self.graph:
                in_degree = self.graph.in_degree(addr)
                out_degree = self.graph.out_degree(addr)
                total_degree = in_degree + out_degree
                
                # If address has >500 connections, likely exchange/mixer/ML pattern
                if total_degree > 500:
                    high_conn_risk = self.RISK_WEIGHTS['high_connectivity']
                    risk_components['high_connectivity'] = high_conn_risk
                    warnings.append(f"🔗 HIGH CONNECTIVITY: {addr[:12]}... has {total_degree} connections")
                    break  # Only count once per path
        
        return risk_components, warnings
    
    def _calculate_proximity_risk(self, path: List[str]) -> Tuple[Dict, List[str]]:
        """
        Calculate graph-based proximity to known risky addresses
        
        Measures distance in transaction graph to blacklisted/sanctioned addresses
        """
        risk_components = {}
        warnings = []
        
        if not self.blacklisted_addresses and not self.sanctioned_addresses:
            return risk_components, warnings
        
        all_risky = self.blacklisted_addresses | self.sanctioned_addresses
        
        # Check if any path address is directly connected to risky addresses
        for addr in path:
            if addr in self.graph:
                # Check successors (outgoing)
                successors = set(self.graph.successors(addr))
                risky_successors = successors & all_risky
                
                # Check predecessors (incoming)
                predecessors = set(self.graph.predecessors(addr))
                risky_predecessors = predecessors & all_risky
                
                if risky_successors or risky_predecessors:
                    # Direct connection to risky address
                    proximity_risk = self.RISK_WEIGHTS['blacklist'] * 0.8  # 80% of direct blacklist risk
                    risk_components['proximity_to_risky'] = proximity_risk
                    warnings.append(f"🔴 PROXIMITY RISK: {addr[:12]}... directly connected to risky address")
                    break  # Only count once
        
        # Check for 2-hop proximity (address connected to address connected to risky)
        for addr in path:
            if addr in self.graph:
                # 2-hop check
                neighbors = set(self.graph.successors(addr)) | set(self.graph.predecessors(addr))
                for neighbor in neighbors:
                    if neighbor in self.graph:
                        neighbor_neighbors = set(self.graph.successors(neighbor)) | set(self.graph.predecessors(neighbor))
                        if neighbor_neighbors & all_risky:
                            proximity_risk = self.RISK_WEIGHTS['blacklist'] * 0.4  # 40% for 2-hop
                            risk_components['proximity_to_risky_2hop'] = proximity_risk
                            warnings.append(f"🟡 2-HOP PROXIMITY: {addr[:12]}... within 2 hops of risky address")
                            break
                if 'proximity_to_risky_2hop' in risk_components:
                    break
        
        return risk_components, warnings
    
    def _analyze_behavior(
        self, path: List[str], transactions: List[Dict]
    ) -> Tuple[Dict, List[str]]:
        """
        Analyze behavioral patterns
        
        - Hot wallet activity
        - Exchange connections
        - Community risk
        """
        risk_components = {}
        warnings = []
        
        # Exchange connections (mixed signal - can reduce or increase risk)
        exchange_count = sum(1 for addr in path if addr in self.exchange_addresses)
        if exchange_count > 0:
            # Exchange connections can be legitimate or used for laundering
            # If many exchanges in path, might indicate layering
            if exchange_count >= 3:
                risk_components['multiple_exchanges'] = self.RISK_WEIGHTS['exchange_risk'] * 1.5
                warnings.append(f"🏦 MULTIPLE EXCHANGES: {exchange_count} exchange addresses in path (possible layering)")
            elif exchange_count == 1:
                # Single exchange connection is usually legitimate
                risk_components['exchange_connection'] = -5.0  # Reduces risk slightly
                warnings.append(f"🏦 EXCHANGE CONNECTION: Legitimate exchange detected (risk reduced)")
        
        # Hot wallet detection (high transaction activity)
        # This is handled in SlowMist analyzer, but we can add here too
        high_activity_count = 0
        for addr in path:
            if addr in self.graph:
                in_degree = self.graph.in_degree(addr)
                out_degree = self.graph.out_degree(addr)
                if in_degree + out_degree > 50:  # High activity threshold
                    high_activity_count += 1
        
        if high_activity_count > 2:
            risk_components['hot_wallet_activity'] = self.RISK_WEIGHTS['hot_wallet'] * high_activity_count
            warnings.append(f"🔥 HIGH ACTIVITY: {high_activity_count} high-activity addresses in path")
        
        return risk_components, warnings
    
    def _analyze_path_complexity(
        self, path: List[str], transactions: List[Dict]
    ) -> Tuple[Dict, List[str]]:
        """
        Analyze path complexity for money laundering patterns
        
        Research shows: Paths with 6+ intermediate addresses are suspicious
        """
        risk_components = {}
        warnings = []
        
        hops = len(path) - 1
        
        # Path complexity risk (layering pattern)
        if hops >= 6:
            complexity_risk = self.RISK_WEIGHTS['path_complexity']
            risk_components['complex_path'] = complexity_risk * (hops / 6)  # Scale with hops
            warnings.append(f"🔀 COMPLEX PATH: {hops} hops detected (possible layering)")
        elif hops >= 4:
            complexity_risk = self.RISK_WEIGHTS['path_complexity'] * 0.5
            risk_components['complex_path'] = complexity_risk
            warnings.append(f"🔀 MODERATE COMPLEXITY: {hops} hops in path")
        
        return risk_components, warnings
    
    def _analyze_volume_patterns(
        self, transactions: List[Dict], total_amount: float
    ) -> Tuple[Dict, List[str]]:
        """
        Analyze transaction volume patterns
        
        - Unusually large transactions
        - Volume anomalies
        """
        risk_components = {}
        warnings = []
        
        if not transactions:
            return risk_components, warnings
        
        # Extract amounts
        amounts = [tx.get('total_amount', 0) for tx in transactions if tx.get('total_amount', 0) > 0]
        
        if not amounts:
            return risk_components, warnings
        
        max_amount = max(amounts)
        avg_amount = statistics.mean(amounts) if amounts else 0
        total_amount = sum(amounts)
        
        # Very large transaction
        if max_amount >= self.VOLUME_THRESHOLDS['very_large']:
            volume_risk = self.RISK_WEIGHTS['volume_anomaly'] * 2.0
            risk_components['very_large_transaction'] = volume_risk
            warnings.append(f"💰 VERY LARGE TRANSACTION: ${max_amount:,.0f} USDT")
        elif max_amount >= self.VOLUME_THRESHOLDS['large']:
            volume_risk = self.RISK_WEIGHTS['volume_anomaly']
            risk_components['large_transaction'] = volume_risk
            warnings.append(f"💰 LARGE TRANSACTION: ${max_amount:,.0f} USDT")
        
        # Total volume analysis
        if total_amount >= self.VOLUME_THRESHOLDS['very_large']:
            volume_risk = self.RISK_WEIGHTS['volume_anomaly'] * 1.5
            risk_components['high_total_volume'] = volume_risk
            warnings.append(f"💰 HIGH TOTAL VOLUME: ${total_amount:,.0f} USDT across path")
        
        return risk_components, warnings
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level from score"""
        if score >= 70:
            return 'critical'
        elif score >= 50:
            return 'high'
        elif score >= 30:
            return 'medium'
        elif score >= 15:
            return 'low-medium'
        else:
            return 'low'
    
    def _get_recommendation(self, score: float, warnings: List[str]) -> str:
        """Get recommendation based on risk score"""
        if score >= 70:
            return "⚠️ CRITICAL RISK: Do not proceed with this transaction. Addresses are blacklisted or show severe risk indicators."
        elif score >= 50:
            return "🔴 HIGH RISK: Strongly recommend additional due diligence before proceeding. Multiple risk factors detected."
        elif score >= 30:
            return "🟡 MEDIUM RISK: Proceed with caution. Some risk indicators present. Review transaction details carefully."
        elif score >= 15:
            return "🟢 LOW-MEDIUM RISK: Generally safe but monitor for unusual patterns."
        else:
            return "✅ LOW RISK: Transaction appears to be low risk. Standard monitoring recommended."
    
    def register_blacklisted_address(self, address: str):
        """Register a blacklisted address"""
        self.blacklisted_addresses.add(address)
        self._address_risk_cache.clear()  # Clear cache
    
    def register_sanctioned_address(self, address: str):
        """Register a sanctioned address"""
        self.sanctioned_addresses.add(address)
        self._address_risk_cache.clear()
    
    def register_mixer_address(self, address: str):
        """Register a mixer/tumbler address"""
        self.mixer_addresses.add(address)
        self._address_risk_cache.clear()
    
    def register_scam_address(self, address: str):
        """Register a known scam address"""
        self.known_scam_addresses.add(address)
        self._address_risk_cache.clear()
    
    def batch_register_risky_addresses(
        self, 
        blacklisted: List[str] = None,
        sanctioned: List[str] = None,
        mixers: List[str] = None,
        scams: List[str] = None
    ):
        """Batch register risky addresses"""
        if blacklisted:
            self.blacklisted_addresses.update(blacklisted)
        if sanctioned:
            self.sanctioned_addresses.update(sanctioned)
        if mixers:
            self.mixer_addresses.update(mixers)
        if scams:
            self.known_scam_addresses.update(scams)
        self._address_risk_cache.clear()

