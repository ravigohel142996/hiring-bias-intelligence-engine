"""
Example usage of the data generator module.

This script demonstrates how to use the data generator to create
synthetic hiring candidate data for testing and analysis.
"""

from core.data_generator import generate_candidates, get_data_summary

# Example 1: Generate default dataset (10,000 candidates)
print("=" * 60)
print("Example 1: Generate 10,000 candidates with default settings")
print("=" * 60)

candidates = generate_candidates()
print(f"\nGenerated {len(candidates)} candidates")
print("\nFirst 5 candidates:")
print(candidates.head())

# Example 2: Generate smaller dataset for testing
print("\n" + "=" * 60)
print("Example 2: Generate smaller dataset (100 candidates)")
print("=" * 60)

small_dataset = generate_candidates(n_candidates=100, random_seed=123)
print(f"\nGenerated {len(small_dataset)} candidates")
print("\nStatistics:")
print(small_dataset.describe())

# Example 3: Get data summary
print("\n" + "=" * 60)
print("Example 3: Get comprehensive data summary")
print("=" * 60)

summary = get_data_summary(candidates)
print(f"\nTotal candidates: {summary['total_candidates']}")
print(f"\nCollege tier distribution:")
for tier, count in sorted(summary['college_tier_distribution'].items()):
    print(f"  Tier {tier}: {count} candidates")

# Example 4: Export to CSV
print("\n" + "=" * 60)
print("Example 4: Export data to CSV")
print("=" * 60)

output_file = '/tmp/hiring_candidates.csv'
candidates.to_csv(output_file, index=False)
print(f"\nData exported to: {output_file}")
print(f"File contains {len(candidates)} rows and {len(candidates.columns)} columns")

# Example 5: Filter and analyze specific cases
print("\n" + "=" * 60)
print("Example 5: Analyze adversarial patterns")
print("=" * 60)

# High skills with tier 3 college (potential bias case)
high_skill_tier3 = candidates[
    (candidates['skill_score'] >= 85) & 
    (candidates['college_tier'] == 3)
]
print(f"\nHigh skill + Tier 3 college: {len(high_skill_tier3)} candidates")
print("These cases test for college tier bias in hiring rules")

# Employment gap with strong skills
gap_with_skills = candidates[
    (candidates['employment_gap'] >= 3) & 
    (candidates['skill_score'] >= 75)
]
print(f"\nLarge employment gap + High skills: {len(gap_with_skills)} candidates")
print("These cases test bias against career gaps")

# Perfect academics, low skills
perfect_academic_low_skill = candidates[
    (candidates['cgpa'] == 10) & 
    (candidates['skill_score'] < 50)
]
print(f"\nPerfect CGPA + Low skills: {len(perfect_academic_low_skill)} candidates")
print("These cases test if rules over-weight education vs practical skills")

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
