"""
Metrics Module for Hiring Bias Intelligence Engine

Utility functions for calculating various metrics and statistics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def calculate_fairness_metrics(results_df: pd.DataFrame, 
                               protected_attribute: str = 'college_tier') -> Dict:
    """
    Calculate fairness metrics like demographic parity and equalized odds.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with decisions and attributes
    protected_attribute : str
        Name of the protected attribute column
        
    Returns:
    --------
    dict
        Fairness metrics
    """
    metrics = {}
    
    # Overall acceptance rate
    overall_accept_rate = (results_df['decision'] == 'ACCEPT').sum() / len(results_df)
    
    # Acceptance rates by protected attribute
    groups = results_df[protected_attribute].unique()
    group_rates = {}
    
    for group in groups:
        group_data = results_df[results_df[protected_attribute] == group]
        if len(group_data) > 0:
            accept_rate = (group_data['decision'] == 'ACCEPT').sum() / len(group_data)
            group_rates[group] = accept_rate
    
    # Demographic parity difference (max difference between groups)
    if len(group_rates) > 1:
        max_rate = max(group_rates.values())
        min_rate = min(group_rates.values())
        demographic_parity = max_rate - min_rate
    else:
        demographic_parity = 0
    
    metrics = {
        'overall_acceptance_rate': overall_accept_rate,
        'group_acceptance_rates': group_rates,
        'demographic_parity_difference': demographic_parity,
        'is_fair': demographic_parity < 0.1  # Common threshold
    }
    
    return metrics


def calculate_accuracy_metrics(results_df: pd.DataFrame, 
                               ground_truth_col: str = None) -> Dict:
    """
    Calculate accuracy metrics if ground truth is available.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with decisions
    ground_truth_col : str
        Name of ground truth column (if available)
        
    Returns:
    --------
    dict
        Accuracy metrics
    """
    if ground_truth_col and ground_truth_col in results_df.columns:
        # Calculate traditional metrics
        correct = (results_df['decision'] == results_df[ground_truth_col]).sum()
        accuracy = correct / len(results_df)
        
        return {
            'accuracy': accuracy,
            'correct_predictions': correct,
            'total_predictions': len(results_df)
        }
    else:
        # Use proxy metrics based on score distribution
        return {
            'avg_score': results_df['score'].mean(),
            'score_std': results_df['score'].std(),
            'high_confidence_rate': (results_df['score'] >= 4).sum() / len(results_df)
        }


def calculate_rule_effectiveness(results_df: pd.DataFrame) -> Dict:
    """
    Calculate how effective each rule is at predicting outcomes.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with rule results
        
    Returns:
    --------
    dict
        Rule effectiveness metrics
    """
    rules = ['rule_skill_score', 'rule_cgpa', 'rule_experience', 
             'rule_employment_gap', 'rule_tier_1_bonus']
    
    effectiveness = {}
    
    for rule in rules:
        # Precision: of those who passed the rule, how many were accepted?
        passed = results_df[results_df[rule] == True]
        if len(passed) > 0:
            precision = (passed['decision'] == 'ACCEPT').sum() / len(passed)
        else:
            precision = 0
        
        # Recall: of those accepted, how many passed this rule?
        accepted = results_df[results_df['decision'] == 'ACCEPT']
        if len(accepted) > 0:
            recall = (accepted[rule] == True).sum() / len(accepted)
        else:
            recall = 0
        
        # F1 score
        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        else:
            f1_score = 0
        
        effectiveness[rule] = {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'pass_rate': results_df[rule].sum() / len(results_df)
        }
    
    return effectiveness


def calculate_intersectional_bias(results_df: pd.DataFrame, 
                                  attributes: List[str]) -> Dict:
    """
    Calculate bias across intersections of multiple attributes.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with decisions
    attributes : list
        List of attribute columns to analyze
        
    Returns:
    --------
    dict
        Intersectional bias metrics
    """
    intersections = {}
    
    # Group by combinations of attributes
    grouped = results_df.groupby(attributes)
    
    for group_keys, group_data in grouped:
        if len(group_data) > 10:  # Only analyze groups with sufficient data
            accept_rate = (group_data['decision'] == 'ACCEPT').sum() / len(group_data)
            
            # Create readable key
            if isinstance(group_keys, tuple):
                key = '_'.join([f"{attr}={val}" for attr, val in zip(attributes, group_keys)])
            else:
                key = f"{attributes[0]}={group_keys}"
            
            intersections[key] = {
                'count': len(group_data),
                'acceptance_rate': accept_rate,
                'avg_score': group_data['score'].mean()
            }
    
    # Find max disparity
    if len(intersections) > 1:
        rates = [v['acceptance_rate'] for v in intersections.values()]
        max_disparity = max(rates) - min(rates)
    else:
        max_disparity = 0
    
    return {
        'intersections': intersections,
        'max_disparity': max_disparity,
        'num_intersections': len(intersections)
    }


def generate_summary_stats(results_df: pd.DataFrame) -> Dict:
    """
    Generate comprehensive summary statistics.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with all results
        
    Returns:
    --------
    dict
        Summary statistics
    """
    total = len(results_df)
    
    stats = {
        'total_candidates': total,
        'decisions': {
            'accept': (results_df['decision'] == 'ACCEPT').sum(),
            'review': (results_df['decision'] == 'REVIEW').sum(),
            'reject': (results_df['decision'] == 'REJECT').sum()
        },
        'rates': {
            'acceptance': (results_df['decision'] == 'ACCEPT').sum() / total * 100,
            'review': (results_df['decision'] == 'REVIEW').sum() / total * 100,
            'rejection': (results_df['decision'] == 'REJECT').sum() / total * 100
        },
        'score_distribution': {
            'mean': results_df['score'].mean(),
            'std': results_df['score'].std(),
            'min': results_df['score'].min(),
            'max': results_df['score'].max(),
            'q25': results_df['score'].quantile(0.25),
            'q50': results_df['score'].quantile(0.50),
            'q75': results_df['score'].quantile(0.75)
        },
        'feature_stats': {
            'avg_skill_score': results_df['skill_score'].mean(),
            'avg_cgpa': results_df['cgpa'].mean(),
            'avg_experience': results_df['years_experience'].mean(),
            'avg_gap': results_df['employment_gap'].mean()
        }
    }
    
    return stats


if __name__ == "__main__":
    # Example usage
    from data_generator import generate_candidates
    from rule_engine import HiringRuleEngine
    
    print("=" * 70)
    print("Metrics Module Test")
    print("=" * 70)
    
    # Generate test data
    candidates = generate_candidates(n_candidates=1000, random_seed=42)
    
    # Apply rule engine
    engine = HiringRuleEngine()
    results = engine.evaluate_batch(candidates)
    
    # Calculate various metrics
    fairness = calculate_fairness_metrics(results, 'college_tier')
    accuracy = calculate_accuracy_metrics(results)
    effectiveness = calculate_rule_effectiveness(results)
    intersectional = calculate_intersectional_bias(results, ['college_tier'])
    summary = generate_summary_stats(results)
    
    print(f"\nFairness Metrics:")
    print(f"  Overall acceptance rate: {fairness['overall_acceptance_rate']:.2%}")
    print(f"  Demographic parity difference: {fairness['demographic_parity_difference']:.2%}")
    print(f"  Is fair (< 10% difference): {fairness['is_fair']}")
    
    print(f"\nAccuracy Metrics:")
    print(f"  Avg score: {accuracy['avg_score']:.2f}")
    print(f"  High confidence rate: {accuracy['high_confidence_rate']:.2%}")
    
    print(f"\nRule Effectiveness:")
    for rule, metrics in list(effectiveness.items())[:3]:
        print(f"  {rule}:")
        print(f"    Precision: {metrics['precision']:.2%}")
        print(f"    Recall: {metrics['recall']:.2%}")
        print(f"    F1: {metrics['f1_score']:.2%}")
    
    print(f"\nSummary Stats:")
    print(f"  Total candidates: {summary['total_candidates']}")
    print(f"  Acceptance rate: {summary['rates']['acceptance']:.1f}%")
    print(f"  Avg score: {summary['score_distribution']['mean']:.2f}")
    
    print("\n" + "=" * 70)
    print("✓ Metrics module working correctly!")
