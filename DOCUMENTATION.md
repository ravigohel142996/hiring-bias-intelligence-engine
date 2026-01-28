# Hiring Bias Intelligence Engine - Complete Documentation

## 🎯 Overview

A production-ready decision intelligence platform that stress-tests hiring rules under scale, bias, and adversarial scenarios. This system simulates thousands of candidate profiles, applies human-defined hiring rules, and uses ML to expose hidden bias amplification, rule dominance & collapse, and unstable decision boundaries.

**⚠️ Not an ATS. Not automation. This is a decision audit system.**

---

## 📁 Project Structure

```
hiring-bias-intelligence-engine/
├── core/                          # Core engine modules
│   ├── data_generator.py         # Synthetic candidate generation
│   ├── rule_engine.py            # Rule-based decision engine
│   ├── bias_analyzer.py          # Bias detection with KMeans
│   ├── collapse_simulator.py    # Rule stability testing
│   ├── metrics.py                # Metrics calculations
│   └── __init__.py               # Module exports
│
├── ui/                            # Dashboard UI modules
│   ├── theme.py                  # Dark glassmorphism theme
│   ├── animations.py             # CSS animations
│   ├── components.py             # Reusable components
│   └── __init__.py               # Module exports
│
├── assets/                        # Static assets
│   ├── css/                      # Additional stylesheets
│   └── images/                   # Images and icons
│
├── app.py                         # Main Streamlit application
├── requirements.txt               # Python dependencies
├── render.yaml                    # Deployment configuration
├── .gitignore                     # Git ignore rules
└── README.md                      # Project overview
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ravigohel142996/hiring-bias-intelligence-engine.git
cd hiring-bias-intelligence-engine

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Docker Deployment (Optional)

```bash
docker build -t bias-engine .
docker run -p 8501:8501 bias-engine
```

### Render.com Deployment

1. Push code to GitHub
2. Connect Render.com to your repository
3. Deploy using `render.yaml` configuration
4. Access your live dashboard!

---

## 💡 Key Features

### 1. Data Generator
- Generates 10,000 synthetic candidates
- 85% normal cases, 10% boundary cases, 5% adversarial cases
- 6 features: skill_score, years_experience, cgpa, college_tier, employment_gap, certifications_count
- Fully reproducible with random seeds

### 2. Rule Engine
- Evaluates candidates against 5 hiring rules:
  - skill_score >= 65
  - cgpa >= 7.0
  - years_experience >= 1
  - employment_gap <= 2
  - college_tier == 1 (bonus)
- Returns ACCEPT, REVIEW, or REJECT decisions
- Tracks which rules fired for each candidate

### 3. Bias Analyzer
- KMeans clustering (5 groups by default)
- Calculates acceptance rates per cluster
- Identifies proxy biases:
  - College tier discrimination
  - Employment gap penalties
- Flags rules with >20% disparity
- Generates fairness scores

### 4. Collapse Simulator
- Tests 10 perturbation scenarios
- Measures decision flips and stability
- Calculates acceptance rate shifts
- Identifies unstable decision regions
- Overall stability score (higher = more stable)

### 5. Interactive Dashboard
- **Overview Page**: Key metrics and decision distribution
- **Bias Heatmap**: Acceptance rates across groups
- **Rule Impact**: Impact analysis for each rule
- **Collapse Simulation**: Stability testing results
- **Insights**: AI-generated recommendations

---

## 📊 Dashboard Pages

### Overview
- Total candidates count
- Overall acceptance rate
- Fairness score (lower is better)
- System stability score
- Decision distribution pie chart
- Bias detection summary

### Bias Heatmap
- Acceptance rates by cluster (bar chart)
- College tier vs employment gap matrix
- List of flagged biased rules
- Severity ratings (high/medium)

### Rule Impact
- Impact score for each rule
- Pass/fail acceptance rates
- Visual comparison of rule effectiveness
- Detailed rule statistics

### Collapse Simulation
- Stability scores across scenarios
- Decision flip counts
- Acceptance rate shifts
- Unstable candidate identification
- Scenario-by-scenario breakdown

### Insights & Recommendations
- AI-generated key findings
- Bias warnings
- Stability alerts
- Actionable recommendations
- System health summary

---

## 🎨 UI Features

### Dark Glassmorphism Theme
- Backdrop blur effects
- Gradient backgrounds
- Soft shadows
- Smooth transitions
- Hover glow effects

### Animations
- Fade-in on page load
- Card slide-up animations
- Smooth section transitions
- Loading spinners
- Status badges

### Responsive Design
- **Mobile** (<768px): Single-column stacked layout
- **Tablet** (768-1024px): Dual-column layout
- **Desktop** (>1024px): Multi-column dashboard
- Touch-friendly (44px minimum targets)
- Reduced animations on mobile
- Responsive charts

---

## 🔧 Configuration

### Rule Engine Configuration

```python
from core import HiringRuleEngine

