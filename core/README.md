# Data Generator Module

This module generates synthetic hiring candidate data for testing bias detection and rule validation in hiring systems.

## Overview

The data generator creates realistic candidate profiles with controlled distributions to test hiring algorithms for potential biases and rule vulnerabilities.

## Features

Generates 10,000 synthetic candidates (configurable) with the following attributes:

- **skill_score** (0-100): Technical and domain skills assessment
- **years_experience** (0-10): Years of relevant work experience
- **cgpa** (0-10): Cumulative Grade Point Average
- **college_tier** (1, 2, 3): Educational institution tier (1 = top tier)
- **employment_gap** (0-5): Years of career gaps
- **certifications_count** (0-5): Number of professional certifications

## Data Distribution

The generator creates three types of candidate profiles:

### Normal Cases (85%)
Typical candidates with realistic distributions and correlations:
- Skill scores: Normal distribution (mean ~65, std ~15)
- Experience: Gamma distribution (slightly right-skewed)
- CGPA: Normal distribution (mean ~7.0, std ~1.2)
- College tier: Weighted (20% tier 1, 50% tier 2, 30% tier 3)
- Employment gap: Exponential distribution (most have small/no gaps)
- Certifications: Poisson distribution (mean ~2)

### Boundary Cases (10%)
Edge cases testing extreme values:
- Perfect candidates (100 skill, 10 years exp, 10 CGPA)
- Minimal qualifications (low skills, low experience)
- High skills with low experience
- Low skills with high experience

### Adversarial Cases (5%)
Profiles designed to expose specific biases:
- Perfect academics with zero practical skills (education bias)
- High skills from tier 3 colleges (college tier bias)
- Career gaps with strong recovery (employment gap bias)
- Low CGPA with high everything else (CGPA bias)
- Mixed anomalies (contradictory profiles)

## Usage

### Basic Usage

```python
from core.data_generator import generate_candidates

# Generate default dataset (10,000 candidates)
candidates = generate_candidates()
print(candidates.head())
```

### Custom Configuration

```python
# Generate smaller dataset with custom seed
candidates = generate_candidates(n_candidates=1000, random_seed=123)
```

### Get Data Summary

```python
from core.data_generator import get_data_summary

summary = get_data_summary(candidates)
print(f"Total candidates: {summary['total_candidates']}")
print(f"College tier distribution: {summary['college_tier_distribution']}")
```

### Export to CSV

```python
candidates.to_csv('hiring_candidates.csv', index=False)
```

### Filter Specific Cases

```python
# Find high-skill candidates from tier 3 colleges
bias_test_cases = candidates[
    (candidates['skill_score'] >= 85) & 
    (candidates['college_tier'] == 3)
]

# Find candidates with employment gaps but strong skills
gap_cases = candidates[
    (candidates['employment_gap'] >= 3) & 
    (candidates['skill_score'] >= 75)
]
```

## Example Output

```
   candidate_id  skill_score  years_experience  cgpa  college_tier  employment_gap  certifications_count
0             1         74.4               2.1  7.11             2             0.4                     1
1             2         46.9               2.5  7.58             2             0.3                     2
2             3         56.9               0.9  6.09             2             1.8                     2
```

## Reproducibility

The generator uses `RandomState` for full reproducibility. Using the same seed will always produce identical datasets:

```python
df1 = generate_candidates(random_seed=42)
df2 = generate_candidates(random_seed=42)
assert df1.equals(df2)  # True
```

## Testing Your Hiring Rules

Use this data to:

1. **Detect Bias**: Test if your rules discriminate based on college tier, employment gaps, or other protected attributes
2. **Validate Edge Cases**: Ensure your rules handle extreme values appropriately
3. **Stress Test**: Verify rule stability with contradictory candidate profiles
4. **Measure Fairness**: Compare acceptance rates across different candidate segments

## Running the Examples

```bash
python examples_usage.py
```

## Implementation Details

- Uses numpy for statistical distributions
- Returns pandas DataFrame for easy manipulation
- Validates input/output data
- Includes comprehensive docstrings
- Thread-safe random number generation

## Validation

Generated data is validated to ensure:
- All values within specified ranges
- No missing values
- Correct data types
- Expected distributions
- Reproducible with random seeds
