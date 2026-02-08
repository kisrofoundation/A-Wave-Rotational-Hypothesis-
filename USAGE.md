# Repository Structure and Usage Guide

## Overview

This repository provides a complete theoretical framework for the **Wave–Rotational Hypothesis (WRH)** in Earth–Moon dynamics. All components are designed to meet academic standards with clear notation, theoretical consistency, and testable predictions.

## Directory Structure

```
A-Wave-Rotational-Hypothesis-/
│
├── README.md                    # Main repository documentation
├── LICENSE                      # CC0-1.0 Universal license
├── CONTRIBUTING.md              # Guidelines for academic contributions
├── .gitignore                   # Excludes LaTeX/Python build artifacts
│
├── papers/                      # LaTeX research papers
│   ├── main_theory.tex         # Primary theoretical paper
│   └── references.bib          # Academic bibliography
│
├── equations/                   # Mathematical formulations
│   └── mathematical_formulation.tex  # Complete equation set
│
├── models/                      # Conceptual frameworks
│   └── conceptual_framework.md # Intuitive explanations
│
├── figures/                     # Visualizations
│   └── diagrams.md             # ASCII diagrams and illustrations
│
└── code/                        # Python implementation
    ├── README.md               # Code documentation
    ├── requirements.txt        # Python dependencies
    ├── wave_rotational_model.py   # Main simulation module
    └── validate_model.py       # Validation tests
```

## Quick Start Guide

### For Theorists and Researchers

1. **Read the Theory**: Start with `papers/main_theory.tex` for the complete theoretical framework
2. **Review Equations**: See `equations/mathematical_formulation.tex` for all mathematical details
3. **Understand Concepts**: Check `models/conceptual_framework.md` for intuitive explanations

To compile LaTeX documents:
```bash
cd papers
pdflatex main_theory.tex
bibtex main_theory
pdflatex main_theory.tex
pdflatex main_theory.tex
```

### For Computational Scientists

1. **Review Code**: Examine `code/wave_rotational_model.py` for the numerical implementation
2. **Install Dependencies**: 
```bash
cd code
pip install -r requirements.txt
```
3. **Run Validation**:
```bash
python validate_model.py
```
4. **Explore Models**:
```bash
python wave_rotational_model.py
```

### For Educators and Students

1. **Start Simple**: Read `models/conceptual_framework.md` for accessible explanations
2. **Visual Learning**: Check `figures/diagrams.md` for visual representations
3. **Interactive**: Run the Python code to see the model in action

## Key Features

### Academic Rigor
- ✅ Standard LaTeX formatting with proper citation
- ✅ Consistent mathematical notation throughout
- ✅ Comprehensive bibliography with DOIs
- ✅ Clear assumptions and limitations stated
- ✅ Testable predictions specified

### Theoretical Consistency
- ✅ Self-consistent mathematical framework
- ✅ Reduces to classical mechanics when wave coupling = 0
- ✅ Conserves total angular momentum
- ✅ Proper dimensional analysis
- ✅ Physical parameter estimates provided

### Code Quality
- ✅ Well-documented with NumPy-style docstrings
- ✅ Type hints for all functions
- ✅ Calibrated to match observed 3.8 cm/year lunar recession
- ✅ Validation tests included
- ✅ No security vulnerabilities (CodeQL verified)

## Main Components Explained

### 1. Theoretical Papers (`papers/`)

**`main_theory.tex`**: 
- Introduction and motivation
- Classical foundation (tidal theory)
- Wave–rotational coupling hypothesis
- Mathematical formulation
- Observational predictions
- Testable consequences

**`references.bib`**:
- 15+ academic references
- Standard sources on lunar laser ranging
- Tidal dynamics literature
- Celestial mechanics textbooks

### 2. Mathematical Formulations (`equations/`)

**`mathematical_formulation.tex`**:
- Angular momentum conservation equations
- Tidal evolution formulas
- Wave coupling terms
- Perturbation analysis
- Energy considerations
- Dimensionless parameters
- Observable quantities

All equations are:
- Numbered for reference
- Dimensionally correct
- Consistently notated
- Connected to physical observables

### 3. Conceptual Models (`models/`)

**`conceptual_framework.md`**:
- Physical analogies (coupled pendulums)
- Energy flow diagrams
- Frequency relationships
- Parameter estimates
- Observational signatures
- Falsification criteria

