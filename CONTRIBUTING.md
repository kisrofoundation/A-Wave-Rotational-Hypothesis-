# Contributing to the Wave–Rotational Hypothesis Project

Thank you for your interest in contributing to this theoretical research project! This document provides guidelines for making contributions that maintain academic rigor, theoretical consistency, and clarity.

## Guiding Principles

All contributions should prioritize:

1. **Clarity** - Mathematical notation, explanations, and code should be clear and accessible
2. **Academic Notation** - Use standard conventions from physics and astronomy literature
3. **Theoretical Consistency** - Ensure all additions are self-consistent with the existing framework
4. **Testability** - Favor formulations that lead to testable predictions
5. **Documentation** - All work should be well-documented and reproducible

## Types of Contributions

### 1. Mathematical Formulations

**LaTeX documents in `papers/` and `equations/`**

When contributing mathematical content:
- Use standard LaTeX packages (`amsmath`, `amssymb`, `mathtools`)
- Define all symbols clearly before first use
- Number all equations for reference
- Include dimensional analysis where appropriate
- Cite relevant literature using `\cite{}`

**Notation conventions:**
- Use bold for vectors: `\mathbf{L}` for angular momentum vectors
- Use subscripts for components: `L_{\text{orb}}`, `L_{\text{rot}}`
- Use `\omega` for angular frequencies, `\Omega` for solid angles
- Use SI units unless otherwise specified

**Example structure:**
```latex
\subsection{New Theoretical Result}

Consider the interaction term:
\begin{equation}
\Gamma_{\text{new}} = f(L_{\text{orb}}, L_{\text{rot}})
\label{eq:new_torque}
\end{equation}

where $f$ is a function to be determined by...
```

### 2. Conceptual Models

**Markdown documents in `models/`**

When contributing conceptual explanations:
- Use clear analogies from everyday experience or well-known physics
- Include ASCII diagrams or describe figures clearly
- Provide order-of-magnitude estimates
- Connect to the mathematical formalism
- Explain implications for observations

**Structure guidelines:**
- Start with overview
- Build from simple to complex
- Use bullet points and numbered lists
- Include tables for parameter comparisons
- End with testable predictions

### 3. Computational Code

**Python scripts in `code/`**

When contributing code:
- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Include comprehensive docstrings (NumPy style)
- Add inline comments for complex algorithms
- Ensure all physical constants are documented with units
- Include example usage in `if __name__ == "__main__"` blocks

**Docstring template:**
```python
def calculate_torque(L_orb: float, L_rot: float, alpha: float) -> float:
    """
    Calculate wave-mediated torque.
    
    Parameters
    ----------
    L_orb : float
        Orbital angular momentum [kg m^2 s^-1]
    L_rot : float
        Rotational angular momentum [kg m^2 s^-1]
    alpha : float
        Dimensionless coupling strength
        
    Returns
    -------
    float
        Torque magnitude [N m]
        
    Notes
    -----
    Based on equation (X) in main_theory.tex
    """
    # Implementation
```

**Dependencies:**
- Prefer standard scientific Python stack: `numpy`, `scipy`, `matplotlib`
- Document all required packages
- Keep dependencies minimal

### 4. Figures and Visualizations

**Images in `figures/`**

When adding figures:
- Use vector formats when possible (PDF, SVG)
- Include source files (e.g., Python scripts that generate plots)
- Label axes clearly with units
- Use consistent color schemes
- Add descriptive captions
- Reference figures in documentation

## Submission Process

### Before Submitting

1. **Check consistency** - Ensure your contribution is consistent with existing theoretical framework
2. **Test code** - Run all Python scripts to verify they execute without errors
3. **Compile LaTeX** - Verify all LaTeX documents compile successfully
4. **Review notation** - Check that mathematical notation follows conventions
5. **Add documentation** - Update README or add comments as needed

### Submitting Changes

1. **Fork the repository** (if you're not a direct collaborator)
2. **Create a descriptive branch** - e.g., `add-energy-derivation` or `improve-numerical-stability`
3. **Make focused changes** - Keep contributions atomic and well-scoped
4. **Write clear commit messages**:
   ```
   Add derivation of wave energy density
   
   - Extends section 3.2 of main_theory.tex
   - Includes dimensional analysis
   - References equation 15 from mathematical_formulation.tex
   ```
5. **Open a pull request** with:
   - Clear description of changes
   - Motivation for the contribution
   - How it maintains theoretical consistency
   - Any new predictions or testable consequences

## Code Review Criteria

Contributions will be reviewed for:

### Mathematical Content
- [ ] Correct derivations
- [ ] Consistent notation
- [ ] Proper dimensional analysis
- [ ] Clear definitions of new terms
- [ ] References to literature where appropriate

### Code Quality
- [ ] Follows style guidelines
- [ ] Includes type hints
- [ ] Has comprehensive docstrings
- [ ] Passes basic tests
- [ ] Produces expected output

### Documentation
- [ ] Clear explanations
- [ ] Proper academic tone
- [ ] Connects to existing framework
- [ ] Includes examples or use cases

### Theoretical Consistency
- [ ] Self-consistent with existing equations
- [ ] Reduces to classical results in appropriate limits
- [ ] Makes testable predictions
- [ ] Acknowledges assumptions and limitations

## Areas for Contribution

We particularly welcome contributions in these areas:

### High Priority
1. **Physical mechanisms** - Proposed origins of the wave field
2. **Parameter estimation** - Better constraints on coupling strength α
3. **Observational analysis** - Analysis of LLR or Earth rotation data
4. **Alternative formulations** - Different mathematical approaches

### Medium Priority
1. **Numerical improvements** - More efficient integration schemes
2. **Visualization tools** - Better plots and diagrams
3. **Educational materials** - Tutorials or explanatory documents
4. **Error analysis** - Uncertainty propagation in calculations

### Nice to Have
1. **Historical context** - Similar hypotheses in literature
2. **Comparative studies** - How WRH compares to other extensions
3. **Philosophical analysis** - Nature of theoretical exploration
4. **Outreach materials** - Simplified explanations for general audience

## Questions and Discussion

- **General questions** - Open a GitHub issue
- **Theoretical discussions** - Use GitHub Discussions
- **Bug reports** - Open an issue with "bug" label
- **Feature requests** - Open an issue with "enhancement" label

## Academic Integrity

All contributions must:
- Acknowledge prior work appropriately
- Cite relevant literature
- Not plagiarize from other sources
- Clearly distinguish original work from existing results
- Maintain scholarly ethics

## Code of Conduct

We are committed to providing a welcoming and respectful environment:
- Be respectful in all interactions
- Focus on theoretical merit, not personalities
- Welcome constructive criticism
- Acknowledge contributions from others
- Maintain professional scientific discourse

## Recognition

Contributors will be acknowledged in:
- Repository CONTRIBUTORS file
- Relevant documentation sections
- Academic citations (for substantial contributions)

## License

By contributing, you agree that your contributions will be licensed under the same CC0-1.0 license as the project.

---

Thank you for helping advance this theoretical exploration!

**Questions?** Open an issue or start a discussion.
