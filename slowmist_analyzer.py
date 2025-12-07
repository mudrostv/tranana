"""
Enhanced Wallet Analyzer integrating SlowMist algorithms
Combines ML-based classification, graph algorithms, and path finding
"""
import networkx as nx
from typing import Dict, List, Set, Optional
from wallet_analyzer import WalletAnalyzer
from slowmist_features import SlowMistFeatureExtractor
from slowmist_graph_algorithms import SlowMistGraphAlgorithms
from tron_api import TronAPI
from config import Config
import time

class SlowMistEnhancedAnalyzer(WalletAnalyzer):
    """
    Enhanced analyzer that adds SlowMist's ML and graph algorithms
    """
    
    def __init__(self, enable_enhanced_risk_scoring: bool = True):
        # Enable enhanced risk scoring by default
        super().__init__(enable_enhanced_risk_scoring=enable_enhanced_risk_scoring)
        self.feature_extractor = SlowMistFeatureExtractor()
        self.graph_algorithms = None
        self.address_classifications = {}
        self.importance_scores = {}
    
    def analyze_connections(self, source: str, target: str) -> Dict:
        """
        Enhanced analysis with SlowMist algorithms
        
        Args:
            source: Source wallet address
            target: Target wallet address
            
        Returns:
            Enhanced analysis results with classifications and importance scores
        """
        print(f"Building graph from source: {source}")
        # Build graph from source (outgoing transactions)
        self.build_transaction_graph(source, depth=0, direction='from')
        
        print(f"Building graph from target: {target}")
        # Build graph from target (incoming transactions) 
        self.build_transaction_graph(target, depth=0, direction='to')
        
        # Limited expansion
        if source in self.graph and len(self.processed_addresses) < self.max_addresses:
            print("Expanding from source neighbors...")
            source_neighbors = list(self.graph.successors(source))[:5]
            for neighbor in source_neighbors:
                if len(self.processed_addresses) >= self.max_addresses:
                    break
                if neighbor not in self.processed_addresses:
                    time.sleep(0.15)
                    self.build_transaction_graph(neighbor, depth=1, direction='from')
        
        if target in self.graph and len(self.processed_addresses) < self.max_addresses:
            print("Expanding from target neighbors...")
            target_neighbors = list(self.graph.predecessors(target))[:5]
            for neighbor in target_neighbors:
                if len(self.processed_addresses) >= self.max_addresses:
                    break
                if neighbor not in self.processed_addresses:
                    time.sleep(0.15)
                    self.build_transaction_graph(neighbor, depth=1, direction='to')
        
        print("Applying SlowMist graph algorithms...")
        # Initialize graph algorithms
        self.graph_algorithms = SlowMistGraphAlgorithms(self.graph)
        
        # Compute PageRank for importance scoring
        print("  Computing PageRank...")
        pagerank_scores = self.graph_algorithms.compute_pagerank()
        self.importance_scores = pagerank_scores
        
        # Compute K-Core for community discovery
        print("  Computing K-Core communities...")
        kcore_scores = self.graph_algorithms.compute_kcore(k=1)
        
        # Label Propagation for community detection
        print("  Running Label Propagation...")
        communities = self.graph_algorithms.label_propagation()
        
        print("Classifying addresses...")
        # Classify important addresses
        key_addresses = self.graph_algorithms.find_key_addresses(top_n=20)
        
        print(f"Finding paths between {source} and {target}")
        # Find paths using bidirectional approach
        paths = self.find_paths_bidirectional(source, target, max_paths=20)
        
        if not paths:
            print("No direct paths found, trying extended search...")
            paths = self.find_paths_extended(source, target, max_paths=10)
        
        # Classify all addresses in paths and key addresses for comprehensive analysis
        print("Classifying addresses in paths...")
        all_path_addresses = set([source, target])
        for path in paths:
            all_path_addresses.update(path)
        
        for addr in list(all_path_addresses) + [a[0] for a in key_addresses[:15]]:
            if addr not in self.address_classifications:
                self._classify_address(addr)
                time.sleep(0.05)  # Rate limiting
        
        # Check blacklist status and exchange connections for key addresses
        print("Checking blacklist status and service connections...")
        addresses_to_check = set([source, target])
        for path in paths:
            addresses_to_check.update(path[:5])  # Check first 5 addresses in each path
        
        # Add key addresses
        for addr, _ in key_addresses[:15]:
            addresses_to_check.add(addr)
        
        blacklist_results = {}
        exchange_connections = {}
        wallet_ratings = {}
        
        for addr in list(addresses_to_check)[:30]:  # Limit API calls
            # Check blacklist
            try:
                blacklist_info = self.api.check_blacklist_status(addr)
                blacklist_results[addr] = blacklist_info
            except:
                blacklist_results[addr] = {'is_blacklisted': False, 'risk_score': 0}
            
            # Check if exchange address
            is_exchange = addr in self.exchange_addresses
            if is_exchange:
                exchange_connections[addr] = {
                    'is_exchange': True,
                    'exchange_name': self.exchange_addresses.get(addr, 'Unknown Exchange')
                }
            
            # Build comprehensive wallet rating
            classification = self.address_classifications.get(addr, {})
            importance = self.importance_scores.get(addr, 0.0)
            blacklist_risk = blacklist_results.get(addr, {}).get('risk_score', 0)
            
            # Calculate overall rating (0-100)
            rating = 50  # Base rating
            if classification.get('type') == 'hot':
                rating += 20
            elif classification.get('type') == 'cold':
                rating -= 10
            if importance > 0.001:
                rating += 15
            if blacklist_risk > 0:
                rating -= 30
            if is_exchange:
                rating += 10
            
            wallet_ratings[addr] = {
                'overall_rating': max(0, min(100, rating)),
                'classification': classification.get('type', 'unknown'),
                'confidence': classification.get('confidence', 0.0),
                'importance_score': importance,
                'blacklist_risk': blacklist_risk,
                'is_exchange': is_exchange,
                'is_blacklisted': blacklist_results.get(addr, {}).get('is_blacklisted', False)
            }
            
            time.sleep(0.1)  # Rate limiting
        
        # Update risk scorer graph if available (graph may have grown)
        if self.risk_scorer:
            self.risk_scorer.graph = self.graph
            # Register any blacklisted addresses found during analysis
            for addr, info in blacklist_results.items():
                if info.get('is_blacklisted'):
                    self.risk_scorer.register_blacklisted_address(addr)
        
        # Analyze each path with enhanced metrics
        analyzed_paths = []
        for path in paths:
            if path:
                path_analysis = self.analyze_path_enhanced(path)
                if path_analysis:
                    analyzed_paths.append(path_analysis)
                    time.sleep(0.1)
        
        # Sort by path length first (shortest), then by risk score
        analyzed_paths.sort(key=lambda x: (x.get('hops', 999), -x.get('risk_score', 0)))
        
        # Get blocked wallets list
        blocked_wallets = [addr for addr, info in blacklist_results.items() 
                          if info.get('is_blacklisted', False)]
        
        # Get service/exchange connections
        service_connections = []
        for addr, info in exchange_connections.items():
            service_connections.append({
                'address': addr,
                'service_type': 'Exchange',
                'service_name': info.get('exchange_name', 'Unknown')
            })
        
        return {
            'source': source,
            'target': target,
            'total_paths_found': len(analyzed_paths),
            'graph_statistics': {
                'nodes': self.graph.number_of_nodes(),
                'edges': self.graph.number_of_edges(),
                'processed_addresses': len(self.processed_addresses)
            },
            'paths': analyzed_paths,
            'shortest_path': analyzed_paths[0] if analyzed_paths else None,
            'slowmist_analysis': {
                'source_classification': self.address_classifications.get(source, {}),
                'target_classification': self.address_classifications.get(target, {}),
                'source_rating': wallet_ratings.get(source, {}),
                'target_rating': wallet_ratings.get(target, {}),
                'key_addresses': [
                    {
                        'address': addr,
                        'importance_score': score,
                        'classification': self.address_classifications.get(addr, {}).get('type', 'unknown'),
                        'rating': wallet_ratings.get(addr, {}),
                        'is_blacklisted': blacklist_results.get(addr, {}).get('is_blacklisted', False)
                    }
                    for addr, score in key_addresses[:15]
                ],
                'communities_detected': len(set(communities.values())) if communities else 0,
                'communities_list': self.graph_algorithms.get_community_list(
                    exchange_addresses=self.exchange_addresses,
                    blacklisted_addresses=set(blocked_wallets),
                    address_classifications=self.address_classifications,
                    service_connections={sc['address']: sc.get('service_name', 'Exchange') 
                                       for sc in service_connections}
                ) if self.graph_algorithms else [],
                'blocked_wallets': [
                    {
                        'address': addr,
                        'risk_score': blacklist_results.get(addr, {}).get('risk_score', 0),
                        'fraud_transaction': blacklist_results.get(addr, {}).get('has_fraud_transaction', False),
                        'classification': wallet_ratings.get(addr, {}).get('classification', 'unknown')
                    }
                    for addr in blocked_wallets
                ],
                'service_connections': service_connections,
                'wallet_ratings': {addr: rating for addr, rating in list(wallet_ratings.items())[:20]}
            }
        }
    
    def _classify_address(self, address: str):
        """Classify an address using feature extraction"""
        try:
            # Get transactions for this address
            transactions = self.api.get_all_usdt_transactions(
                address, 
                direction='both',
                max_transactions=200
            )
            
            # Extract features
            features = self.feature_extractor.extract_features(address, transactions)
            
            # Classify
            classification, confidence = self.feature_extractor.classify_address(features)
            
            # Get importance score
            importance = self.importance_scores.get(address, 0.0)
            
            self.address_classifications[address] = {
                'type': classification,
                'confidence': confidence,
                'importance_score': importance,
                'features': features
            }
        except Exception as e:
            print(f"Error classifying address {address}: {e}")
            self.address_classifications[address] = {
                'type': 'unknown',
                'confidence': 0.0,
                'importance_score': 0.0
            }
    
    def analyze_path_enhanced(self, path: List[str]) -> Dict:
        """
        Enhanced path analysis with SlowMist metrics and advanced risk scoring
        
        Args:
            path: List of addresses forming the path
            
        Returns:
            Dictionary with enhanced path analysis
        """
        # Get basic path analysis (includes enhanced risk scoring if enabled)
        path_info = self.analyze_path(path)
        if not path_info:
            return None
        
        # Add SlowMist enhancements
        path_classifications = []
        path_importance = []
        
        for addr in path:
            # Get or compute classification
            if addr not in self.address_classifications:
                self._classify_address(addr)
            
            classification = self.address_classifications.get(addr, {})
            path_classifications.append({
                'address': addr,
                'type': classification.get('type', 'unknown'),
                'confidence': classification.get('confidence', 0.0),
                'importance': classification.get('importance_score', 0.0)
            })
            path_importance.append(classification.get('importance_score', 0.0))
        
        # Calculate path metrics
        avg_importance = sum(path_importance) / len(path_importance) if path_importance else 0
        hot_wallet_count = sum(1 for c in path_classifications if c['type'] == 'hot')
        cold_wallet_count = sum(1 for c in path_classifications if c['type'] == 'cold')
        
        # Enhanced risk scoring already handles hot wallet risk in risk_scorer.py
        # But we can add additional SlowMist-specific risk adjustments here
        if self.risk_scorer:
            # The risk_scorer already calculated comprehensive risk
            # We can add SlowMist-specific adjustments
            slowmist_risk_adjustment = 0.0
            
            # High importance paths might indicate key infrastructure
            if avg_importance > 0.001:
                # Very important addresses might be exchanges or critical infrastructure
                # This is usually neutral or slightly positive
                pass
            
            # Mixed wallet types might indicate complex routing
            if len(set(c['type'] for c in path_classifications)) > 2:
                slowmist_risk_adjustment += 3.0  # Small penalty for complexity
            
            # Update risk score if needed (risk_scorer already set it)
            if slowmist_risk_adjustment > 0 and 'risk_breakdown' in path_info:
                path_info['risk_score'] = min(100.0, path_info['risk_score'] + slowmist_risk_adjustment)
                path_info['risk_breakdown']['slowmist_complexity'] = slowmist_risk_adjustment
        
        # Add SlowMist data
        path_info['slowmist_metrics'] = {
            'address_classifications': path_classifications,
            'average_importance': avg_importance,
            'hot_wallet_count': hot_wallet_count,
            'cold_wallet_count': cold_wallet_count,
            'path_risk_indicators': {
                'contains_hot_wallets': hot_wallet_count > 0,
                'high_importance_path': avg_importance > 0.001,
                'mixed_types': len(set(c['type'] for c in path_classifications)) > 1
            }
        }
        
        return path_info