engine = HiringRuleEngine()

# Update rule thresholds
engine.update_rules({
    'skill_score_min': 70,    # Raise skill requirement
    'cgpa_min': 7.5,          # Raise CGPA requirement
    'experience_min': 2,      # Require more experience
    'gap_max': 1,             # Reduce acceptable gap
    'tier_1_bonus': False     # Disable tier bonus
})
```

### Bias Analyzer Configuration

```python
from core import BiasAnalyzer

# Configure number of clusters
analyzer = BiasAnalyzer(n_clusters=7)

# Analyze results
results_with_clusters = analyzer.cluster_candidates(results)
bias_report = analyzer.generate_bias_report(results_with_clusters)
```

### Data Generator Configuration

```python
from core import generate_candidates

# Generate custom dataset
candidates = generate_candidates(
    n_candidates=5000,    # Number of candidates
    random_seed=123       # Seed for reproducibility
)
```

---

## 📈 Metrics & Scoring

### Fairness Score
- Standard deviation of acceptance rates across clusters
- Lower scores indicate more fairness
- Threshold: < 10 is considered fair

### Stability Score
- Percentage of decisions that remain unchanged under perturbations
- Higher scores indicate more stable rules
- Threshold: > 80% is considered stable

### Impact Score
- Difference in acceptance rates when a rule passes vs fails
- Positive: rule increases acceptance
- Negative: rule decreases acceptance
- Magnitude indicates strength of impact

### Bias Detection
- **College Tier Bias**: > 15% disparity triggers flag
- **Employment Gap Bias**: > 20% penalty triggers flag
- **Rule Disparity**: > 20% difference triggers flag

---

## 🧪 Testing

### Run All Tests

```bash
# Test core modules
python -m pytest tests/test_core.py

# Test UI components
python -m pytest tests/test_ui.py

# Run integration tests
python -m pytest tests/test_integration.py
```

### Manual Testing

```python
# Test data generation
from core import generate_candidates
candidates = generate_candidates(100, random_seed=42)
assert len(candidates) == 100

# Test rule engine
from core import HiringRuleEngine
engine = HiringRuleEngine()
results = engine.evaluate_batch(candidates)
assert 'decision' in results.columns

# Test bias analysis
from core import BiasAnalyzer
analyzer = BiasAnalyzer(n_clusters=3)
bias_report = analyzer.generate_bias_report(results)
assert 'overall_acceptance_rate' in bias_report
```

---

## 🔐 Security

- ✅ CodeQL security scan: 0 vulnerabilities
- ✅ No hardcoded secrets
- ✅ Input validation on all parameters
- ✅ Safe DataFrame operations
- ✅ No SQL injection risks (no database)
- ✅ XSS prevention in Streamlit

---

## 📱 Mobile Support

### Responsive Features
- Single-column layout on mobile
- Full-width buttons
- Large touch targets (44px minimum)
- Optimized font sizes
- Reduced animations for performance
- Horizontal scroll prevention

### Tested Devices
- ✅ iPhone (Safari, Chrome)
- ✅ Android (Chrome, Firefox)
- ✅ iPad (Safari, Chrome)
- ✅ Desktop (Chrome, Firefox, Safari, Edge)

---

## 🎯 Use Cases

### 1. Audit Existing Hiring Rules
- Import your current rules
- Test against synthetic candidates
- Identify hidden biases
- Measure fairness and stability

### 2. Test New Rule Changes
- Modify rule thresholds
- Run simulations
- Compare outcomes
- Validate before deployment

### 3. Compliance Checking
- Generate bias reports
- Document fairness metrics
- Export audit trails
- Demonstrate due diligence

### 4. Training & Education
- Demonstrate bias amplification
- Show rule interactions
- Teach fairness concepts
- Interactive learning tool

---

## 🤝 Contributing

### Development Setup

```bash
# Clone and install
git clone <repo-url>
cd hiring-bias-intelligence-engine
pip install -r requirements.txt

# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
python -m pytest

# Commit and push
git commit -m "Add: your feature"
git push origin feature/your-feature
```

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Write tests
- Update documentation

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👥 Credits

Built with:
- **Streamlit** - Dashboard framework
- **Plotly** - Interactive charts
- **scikit-learn** - Machine learning
- **pandas** - Data manipulation
- **NumPy** - Numerical computing

---

## 📞 Support

- 📧 Email: support@bias-engine.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📖 Docs: Full documentation at `/docs`

---

## 🗺️ Roadmap

### v2.0 (Planned)
- [ ] Real-time rule editing
- [ ] Custom rule builder UI
- [ ] Export to PDF reports
- [ ] API endpoints
- [ ] Multi-language support

### v2.1 (Future)
- [ ] Historical trend analysis
- [ ] A/B testing framework
- [ ] Integration with ATS systems
- [ ] Advanced ML models
- [ ] Team collaboration features

---

**⚡ Ready to audit your hiring decisions? Deploy now and start testing!**
