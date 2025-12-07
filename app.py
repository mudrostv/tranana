"""
Flask web application for Tron wallet connection analysis
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from wallet_analyzer import WalletAnalyzer
from slowmist_analyzer import SlowMistEnhancedAnalyzer
from tron_api import TronAPI
from config import Config

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for API endpoints

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_connections():
    """API endpoint for analyzing wallet connections"""
    try:
        data = request.json
        source_address = data.get('source_address', '').strip()
        target_address = data.get('target_address', '').strip()
        
        if not source_address or not target_address:
            return jsonify({
                'error': 'Both source_address and target_address are required'
            }), 400
        
        # Validate Tron address format (should start with T and be 34 chars)
        if not (source_address.startswith('T') and len(source_address) == 34):
            return jsonify({'error': 'Invalid source address format'}), 400
        
        if not (target_address.startswith('T') and len(target_address) == 34):
            return jsonify({'error': 'Invalid target address format'}), 400
        
        # Get max_depth from request (default to 2 if not provided)
        max_depth = data.get('max_depth', 2)
        try:
            max_depth = int(max_depth)
            if max_depth < 1 or max_depth > 5:
                return jsonify({'error': 'max_depth must be between 1 and 5'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'max_depth must be an integer between 1 and 5'}), 400
        
        # Use enhanced SlowMist analyzer for comprehensive analysis
        analyzer = SlowMistEnhancedAnalyzer()
        
        # Override max_depth for this analysis
        analyzer.max_depth = max_depth
        
        # Perform analysis (timeout varies by depth: 5-60 minutes)
        import time
        import sys
        start_time = time.time()
        
        print(f"Starting analysis with max_depth={max_depth}")
        sys.stdout.flush()
        
        try:
            results = analyzer.analyze_connections(source_address, target_address)
            elapsed_time = time.time() - start_time
            
            # Add timing information
            results['analysis_time_seconds'] = round(elapsed_time, 2)
            results['analysis_time_minutes'] = round(elapsed_time / 60, 2)
            
            return jsonify(results)
        except KeyboardInterrupt:
            return jsonify({'error': 'Analysis was interrupted'}), 500
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"Analysis failed after {elapsed_time:.2f} seconds: {e}")
            raise
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in analyze_connections: {error_details}")
        return jsonify({'error': str(e), 'details': error_details}), 500

@app.route('/api/check-blacklist', methods=['POST'])
def check_blacklist():
    """Check if an address is blacklisted"""
    try:
        data = request.json
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        
        api = TronAPI()
        result = api.check_blacklist_status(address)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/address-info', methods=['POST'])
def address_info():
    """Get basic information about an address"""
    try:
        data = request.json
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        
        api = TronAPI()
        account_info = api.get_account_info(address)
        blacklist_info = api.check_blacklist_status(address)
        
        return jsonify({
            'address': address,
            'account_info': account_info,
            'blacklist_status': blacklist_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5001)

