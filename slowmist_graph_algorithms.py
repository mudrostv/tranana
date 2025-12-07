"""
SlowMist-inspired graph algorithms for address analysis
Adapted from SlowMist's automatic-tron-address-clustering
Implements PageRank, KCore, and Label Propagation using NetworkX
"""
import networkx as nx
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class SlowMistGraphAlgorithms:
    """
    Graph algorithms for address clustering and importance analysis
    Based on SlowMist's approach but adapted for NetworkX
    """
    
    def __init__(self, graph: nx.DiGraph):
        """
        Initialize with a directed graph
        
        Args:
            graph: NetworkX directed graph with addresses as nodes
        """
        self.graph = graph
        self.pagerank_scores = None
        self.kcore_scores = None
        self.communities = None
    
    def compute_pagerank(self, max_iter: int = 15, damping: float = 0.85) -> Dict[str, float]:
        """
        Compute PageRank scores to identify important/key addresses
        Based on SlowMist's PageRank implementation
        
        Args:
            max_iter: Maximum iterations
            damping: Damping factor (default 0.85)
            
        Returns:
            Dictionary mapping address to PageRank score
        """
        if self.graph.number_of_nodes() == 0:
            return {}
        
        try:
            # Convert to undirected for PageRank if needed, or use directed
            pagerank = nx.pagerank(self.graph, max_iter=max_iter, alpha=damping)
            self.pagerank_scores = pagerank
            return pagerank
        except Exception as e:
            print(f"PageRank computation error: {e}")
            return {}
    
    def compute_kcore(self, k: int = 1) -> Dict[str, int]:
        """
        Compute K-Core decomposition for community discovery
        Identifies addresses with at least k connections
        
        Args:
            k: Minimum degree threshold
            
        Returns:
            Dictionary mapping address to k-core value
        """
        if self.graph.number_of_nodes() == 0:
            return {}
        
        try:
            # Convert to undirected graph for k-core
            undirected = self.graph.to_undirected()
            kcore = nx.k_core(undirected, k=k)
            
            # Calculate k-core values for all nodes
            kcore_scores = {}
            for node in self.graph.nodes():
                if node in kcore:
                    # Find the maximum k such that node is in k-core
                    max_k = k
                    for test_k in range(k, 10):  # Test up to k=10
                        test_core = nx.k_core(undirected, k=test_k)
                        if node in test_core:
                            max_k = test_k
                        else:
                            break
                    kcore_scores[node] = max_k
                else:
                    kcore_scores[node] = 0
            
            self.kcore_scores = kcore_scores
            return kcore_scores
        except Exception as e:
            print(f"K-Core computation error: {e}")
            return {}
    
    def label_propagation(self, known_labels: Dict[str, str] = None, max_iter: int = 20) -> Dict[str, str]:
        """
        Label Propagation Algorithm for community detection
        Propagates known labels to unknown addresses based on graph structure
        
        Args:
            known_labels: Dictionary of address -> label mappings
            max_iter: Maximum iterations
            
        Returns:
            Dictionary mapping address to propagated label
        """
        if self.graph.number_of_nodes() == 0:
            return {}
        
        if known_labels is None:
            known_labels = {}
        
        try:
            # Convert to undirected for label propagation
            undirected = self.graph.to_undirected()
            
            # Use NetworkX's label propagation
            communities = nx.algorithms.community.label_propagation_communities(undirected)
            
            # Create label mapping
            label_map = {}
            for idx, community in enumerate(communities):
                label = f"community_{idx}"
                for node in community:
                    label_map[node] = label
            
            # Override with known labels if provided
            label_map.update(known_labels)
            
            self.communities = label_map
            return label_map
        except Exception as e:
            print(f"Label Propagation error: {e}")
            return {}
    
    def get_community_list(self, 
                          exchange_addresses: Set[str] = None,
                          blacklisted_addresses: Set[str] = None,
                          address_classifications: Dict[str, Dict] = None,
                          service_connections: Dict[str, str] = None) -> List[Dict[str, any]]:
        """
        Get list of communities with their members and intelligent naming
        
        Args:
            exchange_addresses: Set of known exchange addresses
            blacklisted_addresses: Set of blacklisted/blocked addresses
            address_classifications: Dictionary of address -> classification info
            service_connections: Dictionary of address -> service name
            
        Returns:
            List of dictionaries, each containing community info with intelligent naming
        """
        if self.communities is None:
            self.label_propagation()
        
        if not self.communities:
            return []
        
        if exchange_addresses is None:
            exchange_addresses = set()
        if blacklisted_addresses is None:
            blacklisted_addresses = set()
        if address_classifications is None:
            address_classifications = {}
        if service_connections is None:
            service_connections = {}
        
        # Group addresses by community
        community_dict = {}
        for addr, label in self.communities.items():
            if label not in community_dict:
                community_dict[label] = []
            community_dict[label].append(addr)
        
        # Convert to list format with intelligent naming
        community_list = []
        for label, addresses in community_dict.items():
            # Analyze community characteristics
            community_info = self._analyze_community(
                addresses, 
                exchange_addresses,
                blacklisted_addresses,
                address_classifications,
                service_connections
            )
            
            community_list.append({
                'id': label,
                'name': community_info['name'],
                'type': community_info['type'],
                'member_count': len(addresses),
                'addresses': addresses,
                'characteristics': community_info['characteristics'],
                'risk_level': community_info['risk_level']
            })
        
        # Sort by member count (largest first)
        community_list.sort(key=lambda x: x['member_count'], reverse=True)
        
        return community_list
    
    def _analyze_community(self, 
                          addresses: List[str],
                          exchange_addresses: Set[str],
                          blacklisted_addresses: Set[str],
                          address_classifications: Dict[str, Dict],
                          service_connections: Dict[str, str]) -> Dict:
        """
        Analyze a community and assign a meaningful name and type
        
        Returns:
            Dictionary with name, type, characteristics, and risk_level
        """
        exchange_count = sum(1 for addr in addresses if addr in exchange_addresses)
        blacklisted_count = sum(1 for addr in addresses if addr in blacklisted_addresses)
        hot_wallet_count = sum(1 for addr in addresses 
                              if address_classifications.get(addr, {}).get('type') == 'hot')
        cold_wallet_count = sum(1 for addr in addresses 
                               if address_classifications.get(addr, {}).get('type') == 'cold')
        
        total = len(addresses)
        exchange_ratio = exchange_count / total if total > 0 else 0
        blacklisted_ratio = blacklisted_count / total if total > 0 else 0
        
        characteristics = []
        risk_level = 'low'
        community_type = 'unknown'
        name_parts = []
        
        # Check for blocked/bad addresses
        if blacklisted_count > 0:
            risk_level = 'high'
            community_type = 'blocked'
            if blacklisted_count == total:
                name_parts.append('🚫 Blocked Addresses')
            else:
                name_parts.append(f'⚠️ Mixed (Contains {blacklisted_count} Blocked)')
            characteristics.append(f'{blacklisted_count} blocked address(es)')
        
        # Check for exchange addresses
        if exchange_count > 0:
            community_type = 'exchange' if community_type == 'unknown' else community_type
            if exchange_count == total:
                # All members are exchanges
                exchange_names = []
                for addr in addresses:
                    if addr in exchange_addresses:
                        service_name = service_connections.get(addr, 'Exchange')
                        if service_name not in exchange_names:
                            exchange_names.append(service_name)
                
                if len(exchange_names) == 1:
                    name_parts.append(f'🏦 {exchange_names[0]} Community')
                elif len(exchange_names) > 1:
                    name_parts.append(f'🏦 Exchange Community ({", ".join(exchange_names[:2])})')
                else:
                    name_parts.append('🏦 Exchange Community')
            else:
                # Mixed with exchanges
                name_parts.append(f'🏦 Exchange-Related ({exchange_count}/{total} exchanges)')
            
            characteristics.append(f'{exchange_count} exchange address(es)')
        
        # Check for hot wallets (high activity)
        if hot_wallet_count > total * 0.5:  # More than 50% are hot wallets
            if not name_parts:  # Only if no other label yet
                name_parts.append('🔥 High Activity Community')
            community_type = 'hot' if community_type == 'unknown' else community_type
            characteristics.append(f'{hot_wallet_count} hot wallet(s)')
        
        # Check for cold wallets
        if cold_wallet_count > total * 0.5:  # More than 50% are cold wallets
            if not name_parts:  # Only if no other label yet
                name_parts.append('❄️ Low Activity Community')
            community_type = 'cold' if community_type == 'unknown' else community_type
            characteristics.append(f'{cold_wallet_count} cold wallet(s)')
        
        # Default name if no specific characteristics
        if not name_parts:
            if total == 1:
                name_parts.append('👤 Single Address')
            elif total <= 3:
                name_parts.append('👥 Small Community')
            else:
                name_parts.append('👥 Regular Community')
        
        # Set risk level based on characteristics
        if blacklisted_ratio >= 0.5:
            risk_level = 'high'
        elif blacklisted_ratio > 0:
            risk_level = 'medium'
        elif exchange_ratio >= 0.7:
            risk_level = 'low'  # Exchanges are generally safe
        else:
            risk_level = 'low'
        
        return {
            'name': ' | '.join(name_parts) if name_parts else 'Community',
            'type': community_type,
            'characteristics': characteristics,
            'risk_level': risk_level,
            'exchange_count': exchange_count,
            'blacklisted_count': blacklisted_count,
            'hot_wallet_count': hot_wallet_count,
            'cold_wallet_count': cold_wallet_count
        }
    
    def find_key_addresses(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Find top N most important addresses using PageRank
        
        Args:
            top_n: Number of top addresses to return
            
        Returns:
            List of (address, pagerank_score) tuples, sorted by score
        """
        if self.pagerank_scores is None:
            self.compute_pagerank()
        
        if not self.pagerank_scores:
            return []
        
        sorted_addresses = sorted(
            self.pagerank_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_addresses[:top_n]
    
    def get_address_importance(self, address: str) -> float:
        """
        Get PageRank importance score for an address
        
        Args:
            address: Wallet address
            
        Returns:
            PageRank score (0-1)
        """
        if self.pagerank_scores is None:
            self.compute_pagerank()
        
        return self.pagerank_scores.get(address, 0.0)
    
    def get_community_members(self, address: str) -> Set[str]:
        """
        Get all addresses in the same community as the given address
        
        Args:
            address: Wallet address
            
        Returns:
            Set of addresses in the same community
        """
        if self.communities is None:
            self.label_propagation()
        
        if not self.communities:
            return set()
        
        community_label = self.communities.get(address)
        if not community_label:
            return {address}
        
        return {addr for addr, label in self.communities.items() if label == community_label}

