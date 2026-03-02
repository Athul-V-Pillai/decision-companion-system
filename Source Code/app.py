"""
Decision Companion System - Flask Backend
A web-based decision support system using Weighted Sum Model (WSM).
"""

from flask import Flask, render_template, request, jsonify, send_file
from decision_engine import validate_input, evaluate_options, explain_decision, HistoryManager
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from io import BytesIO
import traceback
import os
from datetime import datetime

# Initialize history manager
history_manager = HistoryManager('data/decision_history.json')

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
        
        # Save to history
        history_manager.save_decision(data, evaluation_result)
        
        # Return success response
        return jsonify({
            'success': True,
            'data': {
                'ranked_options': evaluation_result['ranked_options'],
                'scores': evaluation_result['scores'],
                'details': evaluation_result['details'],
                'weights': evaluation_result['weights'],
                'confidence': evaluation_result['confidence'],
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


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Retrieve decision history.
    
    Query Parameters:
        limit (int): Maximum number of records to return
        id (int): Get specific record by ID
    
    Returns:
        JSON with history records
    """
    try:
        # Get specific record by ID if requested
        record_id = request.args.get('id', type=int)
        if record_id:
            record = history_manager.get_history_by_id(record_id)
            if record:
                return jsonify({'success': True, 'data': record}), 200
            else:
                return jsonify({'success': False, 'error': f'Record {record_id} not found'}), 404
        
        # Get all history with optional limit
        limit = request.args.get('limit', type=int)
        history = history_manager.get_all_history(limit)
        
        return jsonify({'success': True, 'data': history}), 200
    
    except Exception as e:
        print(f"Error in /api/history: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to retrieve history'}), 500


@app.route('/api/history/stats', methods=['GET'])
def get_history_stats():
    """
    Get statistics about decision history.
    
    Returns:
        JSON with statistics (total decisions, most recommended, etc.)
    """
    try:
        stats = history_manager.get_statistics()
        return jsonify({'success': True, 'data': stats}), 200
    except Exception as e:
        print(f"Error in /api/history/stats: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to retrieve statistics'}), 500


@app.route('/api/history/<int:record_id>', methods=['DELETE'])
def delete_history_record(record_id):
    """
    Delete a specific history record.
    
    Args:
        record_id (int): ID of record to delete
    
    Returns:
        JSON response
    """
    try:
        if history_manager.delete_history(record_id):
            return jsonify({'success': True, 'message': f'Record {record_id} deleted'}), 200
        else:
            return jsonify({'success': False, 'error': f'Record {record_id} not found'}), 404
    except Exception as e:
        print(f"Error in DELETE /api/history: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to delete history'}), 500


@app.route('/api/export-report', methods=['POST'])
def export_report():
    """
    Generate and export a PDF report of the decision analysis.
    
    Expected JSON input:
    {
        "title": "Decision Report",
        "criteria": ["Criterion 1", ...],
        "options": ["Option A", ...],
        "scores": {"Option A": score1, ...},
        "ranked_options": ["Option A", ...],
        "details": {...},
        "confidence": {...},
        "explanation": {...}
    }
    
    Returns:
        PDF file for download
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Request body must be valid JSON'}), 400
        
        # Generate PDF in memory
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=12,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=8,
            spaceBefore=8
        )
        
        # Title
        title = data.get('title', 'Decision Analysis Report')
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Metadata
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elements.append(Paragraph(f'<b>Generated:</b> {timestamp}', styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Criteria Table
        elements.append(Paragraph('Criteria & Weights', heading_style))
        criteria = data.get('criteria', [])
        weights = data.get('weights', {})
        
        criteria_data = [['Criterion', 'Weight']]
        for criterion in criteria:
            weight = weights.get(criterion, 'N/A')
            if isinstance(weight, float):
                weight = f'{weight:.4f}'
            criteria_data.append([criterion, str(weight)])
        
        criteria_table = Table(criteria_data, colWidths=[3.5*inch, 1.5*inch])
        criteria_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
        ]))
        
        elements.append(criteria_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Options Scores Table
        elements.append(Paragraph('Options & Scores', heading_style))
        options = data.get('options', [])
        scores = data.get('scores', {})
        ranked_options = data.get('ranked_options', [])
        
        scores_data = [['Rank', 'Option', 'Score']]
        for rank, option in enumerate(ranked_options, 1):
            score = scores.get(option, 'N/A')
            if isinstance(score, float):
                score = f'{score:.4f}'
            scores_data.append([str(rank), option, str(score)])
        
        scores_table = Table(scores_data, colWidths=[1*inch, 2.5*inch, 2*inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
        ]))
        
        elements.append(scores_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Confidence Section
        elements.append(Paragraph('Decision Confidence', heading_style))
        confidence = data.get('confidence', {})
        conf_level = confidence.get('level', 'Unknown')
        conf_score = confidence.get('score', 'N/A')
        if isinstance(conf_score, float):
            conf_score = f'{conf_score:.4f}'
        
        elements.append(Paragraph(
            f'<b>Level:</b> {conf_level}<br/><b>Score:</b> {conf_score}<br/><b>Interpretation:</b> {confidence.get("interpretation", "N/A")}',
            styles['Normal']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Explanation
        explanation = data.get('explanation', {})
        if explanation.get('recommendation'):
            elements.append(Paragraph('Recommendation', heading_style))
            elements.append(Paragraph(explanation.get('recommendation', ''), styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(elements)
        
        # Prepare response
        pdf_buffer.seek(0)
        filename = f"decision_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        print(f"Error in /api/export-report: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': 'Failed to generate PDF report'}), 500


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
