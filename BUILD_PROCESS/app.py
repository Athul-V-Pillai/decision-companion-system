"""
Decision Companion System - Flask Backend
A web-based decision support system using Weighted Sum Model (WSM).
"""

from flask import Flask, render_template, request, jsonify
from decision_engine import validate_input, evaluate_options, explain_decision
import traceback

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """
    Main evaluation endpoint.
    
    Expected JSON input:
    {
        "options": ["Option A", "Option B", ...],
        "criteria": ["Criterion 1", "Criterion 2", ...],
        "weights": [weight1, weight2, ...],
        "criterion_types": ["max", "min", ...],
        "scores": {
            "Option A": [score1, score2, ...],
            "Option B": [score1, score2, ...],
            ...
        }
    }
    
    Returns:
        JSON with ranked_options, scores, explanation, and details
    """
    try:
        # Parse JSON input
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be valid JSON'
            }), 400
        
        # Validate input
        is_valid, error_message = validate_input(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            }), 400
        
        # Evaluate options
        evaluation_result = evaluate_options(data)
        
        # Generate explanation
        explanation = explain_decision(evaluation_result)
        
        # Return success response
        return jsonify({
            'success': True,
            'data': {
                'ranked_options': evaluation_result['ranked_options'],
                'scores': evaluation_result['scores'],
                'details': evaluation_result['details'],
                'weights': evaluation_result['weights'],
                'explanation': explanation
            }
        }), 200
    
    except Exception as e:
        # Log error and return generic error message
        print(f"Error in /api/evaluate: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred during evaluation'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'Decision Companion System'}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405


if __name__ == '__main__':
    # Run the app in debug mode during development
    app.run(debug=True, host='0.0.0.0', port=5000)
