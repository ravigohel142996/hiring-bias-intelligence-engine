"""
Collapse Simulator Module for Hiring Bias Intelligence Engine

This module perturbs hiring rules to test decision stability and identify
unstable decision boundaries.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from copy import deepcopy


class CollapseSimulator:
    """
    Simulates rule perturbations to test decision stability.
    """
    
    def __init__(self, rule_engine):
        """
        Initialize the collapse simulator.
        
        Parameters:
        -----------
        rule_engine : HiringRuleEngine
            The rule engine to simulate
        """
        self.rule_engine = rule_engine
        self.baseline_results = None
    
    def set_baseline(self, candidates_df: pd.DataFrame):
        """
        Set baseline results for comparison.
        
        Parameters:
        -----------
        candidates_df : pd.DataFrame
            DataFrame with candidate data
        """
        self.baseline_results = self.rule_engine.evaluate_batch(candidates_df)
    
    def perturb_rules(self, perturbations: Dict) -> Dict:
        """
        Apply perturbations to rules.
        
        Parameters:
        -----------
        perturbations : dict
            Dictionary of rule changes, e.g., {'cgpa_min': -0.2, 'experience_min': 1}
            
        Returns:
        --------
        dict
            Modified rules
        """
        modified_rules = deepcopy(self.rule_engine.rules)
        
        for rule, change in perturbations.items():
            if rule in modified_rules:
                modified_rules[rule] += change
        
        return modified_rules
    
    def simulate_perturbation(self, candidates_df: pd.DataFrame, 
                             perturbations: Dict) -> pd.DataFrame:
        """
        Simulate a single perturbation scenario.
        
        Parameters:
        -----------
        candidates_df : pd.DataFrame
            DataFrame with candidate data
        perturbations : dict
            Rule perturbations to apply
            
        Returns:
        --------
        pd.DataFrame
            Results after perturbation
        """
        # Save original rules
        original_rules = deepcopy(self.rule_engine.rules)
        
        # Apply perturbations
        modified_rules = self.perturb_rules(perturbations)
        self.rule_engine.update_rules(modified_rules)
        
        # Evaluate with perturbed rules
        perturbed_results = self.rule_engine.evaluate_batch(candidates_df)
        
        # Restore original rules
        self.rule_engine.update_rules(original_rules)
        
        return perturbed_results
    
    def measure_decision_flips(self, baseline_df: pd.DataFrame, 
                               perturbed_df: pd.DataFrame) -> Dict:
        """
        Measure how many decisions changed.
        
        Parameters:
        -----------
        baseline_df : pd.DataFrame
            Baseline decisions
        perturbed_df : pd.DataFrame
            Perturbed decisions
            
        Returns:
        --------
        dict
            Flip statistics
        """
        total = len(baseline_df)
        
        # Count flips
        flips = (baseline_df['decision'] != perturbed_df['decision']).sum()
        
        # Analyze flip types
        flip_types = {
            'accept_to_review': 0,
            'accept_to_reject': 0,
            'review_to_accept': 0,
            'review_to_reject': 0,
            'reject_to_review': 0,
            'reject_to_accept': 0
        }
        
        for i in range(total):
            baseline_decision = baseline_df.iloc[i]['decision']
            perturbed_decision = perturbed_df.iloc[i]['decision']
            
            if baseline_decision != perturbed_decision:
                flip_key = f"{baseline_decision.lower()}_to_{perturbed_decision.lower()}"
                if flip_key in flip_types:
                    flip_types[flip_key] += 1
        
        flip_rate = flips / total * 100
        
        return {
            'total_flips': flips,
            'flip_rate': flip_rate,
            'flip_types': flip_types,
            'stable_count': total - flips,
            'stability_score': (total - flips) / total * 100
        }
    
    def measure_acceptance_shift(self, baseline_df: pd.DataFrame, 
                                 perturbed_df: pd.DataFrame) -> Dict:
        """
        Measure how acceptance rates shift.
        
        Parameters:
        -----------
        baseline_df : pd.DataFrame
            Baseline decisions
        perturbed_df : pd.DataFrame
            Perturbed decisions
            
        Returns:
        --------
        dict
            Acceptance rate shift metrics
        """
        baseline_accept_rate = (baseline_df['decision'] == 'ACCEPT').sum() / len(baseline_df) * 100
        perturbed_accept_rate = (perturbed_df['decision'] == 'ACCEPT').sum() / len(perturbed_df) * 100
        
        shift = perturbed_accept_rate - baseline_accept_rate
        
        return {
            'baseline_accept_rate': baseline_accept_rate,
            'perturbed_accept_rate': perturbed_accept_rate,
            'absolute_shift': shift,
            'relative_shift': (shift / baseline_accept_rate * 100) if baseline_accept_rate > 0 else 0
        }
    
    def identify_unstable_regions(self, candidates_df: pd.DataFrame, 
                                  perturbation_scenarios: List[Dict]) -> Dict:
        """
        Identify candidate regions with unstable decisions.
        
        Parameters:
        -----------
        candidates_df : pd.DataFrame
            DataFrame with candidate data
        perturbation_scenarios : list of dict
            List of perturbation scenarios to test
            
        Returns:
        --------
        dict
            Unstable region analysis
        """
        # Track how many times each candidate's decision flips
        flip_counts = np.zeros(len(candidates_df))
        
        baseline_results = self.rule_engine.evaluate_batch(candidates_df)
        
        for perturbation in perturbation_scenarios:
            perturbed_results = self.simulate_perturbation(candidates_df, perturbation)
            
            # Count flips for each candidate
            flips = (baseline_results['decision'] != perturbed_results['decision']).values
            flip_counts += flips.astype(int)
        
        # Identify unstable candidates (flipped in multiple scenarios)
        n_scenarios = len(perturbation_scenarios)
        instability_threshold = n_scenarios * 0.3  # Flips in >30% of scenarios
        
        unstable_mask = flip_counts >= instability_threshold
        unstable_candidates = candidates_df[unstable_mask].copy()
        unstable_candidates['flip_count'] = flip_counts[unstable_mask]
        unstable_candidates['instability_score'] = (flip_counts[unstable_mask] / n_scenarios * 100)
        
        # Analyze characteristics of unstable regions
        if len(unstable_candidates) > 0:
            unstable_profile = {
                'count': len(unstable_candidates),
                'percentage': len(unstable_candidates) / len(candidates_df) * 100,
                'avg_skill_score': unstable_candidates['skill_score'].mean(),
                'avg_cgpa': unstable_candidates['cgpa'].mean(),
                'avg_experience': unstable_candidates['years_experience'].mean(),
                'avg_gap': unstable_candidates['employment_gap'].mean(),
                'avg_flip_count': unstable_candidates['flip_count'].mean(),
                'avg_instability_score': unstable_candidates['instability_score'].mean()
            }
        else:
            unstable_profile = {
                'count': 0,
                'percentage': 0
            }
        
        return {
            'unstable_candidates': unstable_candidates,
            'unstable_profile': unstable_profile,
            'stable_count': len(candidates_df) - len(unstable_candidates),
            'total_scenarios_tested': n_scenarios
        }
    
    def run_full_simulation(self, candidates_df: pd.DataFrame) -> Dict:
        """
        Run a comprehensive collapse simulation with multiple perturbations.
        
        Parameters:
        -----------
        candidates_df : pd.DataFrame
            DataFrame with candidate data
            
        Returns:
        --------
        dict
            Complete simulation results
        """
        # Define perturbation scenarios
        scenarios = [
            {'name': 'CGPA -0.2', 'perturbations': {'cgpa_min': -0.2}},
            {'name': 'CGPA +0.2', 'perturbations': {'cgpa_min': 0.2}},
            {'name': 'Experience +1', 'perturbations': {'experience_min': 1}},
            {'name': 'Experience -1', 'perturbations': {'experience_min': -1}},
            {'name': 'Skills -5', 'perturbations': {'skill_score_min': -5}},
            {'name': 'Skills +5', 'perturbations': {'skill_score_min': 5}},
            {'name': 'Gap +1', 'perturbations': {'gap_max': 1}},
            {'name': 'Gap -1', 'perturbations': {'gap_max': -1}},
            {'name': 'Combined +', 'perturbations': {'cgpa_min': 0.2, 'skill_score_min': 5}},
            {'name': 'Combined -', 'perturbations': {'cgpa_min': -0.2, 'skill_score_min': -5}}
        ]
        
        # Get baseline
        baseline_results = self.rule_engine.evaluate_batch(candidates_df)
        
        simulation_results = {}
        
        for scenario in scenarios:
            # Simulate scenario
            perturbed_results = self.simulate_perturbation(
                candidates_df, 
                scenario['perturbations']
            )
            
            # Measure impacts
            flips = self.measure_decision_flips(baseline_results, perturbed_results)
            shift = self.measure_acceptance_shift(baseline_results, perturbed_results)
            
            simulation_results[scenario['name']] = {
                'perturbations': scenario['perturbations'],
                'flip_metrics': flips,
                'acceptance_shift': shift,
                'stability_score': flips['stability_score']
            }
        
        # Identify unstable regions
        perturbation_list = [s['perturbations'] for s in scenarios]
        unstable_regions = self.identify_unstable_regions(candidates_df, perturbation_list)
        
        # Calculate overall stability score (average across scenarios)
        avg_stability = np.mean([r['stability_score'] for r in simulation_results.values()])
        
        return {
            'scenarios': simulation_results,
            'unstable_regions': unstable_regions,
            'overall_stability_score': avg_stability,
            'baseline_acceptance_rate': (baseline_results['decision'] == 'ACCEPT').sum() / len(baseline_results) * 100
        }


if __name__ == "__main__":
    # Example usage
    from data_generator import generate_candidates
    from rule_engine import HiringRuleEngine
    
    print("=" * 70)
    print("Collapse Simulator Test")
    print("=" * 70)
    
    # Generate test data
    candidates = generate_candidates(n_candidates=1000, random_seed=42)
    
    # Create engine and simulator
    engine = HiringRuleEngine()
    simulator = CollapseSimulator(engine)
    
    # Run full simulation
    results = simulator.run_full_simulation(candidates)
    
    print(f"\nOverall Stability Score: {results['overall_stability_score']:.1f}%")
    print(f"Baseline Acceptance Rate: {results['baseline_acceptance_rate']:.1f}%")
    
    print(f"\nScenario Results:")
    for scenario_name, metrics in list(results['scenarios'].items())[:5]:
        print(f"\n  {scenario_name}:")
        print(f"    Flips: {metrics['flip_metrics']['total_flips']} ({metrics['flip_metrics']['flip_rate']:.1f}%)")
        print(f"    Acceptance shift: {metrics['acceptance_shift']['absolute_shift']:+.1f}%")
        print(f"    Stability: {metrics['stability_score']:.1f}%")
    
    print(f"\nUnstable Regions:")
    unstable = results['unstable_regions']['unstable_profile']
    print(f"  Unstable candidates: {unstable['count']} ({unstable.get('percentage', 0):.1f}%)")
    if unstable['count'] > 0:
        print(f"  Avg instability score: {unstable['avg_instability_score']:.1f}%")
    
    print("\n" + "=" * 70)
    print("✓ Collapse Simulator working correctly!")
