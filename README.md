# 🔗 TRON USDT Wallet Connection Analyzer

<div align="center">

**A powerful deep-chain analysis tool for tracing hidden connections between USDT wallets on the Tron blockchain**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Made for MAGIC with love by no self labs**

</div>

---

## 📜 Manifest: On Privacy, Connections, and the Illusion of Anonymity

Welcome, digital wanderer, to a place where blockchain addresses reveal their hidden geometry, where the invisible threads connecting one wallet to another emerge from the void like constellations in the night sky of distributed ledgers.

In this age of cryptographic promises and privacy theater, we stand at a peculiar intersection. The blockchain presents itself as a monument to transparency—every transaction inscribed forever in the immutable stone of distributed consensus. Yet within this apparent openness, connections hide in plain sight, obscured not by encryption but by the sheer complexity of the network itself. Addresses whisper to each other through intermediaries, like messages passed in a digital game of telephone, leaving traces that exist but remain unseen to the casual observer.

**Privacy is not a feature—it is a fundamental right.** We build this tool not to violate that right, but to illuminate the reality of connection itself. For in understanding how wallets relate to one another, we understand the topology of trust, the architecture of financial flows, and ultimately, the hidden structures that govern our digital existence. The blockchain remembers everything; we merely help you read what it has already written.

This tool traces connections between USDT wallets on the Tron network—not just the obvious, direct paths, but the serpentine routes that wind through multiple intermediaries. What appears as isolated islands of activity reveals itself, upon deeper examination, as an archipelago of relationships. Behind every address, there are patterns. Behind every pattern, there are connections. Behind every connection, there is a story waiting to be discovered.

**We are researchers, not surveillance agents.** This project exists in a state of perpetual becoming—a continuous exploration at the frontier where graph theory meets financial forensics, where machine learning algorithms dance with network analysis, where the abstract mathematics of PageRank and community detection collide with the concrete reality of blockchain transactions. Development is ongoing. The algorithms evolve. The models learn. Nothing is final, everything is experimental.

And a word on the methodology: **this codebase was vibe-coded.** It emerged not from corporate requirement documents or sterile development sprints, but from that mysterious zone where intuition meets implementation, where the logical and the lyrical intersect. The code you see here was written in that particular state of flow where the boundaries between problem and solution dissolve, where the tool becomes an extension of thought itself. It may not follow every best practice. It may have quirks. It may surprise you. But it works, and it works with a certain elegance that comes from being shaped by the process rather than prescribed by it.

Use this tool responsibly. Use it to understand, not to harm. Use it for compliance, for research, for forensics, for the noble pursuit of truth in a world increasingly constructed from layers of abstraction. The blockchain does not judge; it only records. The interpretation—and the responsibility for that interpretation—rests entirely with you.

Welcome to the connection analyzer. Welcome to the ongoing experiment. Welcome to the space where wallets reveal their secrets.

---

<div align="center">

*"In the network, all paths are one path. In the blockchain, all transactions are one transaction. The illusion of separation is merely the resolution of our perception."*

</div>

---

## 🎯 Overview

TRON USDT Wallet Connection Analyzer is an advanced blockchain forensics tool that performs deep-chain analysis to discover hidden transaction paths between two USDT (TRC20) wallets on the Tron network. Unlike basic blockchain explorers that only show direct connections, this tool traces multi-hop relationships through intermediate wallets, revealing complex money flows and uncovering potentially obfuscated transaction patterns.

### Key Capabilities

- **🔍 Multi-Level Path Discovery**: Traces connections up to 5 hops deep through intermediate wallets
- **🧠 ML-Powered Address Classification**: Leverages SlowMist's machine learning models to classify wallets (Hot/Cold/Common)
- **📊 Advanced Risk Scoring**: 14-component comprehensive risk assessment system
- **🌐 Graph Analysis**: PageRank, K-Core, and Label Propagation algorithms for network insights
- **🎨 Interactive Visualization**: Cyberpunk-themed UI with Cytoscape.js graph visualization
- **⚡ Optimized Algorithms**: Bidirectional BFS with early termination and smart pruning
- **🏦 Exchange Detection**: Automatically identifies known exchange hot wallets
- **🚫 Blacklist Integration**: Real-time sanctions and blacklist checking via TronScan API
- **👥 Community Detection**: Discovers wallet communities and their characteristics

---

## ✨ Features

### 🔎 Deep Chain Analysis
- **Bidirectional Search**: Efficiently explores from both source and target wallets
- **Configurable Depth**: Choose analysis depth from 1 to 5 hops (1 hop = direct, 5 hops = very deep)
- **Smart Pruning**: Automatically skips high-connectivity nodes (exchanges/mixers) to improve performance
- **Early Termination**: Stops searching once paths are found, with configurable limits

### 🧠 SlowMist Integration
- **Address Classification**: ML-based classification into Hot, Cold, or Common wallet types
- **PageRank Analysis**: Identifies the most important addresses in the transaction network
- **K-Core Detection**: Finds tightly-knit communities of addresses
- **Label Propagation**: Discovers wallet communities automatically
- **Intelligent Naming**: Communities are automatically named based on their characteristics (e.g., "Binance Community", "Blocked Addresses")