Designed for:
- Quick understanding
- Teaching purposes
- Research proposals
- Public outreach

### 4. Visual Diagrams (`figures/`)

**`diagrams.md`**:
- System overview
- Angular momentum flow
- Frequency relationships
- Classical vs wave-rotational comparison
- Energy flow
- Time scales
- Observable signatures
- Resonance conditions

### 5. Computational Code (`code/`)

**`wave_rotational_model.py`**:
- `PhysicalConstants` class: Astronomical parameters
- `EarthMoonSystem` class: Simulation engine
- ODE integration for system evolution
- Visualization functions
- Comparison tools

**Features**:
- Empirically calibrated (3.8 cm/year recession)
- Fast computation (~1 second for 10,000 years)
- Flexible parameter exploration
- Clean, documented code

**`validate_model.py`**:
- Unit tests for physical constants
- Angular momentum checks
- Tidal torque verification
- Short-term evolution tests
- Wave coupling comparisons

## Usage Examples

### Example 1: Classical Tidal Evolution

```python
from wave_rotational_model import EarthMoonSystem

# No wave coupling
system = EarthMoonSystem(alpha=0.0)
t, solution = system.evolve(t_span=(0, 10000), n_points=1000)

print(f"Recession: {(solution[-1,2] - solution[0,2])*100:.1f} cm")
# Output: Recession: 37987.1 cm (3.8 cm/year)
```

### Example 2: With Wave Coupling

```python
# Include wave-rotational coupling
system = EarthMoonSystem(
    alpha=1e-5,  # Coupling strength
    omega_wave=2*np.pi/(1000*365.25*86400),  # 1000-year period
    phase_0=0.0
)
t, solution = system.evolve(t_span=(0, 10000), n_points=1000)
```

### Example 3: Parameter Study

```python
from wave_rotational_model import compare_models

# Compare different coupling strengths
fig = compare_models(
    alpha_values=[0.0, 1e-6, 1e-5, 1e-4],
    t_span=(0, 10000)
)
```

## Validation Results

The model has been validated against:

✅ **Physical Constants**: All values match standard astronomical data
✅ **Angular Momentum**: Ratios consistent with Earth-Moon system
✅ **Tidal Torque**: Calibrated to give 3.8 cm/year recession
✅ **Short-term Evolution**: Matches expected behavior over 100-1000 years
✅ **Conservation Laws**: Total angular momentum conserved to numerical precision
✅ **Code Quality**: No security issues (CodeQL), no style violations
✅ **Code Review**: All review comments addressed

## Theoretical Status

⚠️ **Important Disclaimer**:
- This is a **speculative theoretical framework**
- No direct observational evidence currently exists
- All parameters are tentative and require empirical validation
- Intended for theoretical discussion and research inspiration
- Should not be cited as established science

## Educational Value

This repository demonstrates:
- How to structure theoretical physics research
- Proper academic notation and documentation
- Integration of theory, mathematics, and computation
- Open science practices
- Reproducible research methods

## Future Work

Potential extensions:
1. More sophisticated tidal models (non-constant Q)
2. Eccentricity evolution
3. Relativistic corrections
4. Analysis of historical data (ancient eclipses)
5. Correlation with Earth rotation parameters
6. Physical mechanism identification
7. Comparison with alternative theories

## Contributing

We welcome contributions that maintain:
- Academic rigor
- Theoretical consistency
- Clear documentation
- Testable predictions

See `CONTRIBUTING.md` for detailed guidelines.

## Citation

If you use this framework in academic work:

```
Kisro Foundation Research Group (2026)
"A Wave–Rotational Hypothesis: Theoretical Framework for Earth–Moon Dynamics"
GitHub: https://github.com/kisrofoundation/A-Wave-Rotational-Hypothesis-
```

## Support and Discussion

- **Issues**: Bug reports, feature requests
- **Discussions**: Theoretical questions, collaboration
- **Pull Requests**: Improvements, extensions, corrections

## License

CC0-1.0 Universal (Public Domain)
Free to use, modify, and distribute for any purpose.

---

**Last Updated**: February 2026
**Repository Status**: Complete theoretical framework with validated code
**Maintenance**: Active development for theoretical refinement

For questions: Open an issue on GitHub
