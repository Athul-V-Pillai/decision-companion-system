"""
Decision Explanation Module
Generates human-readable explanations of the decision logic and results.
"""


def explain_decision(evaluation_result):
    """
    Generate a human-readable explanation of the decision.
    
    Args:
        evaluation_result (dict): Result from evaluate_options() containing:
            - ranked_options
            - scores
            - details
            - weights
    
    Returns:
        dict: Explanation containing:
            - summary (str): Brief summary of the decision
            - recommendation (str): Top recommendation with reasoning
            - ranking_explanation (list): Explanation for each ranked option
            - methodology (str): Explanation of the methodology used
    """
    ranked_options = evaluation_result['ranked_options']
    scores = evaluation_result['scores']
    details = evaluation_result['details']
    weights = evaluation_result['weights']
    
    # Build explanation
    explanation = {
        'summary': _generate_summary(ranked_options, scores),
        'recommendation': _generate_recommendation(ranked_options, scores, details),
        'ranking_explanation': _generate_ranking_explanation(ranked_options, scores, details),
        'methodology': _generate_methodology_explanation(weights)
    }
    
    return explanation


def _generate_summary(ranked_options, scores):
    """Generate a brief summary of the result."""
    if not ranked_options:
        return "No options to evaluate."
    
    top_option = ranked_options[0]
    top_score = scores[top_option]
    
    summary = f"Based on weighted criteria analysis, '{top_option}' is the best choice "
    summary += f"with a total score of {top_score:.4f}."
    
    if len(ranked_options) > 1:
        second_option = ranked_options[1]
        second_score = scores[second_option]
        diff = top_score - second_score
        summary += f" It outperforms the second-best option ('{second_option}') by {diff:.4f} points."
    
    return summary


def _generate_recommendation(ranked_options, scores, details):
    """Generate recommendation with reasoning."""
    if not ranked_options:
        return "No recommendation available."
    
    top_option = ranked_options[0]
    top_details = details[top_option]
    
    recommendation = f"RECOMMENDATION: Choose '{top_option}'\n\n"
    recommendation += f"Final Score: {top_details['total_score']}\n\n"
    recommendation += "Key factors contributing to this choice:\n"
    
    # Sort criteria by their contribution (descending)
    criteria_by_contribution = sorted(
        top_details['criteria_breakdown'],
        key=lambda x: x['contribution'],
        reverse=True
    )
    
    for i, criterion_data in enumerate(criteria_by_contribution[:3], 1):
        recommendation += f"  {i}. {criterion_data['criterion']}: "
        recommendation += f"Score {criterion_data['raw_score']} (contribution: {criterion_data['contribution']:.4f})\n"
    
    return recommendation


def _generate_ranking_explanation(ranked_options, scores, details):
    """Generate explanation for each ranked option."""
    explanations = []
    
    for rank, option in enumerate(ranked_options, 1):
        option_details = details[option]
        score = option_details['total_score']
        
        # Find strongest and weakest criteria
        criteria_by_score = sorted(
            option_details['criteria_breakdown'],
            key=lambda x: x['normalized_score'],
            reverse=True
        )
        
        strongest = criteria_by_score[0]
        weakest = criteria_by_score[-1]
        
        explanation = {
            'rank': rank,
            'option': option,
            'total_score': score,
            'summary': f"#{rank}: {option} (Score: {score})",
            'strengths': f"Strongest in {strongest['criterion']} ({strongest['normalized_score']:.4f})",
            'weaknesses': f"Weakest in {weakest['criterion']} ({weakest['normalized_score']:.4f})"
        }
        
        explanations.append(explanation)
    
    return explanations


def _generate_methodology_explanation(weights):
    """Generate explanation of the methodology used."""
    methodology = "METHODOLOGY: Weighted Sum Model (WSM)\n\n"
    methodology += "This analysis uses the Weighted Sum Model, a multi-criteria decision analysis technique that:\n"
    methodology += "  1. Normalizes all scores to a 0-1 range per criterion\n"
    methodology += "     - For 'max' criteria: higher scores are better\n"
    methodology += "     - For 'min' criteria: lower scores are better\n"
    methodology += "  2. Applies criterion weights to normalized scores\n"
    methodology += "  3. Sums weighted contributions to get final scores\n"
    methodology += "  4. Ranks options by final score (highest is best)\n\n"
    
    methodology += "Criterion Weights (normalized):\n"
    for criterion, weight in weights.items():
        percentage = weight * 100
        methodology += f"  - {criterion}: {percentage:.1f}%\n"
    
    return methodology


def format_explanation_as_text(explanation):
    """
    Format explanation dictionary as readable text.
    
    Args:
        explanation (dict): Explanation from explain_decision()
    
    Returns:
        str: Formatted text explanation
    """
    text = ""
    text += "=" * 70 + "\n"
    text += "DECISION ANALYSIS RESULT\n"
    text += "=" * 70 + "\n\n"
    
    text += explanation['summary'] + "\n\n"
    
    text += "-" * 70 + "\n"
    text += explanation['recommendation'] + "\n"
    
    text += "-" * 70 + "\n"
    text += "FULL RANKING:\n"
    for item in explanation['ranking_explanation']:
        text += f"  {item['summary']}\n"
        text += f"    {item['strengths']}\n"
        text += f"    {item['weaknesses']}\n\n"
    
    text += "-" * 70 + "\n"
    text += explanation['methodology']
    
    return text
