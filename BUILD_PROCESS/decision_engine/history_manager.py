"""
Decision History Manager Module
Persists decision analysis results to local JSON file.
"""

import json
import os
from datetime import datetime
from pathlib import Path


class HistoryManager:
    """Manages persistent storage of decision history."""
    
    def __init__(self, history_file='data/decision_history.json'):
        """
        Initialize history manager.
        
        Args:
            history_file (str): Path to JSON file for storing history
        """
        self.history_file = history_file
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure data directory exists."""
        directory = os.path.dirname(self.history_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    
    def _load_history(self):
        """Load history from JSON file. Returns empty list if file doesn't exist."""
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_history(self, history):
        """Save history to JSON file."""
        self._ensure_directory()
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def save_decision(self, input_data, result):
        """
        Save a decision analysis record.
        
        Args:
            input_data (dict): Original input (options, criteria, weights, scores, etc.)
            result (dict): Evaluation result (ranked_options, scores, confidence, etc.)
        
        Returns:
            dict: Saved record with timestamp and ID
        """
        history = self._load_history()
        
        # Create record
        record = {
            'id': len(history) + 1,
            'timestamp': datetime.now().isoformat(),
            'input': {
                'options': input_data.get('options', []),
                'criteria': input_data.get('criteria', []),
                'weights': input_data.get('weights', []),
                'criterion_types': input_data.get('criterion_types', []),
                'scores': input_data.get('scores', {})
            },
            'result': {
                'ranked_options': result.get('ranked_options', []),
                'scores': {opt: float(score) for opt, score in result.get('scores', {}).items()},
                'confidence': result.get('confidence', {}),
                'weights': result.get('weights', {})
            }
        }
        
        history.append(record)
        self._save_history(history)
        
        return record
    
    def get_all_history(self, limit=None):
        """
        Retrieve all decision records.
        
        Args:
            limit (int): Maximum number of records to return (None = all)
        
        Returns:
            list: List of decision records, newest first
        """
        history = self._load_history()
        # Sort by timestamp, newest first
        history.sort(key=lambda x: x['timestamp'], reverse=True)
        
        if limit:
            return history[:limit]
        return history
    
    def get_history_by_id(self, record_id):
        """
        Retrieve a specific decision record by ID.
        
        Args:
            record_id (int): ID of the record to retrieve
        
        Returns:
            dict: Decision record or None if not found
        """
        history = self._load_history()
        for record in history:
            if record['id'] == record_id:
                return record
        return None
    
    def delete_history(self, record_id=None):
        """
        Delete a specific record or all history.
        
        Args:
            record_id (int): ID to delete; if None, deletes all records
        
        Returns:
            bool: True if deletion was successful
        """
        if record_id is None:
            # Delete all
            self._save_history([])
            return True
        
        history = self._load_history()
        original_length = len(history)
        history = [record for record in history if record['id'] != record_id]
        
        if len(history) < original_length:
            # Re-index IDs after deletion
            for idx, record in enumerate(history, 1):
                record['id'] = idx
            self._save_history(history)
            return True
        
        return False
    
    def get_statistics(self):
        """
        Get statistics about decision history.
        
        Returns:
            dict: Statistics including total decisions, most common options, etc.
        """
        history = self._load_history()
        
        if not history:
            return {
                'total_decisions': 0,
                'most_recommended_option': None,
                'average_confidence_score': None
            }
        
        # Count option recommendations
        option_counts = {}
        confidence_scores = []
        
        for record in history:
            ranked = record['result'].get('ranked_options', [])
            if ranked:
                top_option = ranked[0]
                option_counts[top_option] = option_counts.get(top_option, 0) + 1
            
            confidence = record['result'].get('confidence', {})
            if confidence and 'score' in confidence:
                confidence_scores.append(confidence['score'])
        
        most_recommended = max(option_counts, key=option_counts.get) if option_counts else None
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else None
        
        return {
            'total_decisions': len(history),
            'most_recommended_option': most_recommended,
            'most_recommended_count': option_counts.get(most_recommended, 0) if most_recommended else 0,
            'average_confidence_score': round(avg_confidence, 4) if avg_confidence else None
        }
