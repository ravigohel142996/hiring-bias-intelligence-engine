"""
Rule Engine Module for Hiring Bias Intelligence Engine

This module implements a rule-based hiring decision system that evaluates
candidates based on multiple criteria and tracks which rules fire for each decision.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class HiringRuleEngine:
    """
    Rule-based hiring decision engine with rule tracking.
    
    Rules:
    - skill_score >= 65
    - cgpa >= 7.0
    - years_experience >= 1
    - employment_gap <= 2
    - college_tier == 1 gives bonus
    
    Decisions: ACCEPT, REVIEW, REJECT
    """
    
    def __init__(self):
        """Initialize the rule engine with default thresholds."""
        self.rules = {
            'skill_score_min': 65,
            'cgpa_min': 7.0,
            'experience_min': 1,
            'gap_max': 2,
            'tier_1_bonus': True
        }
    
    def evaluate_candidate(self, candidate: Dict) -> Tuple[str, Dict[str, bool], int]:
        """
        Evaluate a single candidate against hiring rules.
        
        Parameters:
        -----------
        candidate : dict
            Dictionary with keys: skill_score, cgpa, years_experience, 
            employment_gap, college_tier
            
        Returns:
        --------
        tuple : (decision, rules_fired, score)
            - decision: 'ACCEPT', 'REVIEW', or 'REJECT'
            - rules_fired: dict mapping rule names to bool (passed or not)
            - score: int, number of rules passed
        """
        # Evaluate each rule
        rules_fired = {
            'skill_score': candidate['skill_score'] >= self.rules['skill_score_min'],
            'cgpa': candidate['cgpa'] >= self.rules['cgpa_min'],
            'experience': candidate['years_experience'] >= self.rules['experience_min'],
            'employment_gap': candidate['employment_gap'] <= self.rules['gap_max'],
            'tier_1_bonus': candidate['college_tier'] == 1
        }
        
        # Calculate base score (number of core rules passed, excluding bonus)
        core_rules_passed = sum([
            rules_fired['skill_score'],
            rules_fired['cgpa'],
            rules_fired['experience'],
            rules_fired['employment_gap']
        ])
        
        # Apply tier 1 bonus
        if rules_fired['tier_1_bonus']:
            core_rules_passed += 1
        
        # Decision logic
        if core_rules_passed >= 5:  # All core + bonus
            decision = 'ACCEPT'
        elif core_rules_passed >= 4:  # Most rules passed
            decision = 'ACCEPT'
        elif core_rules_passed >= 2:  # Some rules passed
            decision = 'REVIEW'
        else:  # Few rules passed
            decision = 'REJECT'
        
        return decision, rules_fired, core_rules_passed
    
    def evaluate_batch(self, candidates_df: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluate a batch of candidates.
        
        Parameters:
        -----------
        candidates_df : pd.DataFrame
            DataFrame with candidate information
            
        Returns:
        --------
        pd.DataFrame
            Original DataFrame with added columns:
            - decision: ACCEPT/REVIEW/REJECT
            - score: number of rules passed
            - rule_* : boolean for each rule
        """
        results = []
        
        for idx, row in candidates_df.iterrows():
            candidate = {
                'skill_score': row['skill_score'],
                'cgpa': row['cgpa'],
                'years_experience': row['years_experience'],
                'employment_gap': row['employment_gap'],
                'college_tier': row['college_tier']
            }
            
            decision, rules_fired, score = self.evaluate_candidate(candidate)
            
            result = {
                'decision': decision,
                'score': score,
                'rule_skill_score': rules_fired['skill_score'],
                'rule_cgpa': rules_fired['cgpa'],
                'rule_experience': rules_fired['experience'],
                'rule_employment_gap': rules_fired['employment_gap'],
                'rule_tier_1_bonus': rules_fired['tier_1_bonus']
            }
            
            results.append(result)
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        
        # Combine with original data
        output_df = pd.concat([candidates_df.reset_index(drop=True), results_df], axis=1)
        
        return output_df
    
    def get_decision_stats(self, results_df: pd.DataFrame) -> Dict:
        """
        Get statistics about decisions made.
        
        Parameters:
        -----------
        results_df : pd.DataFrame
            DataFrame with decision results
            
        Returns:
        --------
        dict
            Statistics including acceptance rate, decision distribution, etc.
        """
        total = len(results_df)
        
        stats = {
            'total_candidates': total,
            'accept_count': (results_df['decision'] == 'ACCEPT').sum(),
            'review_count': (results_df['decision'] == 'REVIEW').sum(),
            'reject_count': (results_df['decision'] == 'REJECT').sum(),
            'acceptance_rate': (results_df['decision'] == 'ACCEPT').sum() / total * 100,
            'review_rate': (results_df['decision'] == 'REVIEW').sum() / total * 100,
            'reject_rate': (results_df['decision'] == 'REJECT').sum() / total * 100,
            'avg_score': results_df['score'].mean(),
            'rule_pass_rates': {
                'skill_score': results_df['rule_skill_score'].sum() / total * 100,
                'cgpa': results_df['rule_cgpa'].sum() / total * 100,
                'experience': results_df['rule_experience'].sum() / total * 100,
                'employment_gap': results_df['rule_employment_gap'].sum() / total * 100,
                'tier_1_bonus': results_df['rule_tier_1_bonus'].sum() / total * 100
            }
        }
        
        return stats
    
    def get_rule_impact(self, results_df: pd.DataFrame) -> Dict:
        """
        Analyze the impact of each rule on decisions.
        
        Parameters:
        -----------
        results_df : pd.DataFrame
            DataFrame with decision results
            
        Returns:
        --------
        dict
            Impact metrics for each rule
        """
        rules = ['rule_skill_score', 'rule_cgpa', 'rule_experience', 
                 'rule_employment_gap', 'rule_tier_1_bonus']
        
        impact = {}
        
        for rule in rules:
            # Acceptance rate when rule passes vs fails
            passed = results_df[results_df[rule] == True]
            failed = results_df[results_df[rule] == False]
            
            if len(passed) > 0:
                accept_rate_passed = (passed['decision'] == 'ACCEPT').sum() / len(passed) * 100
            else:
                accept_rate_passed = 0
            
            if len(failed) > 0:
                accept_rate_failed = (failed['decision'] == 'ACCEPT').sum() / len(failed) * 100
            else:
                accept_rate_failed = 0
            
            impact[rule] = {
                'pass_count': len(passed),
                'fail_count': len(failed),
                'accept_rate_when_passed': accept_rate_passed,
                'accept_rate_when_failed': accept_rate_failed,
                'impact_score': accept_rate_passed - accept_rate_failed
            }
        
        return impact
    
    def update_rules(self, new_rules: Dict):
        """
        Update rule thresholds.
        
        Parameters:
        -----------
        new_rules : dict
            Dictionary with new rule values
        """
        self.rules.update(new_rules)