### 🎯 Comprehensive Risk Scoring
The risk scoring system evaluates 14 different risk factors:

1. **Blacklist/Sanctions** (50 points): Addresses on OFAC or other sanction lists
2. **Mixer/Tumbler Detection** (40 points): Patterns consistent with mixing services
3. **Known Scam Addresses** (35 points): Addresses associated with fraud
4. **Unregulated Exchanges** (30 points): Connections to unregulated platforms
5. **Velocity Anomalies** (25 points): Unusual transaction frequency patterns
6. **Structuring Patterns** (22 points): Potential money laundering patterns
7. **High Connectivity** (18 points): Addresses with excessive connections (potential mixer/service)
8. **Path Complexity** (15 points): Layering through multiple hops (6+)
9. **Volume Anomalies** (12 points): Unusual transaction amounts
10. **Time Anomalies** (10 points): Suspicious timing patterns
11. **Exchange Risk** (8 points): Connection to known exchanges
12. **Hot Wallet Classification** (5 points): Active trading wallets
13. **Community Risk** (7 points): Membership in high-risk communities

**Risk Levels:**
- **Critical** (70-100): Immediate action required
- **High** (50-69): Significant risk factors present
- **Medium** (30-49): Moderate risk indicators
- **Low-Medium** (15-29): Minor concerns
- **Low** (0-14): Minimal risk

### 📈 Interactive Visualization
- **Cytoscape.js Integration**: Professional network graph visualization
- **DAGRE Layout**: Hierarchical layout showing transaction flow direction
- **Clickable Elements**: 
  - Nodes link to TronScan wallet pages
  - Edges link to transaction pages (or show modal for multiple transactions)
- **Visual Indicators**:
  - ⚡ Source wallet (black star with cyan border)
  - ◎ Target wallet (white star with black border)
  - ⚠ Blacklisted addresses (dark hexagon with magenta border)
  - ◊ Exchange addresses (purple diamond)
  - Regular wallets (gray ellipses)
- **Edge Labels**: Transaction amounts displayed on connections

### 🎨 Cyberpunk ASCII UI
- **Terminal Aesthetic**: Monospace font with ASCII art header
- **Dark Theme**: Black background with cyan accents
- **Glowing Effects**: Text shadows and borders for cyberpunk feel
- **Responsive Design**: Works on all screen sizes

### ⚙️ Advanced Configuration
- **Dynamic Timeouts**: Analysis timeouts adjust based on selected depth:
  - Depth 1: 5 minutes
  - Depth 2: 15 minutes
  - Depth 3: 20 minutes
  - Depth 4: 40 minutes
  - Depth 5: 60 minutes
