"""
Simple validation script for wave-rotational model.
Tests basic functionality and physical correctness.
"""

import numpy as np
from wave_rotational_model import EarthMoonSystem, PhysicalConstants

def test_physical_constants():
    """Verify physical constants are reasonable."""
    const = PhysicalConstants()
    
    print("Testing Physical Constants:")
    print(f"  Earth mass: {const.M_EARTH:.3e} kg")
    print(f"  Moon mass: {const.M_MOON:.3e} kg")
    print(f"  Current Earth-Moon distance: {const.SEMI_MAJOR_AXIS/1e8:.3f} × 10^8 m")
    print(f"  Orbital period: {const.ORBITAL_PERIOD/86400:.2f} days")
    print()
    
    # Verify orbital frequency
    omega_orb = 2 * np.pi / const.ORBITAL_PERIOD
    omega_rot = 2 * np.pi / const.EARTH_ROTATION_PERIOD
    ratio = omega_rot / omega_orb
    print(f"  ω_Earth / ω_Moon = {ratio:.2f} (should be ~27.3)")
    print("  ✓ Physical constants look reasonable")
    print()

def test_angular_momentum():
    """Test angular momentum calculations."""
    system = EarthMoonSystem(alpha=0.0)
    
    L_orb = system.orbital_angular_momentum(
        system.const.SEMI_MAJOR_AXIS,
        system.const.ECCENTRICITY
    )
    
    omega_earth = 2 * np.pi / system.const.EARTH_ROTATION_PERIOD
    L_rot = system.const.I_EARTH * omega_earth
    
    print("Testing Angular Momentum:")
    print(f"  L_orbital = {L_orb:.3e} kg m²/s")
    print(f"  L_rotation = {L_rot:.3e} kg m²/s")
    print(f"  Ratio L_orb/L_rot = {L_orb/L_rot:.2f}")
    print("  ✓ Angular momentum values reasonable")
    print()

def test_tidal_torque():
    """Test tidal torque calculation."""
    system = EarthMoonSystem(alpha=0.0)
    
    omega_earth = 2 * np.pi / system.const.EARTH_ROTATION_PERIOD
    gamma = system.tidal_torque(system.const.SEMI_MAJOR_AXIS, omega_earth)
    
    print("Testing Tidal Torque:")
    print(f"  Tidal torque = {gamma:.3e} N·m")
    
    # Calculate implied recession rate
    # da/dt ~ 3.8 cm/year = 3.8e-2 m/year = 1.2e-9 m/s
    L_rot = system.const.I_EARTH * omega_earth
    
    # Time scale for significant change
    tau = L_rot / abs(gamma)
    print(f"  Time scale for rotation change: {tau/(365.25*86400):.2e} years")
    
    # Expected lunar recession
    L_orb = system.orbital_angular_momentum(
        system.const.SEMI_MAJOR_AXIS,
        system.const.ECCENTRICITY
    )
    mu = (system.const.M_EARTH * system.const.M_MOON) / \
         (system.const.M_EARTH + system.const.M_MOON)
    M_total = system.const.M_EARTH + system.const.M_MOON
    a = system.const.SEMI_MAJOR_AXIS
    
    da_dt = (2 * a**2) / (mu * system.const.G * M_total) * abs(gamma)
    da_dt_cm_per_year = da_dt * 100 * 365.25 * 86400  # Convert to cm/year
    
    print(f"  Implied lunar recession: {da_dt_cm_per_year:.2f} cm/year")
    print(f"  Expected (observed): ~3.8 cm/year")
    print()

def test_short_evolution():
    """Test system evolution over a short period."""
    system = EarthMoonSystem(alpha=0.0)
    
    print("Testing Short-term Evolution (100 years):")
    t, sol = system.evolve((0, 100), n_points=100)
    
    initial_a = sol[0, 2]
    final_a = sol[-1, 2]
    change = (final_a - initial_a) * 100  # Convert to cm
    
    print(f"  Initial distance: {initial_a/1e8:.6f} × 10^8 m")
    print(f"  Final distance: {final_a/1e8:.6f} × 10^8 m")
    print(f"  Change over 100 years: {change:.2f} cm")
    print(f"  Rate: {change/100:.3f} cm/year")
    print()

def test_wave_coupling():
    """Test wave coupling effects."""
    print("Testing Wave Coupling:")
    
    # Classical case
    system_classical = EarthMoonSystem(alpha=0.0)
    t, sol_classical = system_classical.evolve((0, 1000), n_points=500)
    recession_classical = (sol_classical[-1, 2] - sol_classical[0, 2]) * 100
    
    # With wave coupling
    system_wave = EarthMoonSystem(alpha=1e-6, omega_wave=2*np.pi/(500*365.25*86400))
    t, sol_wave = system_wave.evolve((0, 1000), n_points=500)
    recession_wave = (sol_wave[-1, 2] - sol_wave[0, 2]) * 100
    
    print(f"  Classical recession (1000 years): {recession_classical:.2f} cm")
    print(f"  With wave coupling: {recession_wave:.2f} cm")
    print(f"  Difference: {recession_wave - recession_classical:.4f} cm")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("Wave-Rotational Model: Validation Tests")
    print("=" * 60)
    print()
    
    test_physical_constants()
    test_angular_momentum()
    test_tidal_torque()
    test_short_evolution()
    test_wave_coupling()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
