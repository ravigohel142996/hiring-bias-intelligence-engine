"""
Components Module for Hiring Bias Intelligence Engine

Reusable UI components for the dashboard.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import logging
from typing import Dict, List

# Configure logging
logger = logging.getLogger(__name__)


def create_error_fallback_figure(height: int = 400):
    """
    Create a fallback figure for when visualization fails.
    
    Parameters:
    -----------
    height : int
        Height of the figure in pixels
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Error fallback figure
    """
    fig = go.Figure()
    fig.add_annotation(
        text="Visualization temporarily unavailable",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color='white')
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height
    )
    return fig


def create_metric_cards(metrics: Dict):
    """
    Create a row of metric cards.
    
    Parameters:
    -----------
    metrics : dict
        Dictionary of metric name to value
    """
    cols = st.columns(len(metrics))
    
    for col, (title, value) in zip(cols, metrics.items()):
        with col:
            if isinstance(value, dict):
                st.metric(
                    label=title,
                    value=value.get('value', ''),
                    delta=value.get('delta', None)
                )
            else:
                st.metric(label=title, value=value)


def create_decision_pie_chart(results_df: pd.DataFrame, title="Decision Distribution"):
    """
    Create an animated pie chart for decisions.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with decision column
    title : str
        Chart title
        
    Returns:
    --------
    plotly.graph_objects.Figure
    """
    try:
        decision_counts = results_df['decision'].value_counts()
        
        colors = {
            'ACCEPT': '#10b981',
            'REVIEW': '#f59e0b',
            'REJECT': '#ef4444'
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=decision_counts.index,
            values=decision_counts.values,
            hole=0.4,
            marker=dict(colors=[colors.get(d, '#b0b0b0') for d in decision_counts.index]),
            textinfo='label+percent',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color='white', size=12)
            ),
            margin=dict(t=60, b=60, l=20, r=20),
            height=400,
            autosize=True
        )
        
        return fig
    except Exception as e:
        logger.error(f"Failed to create decision pie chart: {e}", exc_info=True)
        return create_error_fallback_figure(height=400)


def create_acceptance_by_cluster_chart(acceptance_by_cluster: Dict, title="Acceptance Rate by Cluster"):
    """
    Create a bar chart for acceptance rates by cluster.
    
    Parameters:
    -----------
    acceptance_by_cluster : dict
        Dictionary of cluster metrics
    title : str
        Chart title
        
    Returns:
    --------
    plotly.graph_objects.Figure
    """
    try:
        clusters = list(acceptance_by_cluster.keys())
        acceptance_rates = [acceptance_by_cluster[c]['acceptance_rate'] for c in clusters]
        totals = [acceptance_by_cluster[c]['total'] for c in clusters]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[f"Cluster {c}" for c in clusters],
            y=acceptance_rates,
            text=[f"{rate:.1f}%<br>({total} candidates)" for rate, total in zip(acceptance_rates, totals)],
            textposition='outside',
            marker=dict(
                color=acceptance_rates,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title=dict(text="Rate %", font=dict(color='white', size=12)),
                    tickfont=dict(color='white', size=10)
                )
            ),
            hovertemplate='<b>%{x}</b><br>Acceptance Rate: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, color='white')),
            xaxis=dict(
                title=dict(text="Cluster", font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12),
                gridcolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                title=dict(text="Acceptance Rate (%)", font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12),
                gridcolor='rgba(255,255,255,0.1)',
                range=[0, 100]
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=60, b=60, l=60, r=60),
            height=500,
            autosize=True
        )
        
        return fig
    except Exception as e:
        logger.error(f"Failed to create acceptance by cluster chart: {e}", exc_info=True)
        return create_error_fallback_figure(height=500)


def create_bias_heatmap(results_df: pd.DataFrame, title="Bias Heatmap"):
    """
    Create a heatmap showing bias patterns.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with results
    title : str
        Chart title
        
    Returns:
    --------
    plotly.graph_objects.Figure
    """
    try:
        # Create pivot table for acceptance rates
        pivot_data = pd.crosstab(
            results_df['college_tier'],
            results_df['employment_gap'].apply(lambda x: 'High' if x > 2 else 'Low'),
            values=(results_df['decision'] == 'ACCEPT').astype(int),
            aggfunc='mean'
        ) * 100
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=[f"Tier {i}" for i in pivot_data.index],
            colorscale='RdYlGn',
            text=pivot_data.values.round(1),
            texttemplate='%{text}%',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{y}</b><br>%{x} Gap<br>Acceptance: %{z:.1f}%<extra></extra>',
            colorbar=dict(
                title=dict(text="Rate %", font=dict(color='white', size=12)),
                tickfont=dict(color='white', size=10)
            )
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, color='white')),
            xaxis=dict(
                title=dict(text="Employment Gap", font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12)
            ),
            yaxis=dict(
                title=dict(text="College Tier", font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=60, b=60, l=80, r=80),
            height=400,
            autosize=True
        )
        
        return fig
    except Exception as e:
        logger.error(f"Failed to create bias heatmap: {e}", exc_info=True)
        return create_error_fallback_figure(height=400)


def create_rule_impact_chart(rule_impact: Dict, title="Rule Impact on Acceptance"):
    """
    Create a bar chart showing rule impact.
    
    Parameters:
    -----------
    rule_impact : dict
        Dictionary of rule impact metrics
    title : str
        Chart title
        
    Returns:
    --------
    plotly.graph_objects.Figure
    """
    try:
        rules = list(rule_impact.keys())
        impact_scores = [rule_impact[r]['impact_score'] for r in rules]
        rule_names = [r.replace('rule_', '').replace('_', ' ').title() for r in rules]
        
        colors = ['#10b981' if score > 0 else '#ef4444' for score in impact_scores]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=rule_names,
            x=impact_scores,
            orientation='h',
            text=[f"{score:+.1f}%" for score in impact_scores],
            textposition='outside',
            marker=dict(color=colors),
            hovertemplate='<b>%{y}</b><br>Impact: %{x:+.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, color='white')),
            xaxis=dict(
                title=dict(text="Impact Score (%)", font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12),
                gridcolor='rgba(255,255,255,0.1)',
                zeroline=True,
                zerolinecolor='rgba(255,255,255,0.3)',
                zerolinewidth=2
            ),
            yaxis=dict(
                tickfont=dict(color='white', size=12)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=60, b=60, l=150, r=100),
            height=400,
            autosize=True
        )
        
        return fig
    except Exception as e:
        logger.error(f"Failed to create rule impact chart: {e}", exc_info=True)
        return create_error_fallback_figure(height=400)


def create_stability_chart(scenarios: Dict, title="Decision Stability Across Scenarios"):
    """
    Create a chart showing stability across perturbation scenarios.
    
    Parameters:
    -----------
    scenarios : dict
        Dictionary of scenario results
    title : str
        Chart title
        
    Returns:
    --------
    plotly.graph_objects.Figure
    """
    try:
        scenario_names = list(scenarios.keys())
        stability_scores = [scenarios[s]['stability_score'] for s in scenario_names]
        flip_rates = [scenarios[s]['flip_metrics']['flip_rate'] for s in scenario_names]
        
        fig = go.Figure()
        
        # Stability bars
        fig.add_trace(go.Bar(
            name='Stability Score',
            x=scenario_names,
            y=stability_scores,
            marker=dict(color='#10b981'),
            text=[f"{score:.1f}%" for score in stability_scores],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Stability: %{y:.1f}%<extra></extra>'
        ))
        
        # Flip rate bars (inverted)
        fig.add_trace(go.Bar(
            name='Flip Rate',
            x=scenario_names,
            y=flip_rates,
            marker=dict(color='#ef4444'),
            text=[f"{rate:.1f}%" for rate in flip_rates],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Flip Rate: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, color='white')),
            xaxis=dict(
                tickfont=dict(color='white', size=10),
                tickangle=-45
            ),
            yaxis=dict(
                title=dict(text="Percentage (%)", font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12),
                gridcolor='rgba(255,255,255,0.1)',
                range=[0, 100]
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='white', size=12)
            ),
            margin=dict(t=80, b=120, l=60, r=60),
            height=500,
            autosize=True
        )
        
        return fig
    except Exception as e:
        logger.error(f"Failed to create stability chart: {e}", exc_info=True)
        return create_error_fallback_figure(height=500)


def device_detector():
    """
    Detect device type using viewport width.
    
    Returns:
    --------
    dict
        Device info with is_mobile, is_tablet, is_desktop flags
    """
    # Use session state to store device info
    if 'device_info' not in st.session_state:
        # Default to desktop
        st.session_state.device_info = {
            'is_mobile': False,
            'is_tablet': False,
            'is_desktop': True,
            'width': 1024
        }
    
    # Inject JavaScript to detect width and update session state
    st.markdown("""
    <script>
        const width = window.innerWidth;
        const device = width < 768 ? 'mobile' : width < 1024 ? 'tablet' : 'desktop';
        // Note: In production, you'd send this back to Streamlit via query params or custom component
    </script>
    """, unsafe_allow_html=True)
    
    return st.session_state.device_info


if __name__ == "__main__":
    print("✓ Components module created")
    print("  - Metric cards")
    print("  - Decision pie chart")
    print("  - Acceptance by cluster chart")
    print("  - Bias heatmap")
    print("  - Rule impact chart")
    print("  - Stability chart")
    print("  - Device detector")