- **Configurable Limits**: All search parameters are tunable in `config.py`
- **Progress Tracking**: Real-time progress updates during analysis

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- TronGrid API key ([Get one here](https://www.trongrid.io/))
- TronScan API key (optional, for enhanced blacklist checking)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/tron-wallet-analyzer.git
cd tron-wallet-analyzer
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your API keys:
# TRONGRID_API_KEY=your_key_here
# TRONSCAN_API_KEY=your_key_here (optional)
```

5. **Run the application:**
```bash
# Option 1: Use the start script
./start.sh

# Option 2: Run directly
python app.py
```

6. **Access the web interface:**
```
http://localhost:5001
```

---

## 📖 Usage Guide

### Basic Analysis

1. **Enter Wallet Addresses:**
   - Source Wallet: Starting address to trace from
   - Target Wallet: Destination address to find connections to
   - Addresses must:
     - Start with 'T'
     - Be exactly 34 characters long
     - Example: `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`

2. **Select Analysis Depth:**
   - Choose 1-5 hops based on how deep you want to search
   - Higher depth = more thorough but slower analysis

3. **Click "Analyze Connections"** and wait for results

4. **Review Results:**
   - **Overview Tab**: Summary statistics, wallet ratings, risk scores, communities
   - **Paths Tab**: Detailed breakdown of all discovered connection paths
   - **Graph Tab**: Interactive network visualization

### Understanding Results

#### Overview Tab
- **Analysis Summary**: Total paths found, wallets analyzed, transactions processed
- **Shortest Path**: Most direct connection with full details
- **Wallet Ratings**: 0-100 scores for source and target wallets
- **Blocked Wallets**: Highlighted if any blacklisted addresses found
- **Service Connections**: Exchange addresses detected in paths
- **Top Important Addresses**: PageRank-sorted list of key wallets
- **Detected Communities**: Wallet clusters with intelligent naming

#### Paths Tab
- **Multiple Paths**: All discovered connection routes
- **Risk Breakdown**: Detailed risk factor analysis per path
- **Transaction Links**: Direct links to TronScan for each transaction
- **Path Details**: Hops count, total amount, transaction count

#### Graph Tab
- **Interactive Network**: Click nodes to view on TronScan
- **Click Edges**: View transactions (modal if multiple transactions)
- **Visual Clarity**: Color-coded by wallet type and risk level

---

## 🏗️ Architecture

### Core Components

```
tron-wallet-analyzer/
├── app.py                      # Flask web application
├── wallet_analyzer.py          # Core graph building and path finding
├── slowmist_analyzer.py        # ML and graph algorithm integration
├── risk_scorer.py              # Comprehensive risk assessment
├── tron_api.py                 # TronGrid/TronScan API wrapper
├── config.py                   # Configuration management
├── slowmist_features.py        # Feature extraction for ML
├── slowmist_graph_algorithms.py # PageRank, K-Core, Label Propagation
├── exchange_addresses.py       # Known exchange wallet database
└── templates/
    └── index.html             # Frontend UI (cyberpunk theme)
```

### Algorithm Flow

1. **Graph Construction**: 
   - Fetches USDT transactions via TronGrid API
   - Builds directed graph (nodes = addresses, edges = transactions)
   - Applies limits to prevent unbounded exploration

2. **Path Discovery**:
   - Bidirectional BFS from source and target
   - Early exchange detection for fast paths
   - Amount filtering to focus on significant transactions
   - High-connectivity node pruning

3. **Analysis**:
   - SlowMist feature extraction and classification
   - PageRank computation for importance scores
   - Community detection via Label Propagation
   - Risk scoring for all paths

4. **Visualization**:
   - Cytoscape.js graph rendering
   - Interactive node/edge interactions
   - Transaction link integration

---

## ⚙️ Configuration

Edit `config.py` to customize analysis parameters:

```python
MAX_DEPTH = 2                      # Maximum search depth (default: 2)
MAX_ADDRESSES_TO_EXPLORE = 200     # Limit total addresses explored
MAX_CONNECTIONS_PER_ADDRESS = 30   # Limit connections per address
MAX_NEIGHBORS_TO_EXPAND = 30       # Neighbors to expand at each level
MIN_TRANSACTION_AMOUNT = 10.0      # Minimum USDT amount to consider
MAX_NODE_CONNECTIONS = 500         # Prune nodes exceeding this
```

---

## 🔌 API Endpoints

### POST /api/analyze
Analyze connections between two addresses

**Request:**
```json
{
  "source_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
  "target_address": "TYBUGtKhc8XKfLM2voacubZUVuPHEY7tVW",
  "max_depth": 2
}
```

**Response:**
```json
{
  "source": "...",
  "target": "...",
  "total_paths_found": 5,
  "paths": [...],
  "graph_statistics": {...},
  "slowmist_analysis": {...},
  "analysis_time_seconds": 45.23
}
```

### GET /api/progress/<analysis_id>
Get real-time analysis progress

### POST /api/check-blacklist
Check if an address is blacklisted

### POST /api/address-info
Get account information for an address

---

## 📊 Performance

### Analysis Times (Approximate)
- **Depth 1** (Direct connections): 30 seconds - 2 minutes
- **Depth 2** (1 intermediate): 2-15 minutes
- **Depth 3** (2 intermediates): 5-20 minutes
- **Depth 4** (3 intermediates): 15-40 minutes
- **Depth 5** (4 intermediates): 30-60 minutes

*Times vary significantly based on wallet transaction history and network size*

### Optimizations
- Bidirectional BFS reduces search space exponentially
- Early termination when paths found
- High-connectivity node pruning
- Transaction amount filtering
- Configurable limits prevent runaway processing

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core language
- **Flask**: Web framework
- **NetworkX**: Graph algorithms and operations
- **Requests**: HTTP client for API calls
- **python-dotenv**: Environment variable management

### Frontend
- **Cytoscape.js**: Network graph visualization
- **DAGRE**: Hierarchical graph layout
- **Vanilla JavaScript**: No framework dependencies
- **Cyberpunk CSS**: Custom styling

### APIs
- **TronGrid API**: Transaction data retrieval
- **TronScan API**: Blacklist checking and address info

### ML/Analytics (Inspired by SlowMist)
- **PageRank**: Importance scoring
- **K-Core**: Community structure analysis
- **Label Propagation**: Community detection
- **Feature Extraction**: Transaction pattern analysis

---

## 📝 Example Use Cases

1. **Compliance & AML**: Trace fund flows to identify potential money laundering
2. **Forensics**: Investigate stolen funds or scam operations
3. **Exchange Security**: Verify customer funds and detect suspicious patterns
4. **Research**: Study transaction network topology and community structures
5. **Risk Assessment**: Evaluate wallet connections before transactions

---

## 🧪 Testing

```bash
# Run basic tests
python test_simple.py

# Test with specific wallet addresses
python test_wallets.py
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **SlowMist**: Inspiration for ML-based address classification and graph algorithms
- **TronGrid**: Transaction data API
- **TronScan**: Blacklist and address information API
- **NetworkX**: Powerful graph analysis library
- **Cytoscape.js**: Excellent graph visualization framework

---

## ⚠️ Disclaimer

This tool is for **legitimate research, compliance, and security purposes only**. Users are responsible for ensuring their use complies with applicable laws and regulations. The authors are not responsible for any misuse of this software.

---

## 📧 Contact

**Made for MAGIC with love by no self labs**

For questions, issues, or contributions, please open an issue on GitHub.

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

</div>
