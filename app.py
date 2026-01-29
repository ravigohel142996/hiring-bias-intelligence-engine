"""
Hiring Bias Intelligence Engine - Main Streamlit Application

A decision intelligence platform that stress-tests hiring rules under scale,
bias, and adversarial scenarios.
"""

import streamlit as st
import pandas as pd
import numpy as np

# Import core modules
from core import (
    generate_candidates,
    HiringRuleEngine,
    BiasAnalyzer,
    CollapseSimulator,
    generate_summary_stats
)

# Import UI modules
from ui.theme import apply_theme
from ui.components import (
    create_metric_cards,
    create_decision_pie_chart,
    create_acceptance_by_cluster_chart,
    create_bias_heatmap,
    create_rule_impact_chart,
    create_stability_chart,
    device_detector
)
from ui.animations import create_metric_card, create_status_badge


# Page configuration
st.set_page_config(
    page_title="Hiring Bias Intelligence Engine",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme
apply_theme()

# Device detection
device_info = device_detector()
is_mobile = device_info['is_mobile']
is_tablet = device_info['is_tablet']
is_desktop = device_info['is_desktop']


def initialize_session_state():
    """Initialize session state variables."""
    if 'candidates' not in st.session_state:
        st.session_state.candidates = None
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'bias_report' not in st.session_state:
        st.session_state.bias_report = None
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = None
    if 'data_generated' not in st.session_state:
        st.session_state.data_generated = False


def generate_data(n_candidates=1000):
    """Generate candidate data and run all analyses."""
    with st.spinner("🔄 Generating candidates..."):
        st.session_state.candidates = generate_candidates(n_candidates=n_candidates, random_seed=42)
    
    with st.spinner("⚙️ Evaluating rules..."):
        engine = HiringRuleEngine()
        st.session_state.results = engine.evaluate_batch(st.session_state.candidates)
        st.session_state.engine = engine
    
    with st.spinner("🔍 Analyzing bias..."):
        analyzer = BiasAnalyzer(n_clusters=5)
        results_with_clusters = analyzer.cluster_candidates(st.session_state.results)
        st.session_state.results = results_with_clusters
        st.session_state.bias_report = analyzer.generate_bias_report(results_with_clusters)
    
    with st.spinner("🧪 Running simulations..."):
        simulator = CollapseSimulator(engine)
        st.session_state.simulation_results = simulator.run_full_simulation(st.session_state.candidates)
    
    st.session_state.data_generated = True
    st.success("✅ All analyses complete!")


def page_overview():
    """Overview page with key metrics."""
    st.title("🎯 Hiring Bias Intelligence Engine")
    st.markdown("### Decision Intelligence Platform")
    
    # Generate data button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 Generate New Data", key="gen_data", use_container_width=True):
            n_candidates_value = st.session_state.get('n_candidates_input', 1000)
            generate_data(n_candidates=n_candidates_value)
    
    with col2:
        n_candidates = st.number_input("Candidates", min_value=100, max_value=10000, value=1000, step=100, key='n_candidates_input')
    
    if not st.session_state.data_generated:
        st.info("👆 Click 'Generate New Data' to start analysis")
        return
    
    # Key metrics
    st.markdown("---")
    st.subheader("📊 Key Metrics")
    
    results = st.session_state.results
    bias_report = st.session_state.bias_report
    sim_results = st.session_state.simulation_results
    
    # Metric cards (responsive layout)
    if is_mobile:
        # Single column on mobile
        st.markdown(create_metric_card(
            "Total Candidates",
            f"{len(results):,}",
            "Synthetic profiles generated",
            "👥"
        ), unsafe_allow_html=True)
        
        st.markdown(create_metric_card(
            "Acceptance Rate",
            f"{bias_report['overall_acceptance_rate']:.1f}%",
            f"{(results['decision'] == 'ACCEPT').sum()} accepted",
            "✅"
        ), unsafe_allow_html=True)
        
        st.markdown(create_metric_card(
            "Fairness Score",
            f"{bias_report['fairness_score']:.2f}",
            "Lower is more fair",
            "⚖️"
        ), unsafe_allow_html=True)
        
        st.markdown(create_metric_card(
            "Stability Score",
            f"{sim_results['overall_stability_score']:.1f}%",
            "Decision consistency",
            "🎯"
        ), unsafe_allow_html=True)
    else:
        # Multi-column on tablet/desktop
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Total Candidates",
                f"{len(results):,}",
                "Synthetic profiles",
                "👥"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Acceptance Rate",
                f"{bias_report['overall_acceptance_rate']:.1f}%",
                f"{(results['decision'] == 'ACCEPT').sum()} accepted",
                "✅"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Fairness Score",
                f"{bias_report['fairness_score']:.2f}",
                "Std dev across groups",
                "⚖️"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Stability Score",
                f"{sim_results['overall_stability_score']:.1f}%",
                "Decision consistency",
                "🎯"
            ), unsafe_allow_html=True)
    
    # Decision distribution
    st.markdown("---")
    st.subheader("📈 Decision Distribution")
    
    if is_mobile:
        st.plotly_chart(create_decision_pie_chart(results), use_container_width=True, config={'responsive': True})
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_decision_pie_chart(results), use_container_width=True, config={'responsive': True})
        with col2:
            # Additional stats
            st.markdown("##### Decision Breakdown")
            accept_count = (results['decision'] == 'ACCEPT').sum()
            review_count = (results['decision'] == 'REVIEW').sum()
            reject_count = (results['decision'] == 'REJECT').sum()
            
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                    <span>Accept:</span>
                    <span>{create_status_badge('accept', f'{accept_count} ({accept_count/len(results)*100:.1f}%)')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                    <span>Review:</span>
                    <span>{create_status_badge('review', f'{review_count} ({review_count/len(results)*100:.1f}%)')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                    <span>Reject:</span>
                    <span>{create_status_badge('reject', f'{reject_count} ({reject_count/len(results)*100:.1f}%)')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Bias summary
    st.markdown("---")
    st.subheader("🚨 Bias Detection Summary")
    
    tier_bias = bias_report['proxy_biases']['college_tier']
    gap_bias = bias_report['proxy_biases']['employment_gap']
    
    if is_mobile:
        # Mobile: single column
        st.markdown(f"""
        <div class="glass-card">
            <h4>📚 College Tier Bias</h4>
            <p>Disparity: <strong>{tier_bias['disparity']:.1f}%</strong></p>
            <p>Status: {create_status_badge('error' if tier_bias['bias_detected'] else 'success', 
                                           'Bias Detected' if tier_bias['bias_detected'] else 'Fair')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <h4>⏳ Employment Gap Bias</h4>
            <p>Penalty: <strong>{gap_bias['penalty']:.1f}%</strong></p>
            <p>Status: {create_status_badge('error' if gap_bias['bias_detected'] else 'success',
                                           'Bias Detected' if gap_bias['bias_detected'] else 'Fair')}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Desktop/tablet: two columns
        col1, col2 = st.columns(2)
        # Desktop/tablet: two columns
        col1, col2 = st.columns(2)
    
        with col1:
            st.markdown(f"""
            <div class="glass-card">
                <h4>📚 College Tier Bias</h4>
                <p>Disparity: <strong>{tier_bias['disparity']:.1f}%</strong></p>
                <p>Status: {create_status_badge('error' if tier_bias['bias_detected'] else 'success', 
                                               'Bias Detected' if tier_bias['bias_detected'] else 'Fair')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="glass-card">
                <h4>⏳ Employment Gap Bias</h4>
                <p>Penalty: <strong>{gap_bias['penalty']:.1f}%</strong></p>
                <p>Status: {create_status_badge('error' if gap_bias['bias_detected'] else 'success',
                                               'Bias Detected' if gap_bias['bias_detected'] else 'Fair')}</p>
            </div>
            """, unsafe_allow_html=True)


def page_bias_heatmap():
    """Bias heatmap page."""
    st.title("🔥 Bias Heatmap")
    
    if not st.session_state.data_generated:
        st.warning("⚠️ Please generate data first from the Overview page")
        return
    
    results = st.session_state.results
    bias_report = st.session_state.bias_report
    
    st.markdown("### Acceptance Rates Across Groups")
    
    # Cluster analysis
    st.plotly_chart(
        create_acceptance_by_cluster_chart(bias_report['acceptance_by_cluster']),
        use_container_width=True,
        config={'responsive': True}
    )
    
    # Bias heatmap
    st.markdown("### Tier vs Gap Acceptance Matrix")
    st.plotly_chart(
        create_bias_heatmap(results),
        use_container_width=True,
        config={'responsive': True}
    )
    
    # Flagged rules
    st.markdown("---")
    st.subheader("⚠️ Flagged Rules")
    
    flagged_rules = bias_report['flagged_rules']
    if flagged_rules:
        for rule in flagged_rules:
            severity_color = 'error' if rule['severity'] == 'high' else 'warning'
            st.markdown(f"""
            <div class="glass-card">
                <h4>{rule['rule'].replace('rule_', '').replace('_', ' ').title()}</h4>
                <p>Disparity: <strong>{rule['disparity']:.1f}%</strong> 
                   {create_status_badge(severity_color, rule['severity'].upper())}</p>
                <p>Pass rate: {rule['pass_accept_rate']:.1f}% | Fail rate: {rule['fail_accept_rate']:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No significantly biased rules detected!")


def page_rule_impact():
    """Rule impact page."""
    st.title("📊 Rule Impact Analysis")
    
    if not st.session_state.data_generated:
        st.warning("⚠️ Please generate data first from the Overview page")
        return
    
    results = st.session_state.results
    engine = st.session_state.engine
    
    rule_impact = engine.get_rule_impact(results)
    
    st.markdown("### Impact of Each Rule on Acceptance")
    st.plotly_chart(
        create_rule_impact_chart(rule_impact),
        use_container_width=True,
        config={'responsive': True}
    )
    
    # Rule details
    st.markdown("---")
    st.subheader("📋 Rule Details")
    
    for rule_name, metrics in rule_impact.items():
        with st.expander(f"{rule_name.replace('rule_', '').replace('_', ' ').title()}"):
            col1, col2 = st.columns(2) if not is_mobile else st.columns(1)
            
            with col1:
                st.metric("Pass Count", f"{metrics['pass_count']:,}")
                st.metric("Accept Rate (Passed)", f"{metrics['accept_rate_when_passed']:.1f}%")
            
            if not is_mobile:
                with col2:
                    st.metric("Fail Count", f"{metrics['fail_count']:,}")
                    st.metric("Accept Rate (Failed)", f"{metrics['accept_rate_when_failed']:.1f}%")
            else:
                st.metric("Fail Count", f"{metrics['fail_count']:,}")
                st.metric("Accept Rate (Failed)", f"{metrics['accept_rate_when_failed']:.1f}%")
            
            st.metric("Impact Score", f"{metrics['impact_score']:+.1f}%")


def page_collapse_simulation():
    """Collapse simulation page."""
    st.title("🧪 Rule Collapse Simulation")
    
    if not st.session_state.data_generated:
        st.warning("⚠️ Please generate data first from the Overview page")
        return
    
    sim_results = st.session_state.simulation_results
    
    st.markdown("### Decision Stability Under Perturbations")
    st.plotly_chart(
        create_stability_chart(sim_results['scenarios']),
        use_container_width=True,
        config={'responsive': True}
    )
    
    # Scenario details
    st.markdown("---")
    st.subheader("📊 Scenario Details")
    
    for scenario_name, metrics in list(sim_results['scenarios'].items())[:5]:
        with st.expander(f"📌 {scenario_name}"):
            col1, col2, col3 = st.columns(3) if not is_mobile else st.columns(1)
            
            with col1:
                st.metric("Stability", f"{metrics['stability_score']:.1f}%")
            
            if not is_mobile:
                with col2:
                    st.metric("Total Flips", metrics['flip_metrics']['total_flips'])
                with col3:
                    st.metric("Acceptance Shift", f"{metrics['acceptance_shift']['absolute_shift']:+.1f}%")
            else:
                st.metric("Total Flips", metrics['flip_metrics']['total_flips'])
                st.metric("Acceptance Shift", f"{metrics['acceptance_shift']['absolute_shift']:+.1f}%")
    
    # Unstable regions
    st.markdown("---")
    st.subheader("⚠️ Unstable Decision Regions")
    
    unstable = sim_results['unstable_regions']['unstable_profile']
    
    st.markdown(f"""
    <div class="glass-card">
        <p><strong>Unstable Candidates:</strong> {unstable['count']} ({unstable.get('percentage', 0):.1f}%)</p>
        {f"<p><strong>Avg Instability Score:</strong> {unstable.get('avg_instability_score', 0):.1f}%</p>" if unstable['count'] > 0 else ""}
        <p>{create_status_badge('success' if unstable['count'] < 100 else 'warning', 
                               'Stable System' if unstable['count'] < 100 else 'Some Instability')}</p>
    </div>
    """, unsafe_allow_html=True)


def page_insights():
    """Insights and recommendations page."""
    st.title("💡 Insights & Recommendations")
    
    if not st.session_state.data_generated:
        st.warning("⚠️ Please generate data first from the Overview page")
        return
    
    bias_report = st.session_state.bias_report
    sim_results = st.session_state.simulation_results
    
    st.markdown("### 🎯 Key Findings")
    
    # Generate insights
    insights = []
    
    # Bias insights
    if bias_report['bias_summary']['tier_bias_detected']:
        insights.append({
            'type': 'warning',
            'title': 'College Tier Bias Detected',
            'message': f"There's a {bias_report['proxy_biases']['college_tier']['disparity']:.1f}% disparity in acceptance rates between tier 1 and tier 3 colleges."
        })
    
    if bias_report['bias_summary']['gap_bias_detected']:
        insights.append({
            'type': 'warning',
            'title': 'Employment Gap Bias Detected',
            'message': f"Candidates with employment gaps face a {bias_report['proxy_biases']['employment_gap']['penalty']:.1f}% penalty in acceptance rates."
        })
    
    # Stability insights
    if sim_results['overall_stability_score'] < 80:
        insights.append({
            'type': 'error',
            'title': 'Low System Stability',
            'message': f"Overall stability score is {sim_results['overall_stability_score']:.1f}%. Small rule changes cause significant decision shifts."
        })
    
    # Fairness insights
    if bias_report['fairness_score'] > 10:
        insights.append({
            'type': 'warning',
            'title': 'High Fairness Score',
            'message': f"Fairness score of {bias_report['fairness_score']:.2f} indicates uneven acceptance rates across candidate groups."
        })
    
    # Display insights
    for insight in insights:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid {'#ef4444' if insight['type'] == 'error' else '#f59e0b'};">
            <h4>⚠️ {insight['title']}</h4>
            <p>{insight['message']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if not insights:
        st.success("✅ No major issues detected! The hiring system appears fair and stable.")
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 💡 Recommendations")
    
    recommendations = [
        "Review rules that show high disparity in acceptance rates",
        "Consider removing or adjusting the college tier bonus",
        "Implement a grace period for employment gaps",
        "Test rule changes with smaller perturbations",
        "Monitor acceptance rates across demographic groups regularly"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div class="glass-card">
            <p><strong>{i}.</strong> {rec}</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application."""
    initialize_session_state()
    
   # Sidebar navigation
with st.sidebar:
    st.image(
        "https://via.placeholder.com/150x50/667eea/ffffff?text=Bias+Engine",
        width="container"
    )
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["Overview", "Bias Heatmap", "Rule Impact", "Collapse Simulation", "Insights"],
        key="nav"
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This platform stress-tests hiring rules to expose:
    - Hidden bias amplification
    - Rule dominance & collapse  
    - Unstable decision boundaries
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

    # Route to pages
    if page == "Overview":
        page_overview()
    elif page == "Bias Heatmap":
        page_bias_heatmap()
    elif page == "Rule Impact":
        page_rule_impact()
    elif page == "Collapse Simulation":
        page_collapse_simulation()
    elif page == "Insights":
        page_insights()


if __name__ == "__main__":
    main()
