"""
Decision Engine Evaluator Module
Implements the Weighted Sum Model (WSM) for multi-criteria decision analysis.
"""


def normalize_weights(weights):
    """
    Normalize weights so they sum to 1.
    
    Args:
        weights (list): List of numeric weights
    
    Returns:
        list: Normalized weights summing to 1.0
    """
    total = sum(weights)
    if total == 0:
        # Fallback: equal weights
        return [1.0 / len(weights) for _ in weights]
    return [w / total for w in weights]


def normalize_scores(scores, criterion_type):
    """
    Normalize scores to 0-1 range based on criterion type.
    
    Args:
        scores (list): List of numeric scores for a criterion
        criterion_type (str): 'max' (higher is better) or 'min' (lower is better)
    
    Returns:
        list: Normalized scores
    """
    min_score = min(scores)
    max_score = max(scores)
    
    # Handle edge case where all scores are the same
    if min_score == max_score:
        return [1.0] * len(scores)
    
    score_range = max_score - min_score
    
    if criterion_type == 'max':
        # Higher scores are better: normalize to (score - min) / range
        normalized = [(score - min_score) / score_range for score in scores]
    else:  # criterion_type == 'min'
        # Lower scores are better: normalize to (max - score) / range
        normalized = [(max_score - score) / score_range for score in scores]
    
    return normalized


def calculate_weighted_scores(options, criteria, normalized_weights, criterion_types, scores):
    """
    Calculate weighted scores for each option using WSM.
    
    Args:
        options (list): List of option names
        criteria (list): List of criterion names
        normalized_weights (list): Normalized weights (sum to 1)
        criterion_types (list): Type for each criterion ('max' or 'min')
        scores (dict): Scores per option per criterion
    
    Returns:
        dict: Dictionary with option names as keys and total weighted scores as values
    """
    weighted_scores = {}
    
    for option in options:
        total_score = 0.0
        option_scores_list = scores[option]
        
        # For each criterion, calculate normalized score and apply weight
        for criterion_idx, criterion in enumerate(criteria):
            criterion_scores = [scores[opt][criterion_idx] for opt in options]
            normalized_criterion_scores = normalize_scores(criterion_scores, criterion_types[criterion_idx])
            
            # Get this option's normalized score for this criterion
            option_norm_score = normalized_criterion_scores[option_scores_list.index(option_scores_list[criterion_idx])]
            
            # Apply weight
            weighted_contrib = normalized_weights[criterion_idx] * option_norm_score
            total_score += weighted_contrib
        
        weighted_scores[option] = total_score
    
    return weighted_scores


def evaluate_options(data):
    """
    Main evaluation function using Weighted Sum Model.
    
    Args:
        data (dict): Validated input with:
            - options (list)
            - criteria (list)
            - weights (list)
            - criterion_types (list)
            - scores (dict)
    
    Returns:
        dict: Result containing:
            - ranked_options (list): Options sorted by score (best first)
            - scores (dict): Total score for each option
            - details (dict): Detailed breakdown per option
    """
    options = data['options']
    criteria = data['criteria']
    weights = [float(w) for w in data['weights']]
    criterion_types = data['criterion_types']
    scores = {opt: [float(s) for s in data['scores'][opt]] for opt in options}
    
    # Step 1: Normalize weights
    normalized_weights = normalize_weights(weights)
    
    # Step 2: Calculate weighted scores
    weighted_scores = calculate_weighted_scores(
        options, criteria, normalized_weights, criterion_types, scores
    )
    
    # Step 3: Rank options
    ranked_options = sorted(options, key=lambda opt: weighted_scores[opt], reverse=True)
    
    # Step 4: Build details for explanation
    details = _build_evaluation_details(
        options, criteria, normalized_weights, criterion_types, scores, weighted_scores
    )
    
    return {
        'ranked_options': ranked_options,
        'scores': weighted_scores,
        'details': details,
        'weights': {crit: weight for crit, weight in zip(criteria, normalized_weights)}
    }


def _build_evaluation_details(options, criteria, normalized_weights, criterion_types, scores, weighted_scores):
    """
    Build detailed breakdown of evaluation for each option.
    
    Args:
        options (list): Option names
        criteria (list): Criterion names
        normalized_weights (list): Normalized weights
        criterion_types (list): Criterion types
        scores (dict): Input scores
        weighted_scores (dict): Calculated weighted scores
    
    Returns:
        dict: Detailed breakdown per option
    """
    details = {}
    
    for option in options:
        criteria_breakdown = []
        total = 0.0
        
        for criterion_idx, criterion in enumerate(criteria):
            criterion_scores = [scores[opt][criterion_idx] for opt in options]
            normalized_criterion_scores = normalize_scores(
                criterion_scores, criterion_types[criterion_idx]
            )
            
            # Find normalized score for this option
            option_score = scores[option][criterion_idx]
            option_position = options.index(option)
            option_norm_score = normalized_criterion_scores[option_position]
            
            weighted_contrib = normalized_weights[criterion_idx] * option_norm_score
            total += weighted_contrib
            
            criteria_breakdown.append({
                'criterion': criterion,
                'raw_score': option_score,
                'normalized_score': round(option_norm_score, 4),
                'weight': round(normalized_weights[criterion_idx], 4),
                'contribution': round(weighted_contrib, 4)
            })
        
        details[option] = {
            'criteria_breakdown': criteria_breakdown,
            'total_score': round(weighted_scores[option], 4)
        }
    
    return details
