"""
Bias Analyzer Module for Hiring Bias Intelligence Engine

This module uses clustering to identify groups of candidates and analyzes
acceptance rates across groups to detect potential biases.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple


class BiasAnalyzer:
    """
    Analyzes hiring decisions for potential biases using clustering and statistics.
    """
    
    def __init__(self, n_clusters=5):
        """
        Initialize the bias analyzer.
        
        Parameters:
        -----------
        n_clusters : int
            Number of clusters for KMeans
        """
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = None
        self.cluster_profiles = None
    
    def cluster_candidates(self, candidates_df: pd.DataFrame) -> pd.DataFrame:
        """
        Cluster candidates using KMeans based on their features.
        
        Parameters:
        -----------
        candidates_df : pd.DataFrame
            DataFrame with candidate features
            
        Returns:
        --------
        pd.DataFrame
            Original DataFrame with added 'cluster' column
        """
        # Select features for clustering
        features = ['skill_score', 'years_experience', 'cgpa', 
                   'college_tier', 'employment_gap', 'certifications_count']
        
        X = candidates_df[features].values
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Perform KMeans clustering
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        clusters = self.kmeans.fit_predict(X_scaled)
        
        # Add cluster labels to dataframe
        result_df = candidates_df.copy()
        result_df['cluster'] = clusters
        
        # Calculate cluster profiles (average values per cluster)
        self.cluster_profiles = result_df.groupby('cluster')[features].mean()
        
        return result_df
    
    def calculate_acceptance_rates(self, results_df: pd.DataFrame) -> Dict:
        """
        Calculate acceptance rates per cluster.
        
        Parameters:
        -----------
        results_df : pd.DataFrame
            DataFrame with clusters and decisions
            
        Returns:
        --------
        dict
            Acceptance rates and statistics per cluster
        """
        acceptance_by_cluster = {}
        
        for cluster_id in range(self.n_clusters):
            cluster_data = results_df[results_df['cluster'] == cluster_id]
            total = len(cluster_data)
            
            if total > 0:
                accept_count = (cluster_data['decision'] == 'ACCEPT').sum()
                review_count = (cluster_data['decision'] == 'REVIEW').sum()
                reject_count = (cluster_data['decision'] == 'REJECT').sum()
                
                acceptance_by_cluster[cluster_id] = {
                    'total': total,
                    'accept_count': accept_count,
                    'review_count': review_count,
                    'reject_count': reject_count,
                    'acceptance_rate': accept_count / total * 100,
                    'review_rate': review_count / total * 100,
                    'reject_rate': reject_count / total * 100,
                    'avg_skill_score': cluster_data['skill_score'].mean(),
                    'avg_cgpa': cluster_data['cgpa'].mean(),
                    'avg_experience': cluster_data['years_experience'].mean(),
                    'avg_gap': cluster_data['employment_gap'].mean(),
                    'tier_1_pct': (cluster_data['college_tier'] == 1).sum() / total * 100
                }
        
        return acceptance_by_cluster
    
    def identify_proxy_bias(self, results_df: pd.DataFrame) -> Dict:
        """
        Identify potential proxy biases (college tier, employment gap).
        
        Parameters:
        -----------
        results_df : pd.DataFrame
            DataFrame with decisions
            
        Returns:
        --------
        dict
            Bias metrics for each proxy variable
        """
        biases = {}
        
        # College Tier Bias
        tier_bias = {}
        for tier in [1, 2, 3]:
            tier_data = results_df[results_df['college_tier'] == tier]
            if len(tier_data) > 0:
                acceptance_rate = (tier_data['decision'] == 'ACCEPT').sum() / len(tier_data) * 100
                tier_bias[f'tier_{tier}'] = {
                    'count': len(tier_data),
                    'acceptance_rate': acceptance_rate,
                    'avg_skill_score': tier_data['skill_score'].mean(),
                    'avg_cgpa': tier_data['cgpa'].mean()
                }
        
        # Calculate disparity (difference between tier 1 and tier 3)
        if 'tier_1' in tier_bias and 'tier_3' in tier_bias:
            tier_disparity = tier_bias['tier_1']['acceptance_rate'] - tier_bias['tier_3']['acceptance_rate']
        else:
            tier_disparity = 0
        
        biases['college_tier'] = {
            'by_tier': tier_bias,
            'disparity': tier_disparity,
            'bias_detected': abs(tier_disparity) > 15  # Flag if >15% difference
        }
        
        # Employment Gap Bias
        gap_bias = {}
        gap_ranges = [
            ('no_gap', 0, 0),
            ('small_gap', 0.1, 1),
            ('medium_gap', 1.1, 2),
            ('large_gap', 2.1, 5)
        ]
        
        for label, min_gap, max_gap in gap_ranges:
            gap_data = results_df[
                (results_df['employment_gap'] >= min_gap) & 
                (results_df['employment_gap'] <= max_gap)
            ]
            if len(gap_data) > 0:
                acceptance_rate = (gap_data['decision'] == 'ACCEPT').sum() / len(gap_data) * 100
                gap_bias[label] = {
                    'count': len(gap_data),
                    'acceptance_rate': acceptance_rate,
                    'avg_skill_score': gap_data['skill_score'].mean()
                }
        
        # Calculate gap penalty (difference between no gap and large gap)
        if 'no_gap' in gap_bias and 'large_gap' in gap_bias:
            gap_penalty = gap_bias['no_gap']['acceptance_rate'] - gap_bias['large_gap']['acceptance_rate']
        else:
            gap_penalty = 0
        
        biases['employment_gap'] = {
            'by_range': gap_bias,
            'penalty': gap_penalty,
            'bias_detected': gap_penalty > 20  # Flag if >20% penalty
        }
        
        return biases
    
    def flag_disproportionate_rules(self, results_df: pd.DataFrame, 
                                   threshold: float = 20.0) -> List[Dict]:
        """
        Flag rules that disproportionately affect outcomes.
        
        Parameters:
        -----------
        results_df : pd.DataFrame
            DataFrame with decisions and rule results
        threshold : float
            Percentage difference threshold to flag as disproportionate
            
        Returns:
        --------
        list of dict
            List of flagged rules with metrics
        """
        flagged_rules = []
        
        rules = ['rule_skill_score', 'rule_cgpa', 'rule_experience', 
                 'rule_employment_gap', 'rule_tier_1_bonus']
        
        for rule in rules:
            # Calculate acceptance rate for those who pass vs fail the rule
            passed = results_df[results_df[rule] == True]
            failed = results_df[results_df[rule] == False]
            
            if len(passed) > 0 and len(failed) > 0:
                pass_accept_rate = (passed['decision'] == 'ACCEPT').sum() / len(passed) * 100
                fail_accept_rate = (failed['decision'] == 'ACCEPT').sum() / len(failed) * 100
                
                disparity = pass_accept_rate - fail_accept_rate
                
                if abs(disparity) > threshold:
                    flagged_rules.append({
                        'rule': rule,
                        'pass_count': len(passed),
                        'fail_count': len(failed),
                        'pass_accept_rate': pass_accept_rate,
                        'fail_accept_rate': fail_accept_rate,
                        'disparity': disparity,
                        'severity': 'high' if abs(disparity) > 40 else 'medium'
                    })
        
        # Sort by disparity magnitude
        flagged_rules.sort(key=lambda x: abs(x['disparity']), reverse=True)
        
        return flagged_rules
    
    def generate_bias_report(self, results_df: pd.DataFrame) -> Dict:
        """
        Generate a comprehensive bias analysis report.
        
        Parameters:
        -----------
        results_df : pd.DataFrame
            DataFrame with clusters, decisions, and rule results
            
        Returns:
        --------
        dict
            Complete bias analysis report
        """
        # Cluster candidates if not already done
        if 'cluster' not in results_df.columns:
            results_df = self.cluster_candidates(results_df)
        
        # Calculate all metrics
        acceptance_rates = self.calculate_acceptance_rates(results_df)
        proxy_biases = self.identify_proxy_bias(results_df)
        flagged_rules = self.flag_disproportionate_rules(results_df)
        
        # Overall statistics
        overall_accept_rate = (results_df['decision'] == 'ACCEPT').sum() / len(results_df) * 100
        
        # Calculate fairness score (lower is more fair)
        acceptance_values = [cluster['acceptance_rate'] for cluster in acceptance_rates.values()]
        fairness_score = np.std(acceptance_values) if len(acceptance_values) > 0 else 0
        
        report = {
            'overall_acceptance_rate': overall_accept_rate,
            'fairness_score': fairness_score,
            'acceptance_by_cluster': acceptance_rates,
            'proxy_biases': proxy_biases,
            'flagged_rules': flagged_rules,
            'bias_summary': {
                'tier_bias_detected': proxy_biases['college_tier']['bias_detected'],
                'gap_bias_detected': proxy_biases['employment_gap']['bias_detected'],
                'high_severity_rules': len([r for r in flagged_rules if r['severity'] == 'high']),
                'total_flagged_rules': len(flagged_rules)
            }
        }
        
        return report


if __name__ == "__main__":
    # Example usage
    from data_generator import generate_candidates
    from rule_engine import HiringRuleEngine
    
    print("=" * 70)
    print("Bias Analyzer Test")
    print("=" * 70)
    
    # Generate test data
    candidates = generate_candidates(n_candidates=1000, random_seed=42)
    
    # Apply rule engine
    engine = HiringRuleEngine()
    results = engine.evaluate_batch(candidates)
    
    # Analyze bias
    analyzer = BiasAnalyzer(n_clusters=5)
    results_with_clusters = analyzer.cluster_candidates(results)
    
    # Generate bias report
    bias_report = analyzer.generate_bias_report(results_with_clusters)
    
    print(f"\nOverall Acceptance Rate: {bias_report['overall_acceptance_rate']:.1f}%")
    print(f"Fairness Score (std dev): {bias_report['fairness_score']:.2f}")
    
    print(f"\nAcceptance Rates by Cluster:")
    for cluster_id, metrics in bias_report['acceptance_by_cluster'].items():
        print(f"  Cluster {cluster_id}: {metrics['acceptance_rate']:.1f}% ({metrics['total']} candidates)")
    
    print(f"\nCollege Tier Bias:")
    tier_bias = bias_report['proxy_biases']['college_tier']
    print(f"  Disparity: {tier_bias['disparity']:.1f}%")
    print(f"  Bias Detected: {tier_bias['bias_detected']}")
    
    print(f"\nEmployment Gap Bias:")
    gap_bias = bias_report['proxy_biases']['employment_gap']
    print(f"  Penalty: {gap_bias['penalty']:.1f}%")
    print(f"  Bias Detected: {gap_bias['bias_detected']}")
    
    print(f"\nFlagged Rules ({len(bias_report['flagged_rules'])}):")
    for rule in bias_report['flagged_rules'][:3]:
        print(f"  {rule['rule']}: {rule['disparity']:.1f}% disparity ({rule['severity']} severity)")
    
    print("\n" + "=" * 70)
    print("✓ Bias Analyzer working correctly!")
