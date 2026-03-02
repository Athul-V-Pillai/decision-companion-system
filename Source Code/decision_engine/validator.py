"""
Input Validation Module
Handles validation of criteria, options, and scores before processing.
"""


def validate_input(data):
    """
    Validate input data for decision evaluation.
    
    Args:
        data (dict): Input dictionary containing:
            - options (list): List of option names
            - criteria (list): List of criterion names
            - weights (list): Weight for each criterion
            - criterion_types (list): Type for each criterion ("max" or "min")
            - scores (dict): Dict mapping options to lists of scores
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    
    # Check required fields
    required_fields = ['options', 'criteria', 'weights', 'criterion_types', 'scores']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    options = data.get('options', [])
    criteria = data.get('criteria', [])
    weights = data.get('weights', [])
    criterion_types = data.get('criterion_types', [])
    scores = data.get('scores', {})
    
    # Validate non-empty lists
    if not options or len(options) == 0:
        return False, "At least one option is required"
    
    if not criteria or len(criteria) == 0:
        return False, "At least one criterion is required"
    
    # Validate length consistency
    if len(criteria) != len(weights):
        return False, f"Number of weights ({len(weights)}) must match number of criteria ({len(criteria)})"
    
    if len(criteria) != len(criterion_types):
        return False, f"Number of criterion_types ({len(criterion_types)}) must match number of criteria ({len(criteria)})"
    
    # Validate weights are numeric and positive
    try:
        weights_float = [float(w) for w in weights]
        if any(w <= 0 for w in weights_float):
            return False, "All weights must be positive numbers"
    except (ValueError, TypeError):
        return False, "Weights must be numeric values"
    
    # Validate criterion types
    for ctype in criterion_types:
        if ctype not in ['max', 'min']:
            return False, f"Criterion type must be 'max' or 'min', got: {ctype}"
    
    # Validate scores structure
    if not isinstance(scores, dict):
        return False, "Scores must be a dictionary mapping options to score lists"
    
    # Check all options have scores
    for option in options:
        if option not in scores:
            return False, f"Missing scores for option: {option}"
        
        option_scores = scores[option]
        
        # Check score list length matches criteria count
        if len(option_scores) != len(criteria):
            return False, f"Option '{option}' has {len(option_scores)} scores but {len(criteria)} criteria exist"
        
        # Check all scores are numeric
        try:
            [float(score) for score in option_scores]
        except (ValueError, TypeError):
            return False, f"All scores for option '{option}' must be numeric values"
    
    # Ensure no extra options in scores
    extra_options = set(scores.keys()) - set(options)
    if extra_options:
        return False, f"Unknown options in scores: {', '.join(extra_options)}"
    
    return True, None


def validate_option_name(name):
    """
    Validate individual option name.
    
    Args:
        name (str): Option name to validate
    
    Returns:
        bool: True if valid
    """
    return isinstance(name, str) and len(name.strip()) > 0


def validate_criterion_name(name):
    """
    Validate individual criterion name.
    
    Args:
        name (str): Criterion name to validate
    
    Returns:
        bool: True if valid
    """
    return isinstance(name, str) and len(name.strip()) > 0
