"""
Core modules for Hiring Bias Intelligence Engine
"""

from .data_generator import generate_candidates, get_data_summary
from .rule_engine import HiringRuleEngine
from .bias_analyzer import BiasAnalyzer
from .collapse_simulator import CollapseSimulator
from .metrics import (
    calculate_fairness_metrics,
    calculate_accuracy_metrics,
    calculate_rule_effectiveness,
    calculate_intersectional_bias,
    generate_summary_stats
)

__all__ = [
    'generate_candidates',
    'get_data_summary',
    'HiringRuleEngine',
    'BiasAnalyzer',
    'CollapseSimulator',
    'calculate_fairness_metrics',
    'calculate_accuracy_metrics',
    'calculate_rule_effectiveness',
    'calculate_intersectional_bias',
    'generate_summary_stats'
]