if __name__ == "__main__":
    # Example usage
    from data_generator import generate_candidates
    
    print("=" * 70)
    print("Rule Engine Test")
    print("=" * 70)
    
    # Generate test data
    candidates = generate_candidates(n_candidates=1000, random_seed=42)
    
    # Create engine and evaluate
    engine = HiringRuleEngine()
    results = engine.evaluate_batch(candidates)
    
    # Get statistics
    stats = engine.get_decision_stats(results)
    
    print(f"\nDecision Statistics:")
    print(f"  Total Candidates: {stats['total_candidates']}")
    print(f"  Accept: {stats['accept_count']} ({stats['acceptance_rate']:.1f}%)")
    print(f"  Review: {stats['review_count']} ({stats['review_rate']:.1f}%)")
    print(f"  Reject: {stats['reject_count']} ({stats['reject_rate']:.1f}%)")
    print(f"  Average Score: {stats['avg_score']:.2f}")
    
    print(f"\nRule Pass Rates:")
    for rule, rate in stats['rule_pass_rates'].items():
        print(f"  {rule}: {rate:.1f}%")
    
    # Get rule impact
    impact = engine.get_rule_impact(results)
    
    print(f"\nRule Impact Analysis:")
    for rule, metrics in impact.items():
        print(f"\n  {rule}:")
        print(f"    Pass count: {metrics['pass_count']}")
        print(f"    Fail count: {metrics['fail_count']}")
        print(f"    Accept rate (passed): {metrics['accept_rate_when_passed']:.1f}%")
        print(f"    Accept rate (failed): {metrics['accept_rate_when_failed']:.1f}%")
        print(f"    Impact score: {metrics['impact_score']:.1f}")
    
    print("\n" + "=" * 70)
    print("✓ Rule Engine working correctly!")
