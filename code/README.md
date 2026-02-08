# Code: Numerical Implementation

This directory contains Python code for numerical calculations and simulations related to the wave–rotational hypothesis.

## Files

- **`wave_rotational_model.py`** - Main module with classes and functions for modeling Earth-Moon dynamics

## Requirements

```bash
pip install numpy scipy matplotlib
```

Or use:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from wave_rotational_model import EarthMoonSystem, PhysicalConstants

# Classical tidal evolution (no wave coupling)
system = EarthMoonSystem(alpha=0.0)
t, solution = system.evolve(t_span=(0, 10000), n_points=1000)

print(f"Lunar recession over 10,000 years: {(solution[-1, 2] - solution[0, 2])*100:.2f} cm")
```

### With Wave Coupling

```python
# Include wave-rotational coupling
system = EarthMoonSystem(
    alpha=1e-5,  # Coupling strength
    omega_wave=2*np.pi/(1000*365.25*86400),  # 1000 year period
    phase_0=0.0  # Initial phase
)

t, solution = system.evolve(t_span=(0, 10000), n_points=1000)
```

### Comparing Models

```python
from wave_rotational_model import compare_models

# Compare different coupling strengths
fig = compare_models(
    alpha_values=[0.0, 1e-6, 1e-5],
    t_span=(0, 10000)
)
fig.savefig('model_comparison.png', dpi=300)
```

## Running Examples

Execute the main module to run built-in examples:

```bash
python wave_rotational_model.py
```

This will:
1. Calculate classical tidal evolution
2. Calculate wave-coupled evolution
3. Print numerical results
4. Note that plots won't be displayed in headless environments

## Module Documentation

### Classes

#### `PhysicalConstants`
Contains standard physical and astronomical constants:
- Gravitational constant `G`
- Earth and Moon masses, radii
- Current orbital parameters
- Tidal parameters

#### `EarthMoonSystem`
Main simulation class for Earth-Moon dynamics.

**Initialization:**
```python
system = EarthMoonSystem(alpha=0.0, omega_wave=..., phase_0=0.0)
```

**Methods:**
- `orbital_angular_momentum(a, e)` - Calculate orbital angular momentum
- `tidal_torque(a)` - Calculate classical tidal torque
- `wave_torque(L_orb, L_rot, t)` - Calculate wave-mediated torque
- `evolve(t_span, n_points)` - Integrate system evolution

### Functions

#### `plot_evolution(t, solution, title)`
Create a 3-panel plot showing:
- Orbital angular momentum vs time
- Rotational angular momentum vs time
- Semi-major axis vs time

#### `compare_models(alpha_values, t_span)`
Generate comparison plots for multiple coupling strengths.

## Physical Parameters

Current Earth-Moon system values (from `PhysicalConstants`):

| Parameter | Value | Units |
|-----------|-------|-------|
| Earth mass | 5.972×10²⁴ | kg |
| Moon mass | 7.342×10²² | kg |
| Earth radius | 6.371×10⁶ | m |
| Semi-major axis | 3.844×10⁸ | m |
| Orbital period | 27.322 | days |
| Earth rotation | 1.0 | day |
| Love number k₂ | 0.299 | - |
| Tidal lag | 2.16×10⁻² | rad |

## Numerical Methods

The code uses:
- **ODE Integration**: `scipy.integrate.odeint` for solving coupled differential equations
- **Time stepping**: Adaptive step size for numerical stability
- **Initial conditions**: Based on current Earth-Moon system

### Equations Solved

The system evolves according to:

```
dL_orb/dt = -Γ_tidal + Γ_wave
dL_rot/dt = +Γ_tidal - Γ_wave
da/dt = (2a²/μGM) × dL_orb/dt
```

where:
- `L_orb` = orbital angular momentum
- `L_rot` = rotational angular momentum  
- `a` = semi-major axis
- `Γ_tidal` = tidal torque
- `Γ_wave` = wave-mediated torque

## Limitations and Assumptions

1. **Circular orbit approximation** - Assumes small eccentricity
2. **Simplified tidal model** - Uses constant Love number and tidal lag
3. **No other planets** - Two-body problem only
4. **Uniform sphere** - Simplified moment of inertia
5. **Hypothetical coupling** - Wave torque is speculative, not based on observations

## Extending the Code

### Adding New Physical Effects

To add additional torques:

```python
def new_torque(self, state, t):
    """Calculate additional torque term."""
    return ...  # Your calculation

def derivatives(self, state, t):
    # Modify to include new_torque
    gamma_total = gamma_tidal + gamma_wave + self.new_torque(state, t)
```

### Custom Analysis

Extract specific quantities:

```python
t, sol = system.evolve((0, 10000))

L_orb = sol[:, 0]  # Orbital angular momentum
L_rot = sol[:, 1]  # Rotational angular momentum
a = sol[:, 2]      # Semi-major axis

# Calculate derived quantities
omega_earth = L_rot / system.const.I_EARTH
period_earth = 2 * np.pi / omega_earth  # Earth rotation period
recession_rate = np.gradient(a, t * 365.25 * 86400)  # cm/year
```

## Testing

Basic sanity checks:

```python
# Angular momentum should be roughly conserved
L_total = sol[:, 0] + sol[:, 1]
conservation_error = (L_total[-1] - L_total[0]) / L_total[0]
print(f"Angular momentum conservation error: {conservation_error:.2e}")

# Semi-major axis should increase (for Earth-Moon system)
assert sol[-1, 2] > sol[0, 2], "Moon should recede from Earth"
```

## Performance

Typical performance on modern hardware:
- 1,000 time points over 10,000 years: <1 second
- 10,000 time points over 100,000 years: ~5 seconds

For very long integrations or high precision, consider:
- Increasing `n_points` for smoother output
- Using more sophisticated ODE solvers from `scipy.integrate`
- Implementing adaptive time stepping

## References

Implementation based on:
- `papers/main_theory.tex` - Theoretical framework
- `equations/mathematical_formulation.tex` - Mathematical equations
- Standard celestial mechanics textbooks

## Troubleshooting

**Import errors:**
```bash
pip install --upgrade numpy scipy matplotlib
```

**Integration warnings:**
- Try increasing `n_points` for smoother evolution
- Check that time span isn't too long (keep under 1 million years)
- Verify initial conditions are physically reasonable

**Unexpected results:**
- Check parameter values (especially `alpha`, `omega_wave`)
- Verify units (all SI unless otherwise noted)
- Compare with classical case (alpha=0) first

## Contributing

See `../CONTRIBUTING.md` for guidelines on:
- Code style requirements
- Documentation standards
- Testing procedures
- Submitting improvements

---

For questions or issues, please open a GitHub issue.
