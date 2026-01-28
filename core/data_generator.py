"""
Data Generator Module for Hiring Bias Intelligence Engine

This module generates synthetic hiring candidate data for testing and analysis.
It creates diverse candidate profiles including normal, boundary, and adversarial cases
to stress-test hiring rules and expose potential biases.
"""

import pandas as pd
import numpy as np


def generate_candidates(n_candidates=10000, random_seed=42):
    """
    Generate synthetic hiring candidate data.
    
    Parameters:
    -----------
    n_candidates : int, default=10000
        Number of candidate profiles to generate
    random_seed : int, default=42
        Random seed for reproducibility
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing candidate profiles with the following columns:
        - skill_score: 0-100 (technical/domain skills)
        - years_experience: 0-10 (years of relevant experience)
        - cgpa: 0-10 (cumulative GPA)
        - college_tier: 1, 2, or 3 (tier 1 = top tier)
        - employment_gap: 0-5 (years of employment gap)
        - certifications_count: 0-5 (number of professional certifications)
    """
    np.random.seed(random_seed)
    
    # Calculate distribution sizes
    # 85% normal cases, 10% boundary cases, 5% adversarial cases
    n_normal = int(n_candidates * 0.85)
    n_boundary = int(n_candidates * 0.10)
    n_adversarial = n_candidates - n_normal - n_boundary
    
    # Generate NORMAL CASES (85%)
    # These represent typical candidates with reasonable correlations
    normal_data = _generate_normal_cases(n_normal)
    
    # Generate BOUNDARY CASES (10%)
    # These test edge cases and extreme values
    boundary_data = _generate_boundary_cases(n_boundary)
    
    # Generate ADVERSARIAL CASES (5%)
    # These expose potential biases and rule vulnerabilities
    adversarial_data = _generate_adversarial_cases(n_adversarial)
    
    # Combine all datasets
    all_data = pd.concat([normal_data, boundary_data, adversarial_data], ignore_index=True)
    
    # Shuffle the data to mix different case types
    all_data = all_data.sample(frac=1, random_state=random_seed).reset_index(drop=True)
    
    # Add a candidate ID for tracking
    all_data.insert(0, 'candidate_id', range(1, len(all_data) + 1))
    
    return all_data


def _generate_normal_cases(n):
    """Generate normal/typical candidate profiles."""
    data = {}
    
    # Skill score: Normal distribution centered around 60-70
    data['skill_score'] = np.clip(
        np.random.normal(65, 15, n),
        0, 100
    ).round(1)
    
    # Years of experience: Slightly right-skewed distribution
    data['years_experience'] = np.clip(
        np.random.gamma(3, 1, n),
        0, 10
    ).round(1)
    
    # CGPA: Normal distribution, higher mean (6.5-7.5)
    data['cgpa'] = np.clip(
        np.random.normal(7.0, 1.2, n),
        0, 10
    ).round(2)
    
    # College tier: Weighted towards tier 2
    # Tier 1: 20%, Tier 2: 50%, Tier 3: 30%
    data['college_tier'] = np.random.choice(
        [1, 2, 3],
        size=n,
        p=[0.20, 0.50, 0.30]
    )
    
    # Employment gap: Most candidates have small/no gaps
    # Exponential decay with mean ~0.5 years
    data['employment_gap'] = np.clip(
        np.random.exponential(0.5, n),
        0, 5
    ).round(1)
    
    # Certifications: Poisson distribution (mean = 2)
    data['certifications_count'] = np.clip(
        np.random.poisson(2, n),
        0, 5
    )
    
    return pd.DataFrame(data)


def _generate_boundary_cases(n):
    """Generate boundary/edge case candidate profiles."""
    data = {}
    
    # Mix of extreme values at boundaries
    n_per_type = n // 4
    
    # Type 1: Maximum values (25%)
    max_vals = n_per_type
    data_max = {
        'skill_score': np.full(max_vals, 100.0),
        'years_experience': np.full(max_vals, 10.0),
        'cgpa': np.full(max_vals, 10.0),
        'college_tier': np.ones(max_vals, dtype=int),
        'employment_gap': np.zeros(max_vals),
        'certifications_count': np.full(max_vals, 5)
    }
    
    # Type 2: Minimum values (25%)
    min_vals = n_per_type
    data_min = {
        'skill_score': np.random.uniform(0, 20, min_vals).round(1),
        'years_experience': np.random.uniform(0, 1, min_vals).round(1),
        'cgpa': np.random.uniform(0, 4, min_vals).round(2),
        'college_tier': np.full(min_vals, 3, dtype=int),
        'employment_gap': np.random.uniform(3, 5, min_vals).round(1),
        'certifications_count': np.zeros(min_vals, dtype=int)
    }
    
    # Type 3: High skills, low experience (25%)
    high_low = n_per_type
    data_hl = {
        'skill_score': np.random.uniform(85, 100, high_low).round(1),
        'years_experience': np.random.uniform(0, 2, high_low).round(1),
        'cgpa': np.random.uniform(8, 10, high_low).round(2),
        'college_tier': np.random.choice([1, 2], high_low),
        'employment_gap': np.random.uniform(0, 1, high_low).round(1),
        'certifications_count': np.random.randint(3, 6, high_low)
    }
    
    # Type 4: Low skills, high experience (25% + remainder)
    low_high = n - (max_vals + min_vals + high_low)
    data_lh = {
        'skill_score': np.random.uniform(20, 40, low_high).round(1),
        'years_experience': np.random.uniform(7, 10, low_high).round(1),
        'cgpa': np.random.uniform(5, 7, low_high).round(2),
        'college_tier': np.full(low_high, 3, dtype=int),
        'employment_gap': np.random.uniform(1, 3, low_high).round(1),
        'certifications_count': np.random.randint(0, 3, low_high)
    }
    
    # Combine all boundary types
    df_max = pd.DataFrame(data_max)
    df_min = pd.DataFrame(data_min)
    df_hl = pd.DataFrame(data_hl)
    df_lh = pd.DataFrame(data_lh)
    
    return pd.concat([df_max, df_min, df_hl, df_lh], ignore_index=True)


