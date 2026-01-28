"""
UI modules for Hiring Bias Intelligence Engine
"""

from .theme import apply_theme, get_theme_css
from .animations import (
    get_card_animation,
    get_fade_in_animation,
    create_animated_container,
    create_metric_card,
    create_progress_bar,
    create_status_badge,
    create_loading_spinner
)
from .components import (
    create_metric_cards,
    create_decision_pie_chart,
    create_acceptance_by_cluster_chart,
    create_bias_heatmap,
    create_rule_impact_chart,
    create_stability_chart,
    device_detector
)

__all__ = [
    'apply_theme',
    'get_theme_css',
    'get_card_animation',
    'get_fade_in_animation',
    'create_animated_container',
    'create_metric_card',
    'create_progress_bar',
    'create_status_badge',
    'create_loading_spinner',
    'create_metric_cards',
    'create_decision_pie_chart',
    'create_acceptance_by_cluster_chart',
    'create_bias_heatmap',
    'create_rule_impact_chart',
    'create_stability_chart',
    'device_detector'
]