def _generate_adversarial_cases(n):
    """Generate adversarial cases that expose potential biases and rule vulnerabilities."""
    data = {}
    
    n_per_type = n // 5
    
    # Type 1: Perfect academics, zero practical (20%)
    # Tests if rules over-weight education
    type1 = n_per_type
    data_t1 = {
        'skill_score': np.random.uniform(20, 40, type1).round(1),
        'years_experience': np.zeros(type1),
        'cgpa': np.full(type1, 10.0),
        'college_tier': np.ones(type1, dtype=int),
        'employment_gap': np.zeros(type1),
        'certifications_count': np.zeros(type1, dtype=int)
    }
    
    # Type 2: High skills, tier 3 college (20%)
    # Tests for college tier bias
    type2 = n_per_type
    data_t2 = {
        'skill_score': np.random.uniform(85, 100, type2).round(1),
        'years_experience': np.random.uniform(5, 10, type2).round(1),
        'cgpa': np.random.uniform(7, 9, type2).round(2),
        'college_tier': np.full(type2, 3, dtype=int),
        'employment_gap': np.random.uniform(0, 1, type2).round(1),
        'certifications_count': np.random.randint(3, 6, type2)
    }
    
    # Type 3: Employment gap with strong recovery (20%)
    # Tests bias against career gaps
    type3 = n_per_type
    data_t3 = {
        'skill_score': np.random.uniform(75, 95, type3).round(1),
        'years_experience': np.random.uniform(4, 8, type3).round(1),
        'cgpa': np.random.uniform(7, 9, type3).round(2),
        'college_tier': np.random.choice([1, 2], type3),
        'employment_gap': np.random.uniform(3, 5, type3).round(1),
        'certifications_count': np.random.randint(4, 6, type3)
    }
    
    # Type 4: Low CGPA, high everything else (20%)
    # Tests CGPA bias
    type4 = n_per_type
    data_t4 = {
        'skill_score': np.random.uniform(80, 100, type4).round(1),
        'years_experience': np.random.uniform(6, 10, type4).round(1),
        'cgpa': np.random.uniform(4, 6, type4).round(2),
        'college_tier': np.random.choice([1, 2], type4),
        'employment_gap': np.random.uniform(0, 1, type4).round(1),
        'certifications_count': np.random.randint(3, 6, type4)
    }
    
    # Type 5: Mixed anomalies (20% + remainder)
    # Random contradictory profiles
    type5 = n - (type1 + type2 + type3 + type4)
    data_t5 = {
        'skill_score': np.random.uniform(0, 100, type5).round(1),
        'years_experience': np.random.uniform(0, 10, type5).round(1),
        'cgpa': np.random.uniform(0, 10, type5).round(2),
        'college_tier': np.random.choice([1, 2, 3], type5),
        'employment_gap': np.random.uniform(0, 5, type5).round(1),
        'certifications_count': np.random.randint(0, 6, type5)
    }
    
    # Combine all adversarial types
    df_t1 = pd.DataFrame(data_t1)
    df_t2 = pd.DataFrame(data_t2)
    df_t3 = pd.DataFrame(data_t3)
    df_t4 = pd.DataFrame(data_t4)
    df_t5 = pd.DataFrame(data_t5)
    
    return pd.concat([df_t1, df_t2, df_t3, df_t4, df_t5], ignore_index=True)


def get_data_summary(df):
    """
    Get a comprehensive summary of the generated candidate data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The candidate data DataFrame
        
    Returns:
    --------
    dict
        Dictionary containing summary statistics
    """
    summary = {
        'total_candidates': len(df),
        'feature_statistics': df.describe().to_dict(),
        'college_tier_distribution': df['college_tier'].value_counts().to_dict(),
        'missing_values': df.isnull().sum().to_dict()
    }
    return summary


if __name__ == "__main__":
    # Example usage and testing
    print("Generating 10,000 synthetic hiring candidates...")
    candidates_df = generate_candidates(n_candidates=10000)
    
    print(f"\nGenerated {len(candidates_df)} candidates")
    print("\nFirst 10 candidates:")
    print(candidates_df.head(10))
    
    print("\nData Summary:")
    print(candidates_df.describe())
    
    print("\nCollege Tier Distribution:")
    print(candidates_df['college_tier'].value_counts().sort_index())
    
    print("\nData shape:", candidates_df.shape)
    print("Columns:", list(candidates_df.columns))
    
    # Verify ranges
    print("\n=== Verification ===")
    print(f"Skill score range: {candidates_df['skill_score'].min():.1f} - {candidates_df['skill_score'].max():.1f}")
    print(f"Years experience range: {candidates_df['years_experience'].min():.1f} - {candidates_df['years_experience'].max():.1f}")
    print(f"CGPA range: {candidates_df['cgpa'].min():.2f} - {candidates_df['cgpa'].max():.2f}")
    print(f"College tier values: {sorted(candidates_df['college_tier'].unique())}")
    print(f"Employment gap range: {candidates_df['employment_gap'].min():.1f} - {candidates_df['employment_gap'].max():.1f}")
    print(f"Certifications range: {candidates_df['certifications_count'].min()} - {candidates_df['certifications_count'].max()}")
