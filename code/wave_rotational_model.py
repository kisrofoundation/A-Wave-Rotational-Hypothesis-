"""
Wave-Rotational Hypothesis: Theoretical Calculations
=====================================================

This module provides numerical tools for exploring the wave-rotational
hypothesis in Earth-Moon dynamics. All calculations are theoretical and
based on the conceptual framework described in the accompanying papers.

Physical constants and orbital parameters are based on standard astronomical
values.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from typing import Tuple, Optional


# Physical constants (SI units unless noted)
class PhysicalConstants:
    """Standard physical and astronomical constants."""
    
    G = 6.67430e-11  # Gravitational constant [m^3 kg^-1 s^-2]
    M_EARTH = 5.972e24  # Earth mass [kg]
    M_MOON = 7.342e22  # Moon mass [kg]
    R_EARTH = 6.371e6  # Earth radius [m]
    R_MOON = 1.737e6  # Moon radius [m]
    
    # Current Earth-Moon system parameters
    SEMI_MAJOR_AXIS = 3.844e8  # Current Earth-Moon distance [m]
    ECCENTRICITY = 0.0549  # Orbital eccentricity
    ORBITAL_PERIOD = 27.322 * 86400  # Sidereal month [s]
    EARTH_ROTATION_PERIOD = 86400  # One day [s]
    
    # Tidal parameters
    K2_EARTH = 0.299  # Earth's Love number (dimensionless)
    TIDAL_LAG = 2.16e-2  # Tidal lag angle [radians]
    
    # Moment of inertia (simplified as uniform sphere)
    I_EARTH = 0.4 * M_EARTH * R_EARTH**2  # [kg m^2]


class EarthMoonSystem:
    """
    Model of Earth-Moon dynamics with optional wave-rotational coupling.
    
    This class implements both classical tidal evolution and the hypothetical
    wave-rotational coupling mechanism.
    """
    
    def __init__(self, 
                 alpha: float = 0.0,
                 omega_wave: float = 2*np.pi/(1000*365.25*86400),
                 phase_0: float = 0.0):
        """
        Initialize Earth-Moon system model.
        
        Parameters
        ----------
        alpha : float
            Dimensionless wave coupling strength (0 for classical case)
        omega_wave : float
            Wave angular frequency [rad/s] (default: 1000 year period)
        phase_0 : float
            Initial phase of wave coupling [rad]
        """
        self.alpha = alpha
        self.omega_wave = omega_wave
        self.phase_0 = phase_0
        self.const = PhysicalConstants()
        
    def orbital_angular_momentum(self, a: float, e: float) -> float:
        """
        Calculate orbital angular momentum.
        
        Parameters
        ----------
        a : float
            Semi-major axis [m]
        e : float
            Orbital eccentricity
            
        Returns
        -------
        float
            Orbital angular momentum [kg m^2 s^-1]
        """
        mu = (self.const.M_EARTH * self.const.M_MOON) / \
             (self.const.M_EARTH + self.const.M_MOON)
        M_total = self.const.M_EARTH + self.const.M_MOON
        
        return mu * np.sqrt(self.const.G * M_total * a * (1 - e**2))
    
    def tidal_torque(self, a: float, omega_rot: float = None) -> float:
        """
        Calculate classical tidal torque on Earth from the Moon.
        
        This uses an empirically calibrated formula to match the observed
        lunar recession rate of ~3.8 cm/year at the current Earth-Moon distance.
        
        When Earth rotates faster than Moon orbits (ω_rot > ω_orb), the tidal
        bulge leads the Earth-Moon line, transferring angular momentum from
        Earth's rotation to Moon's orbit.
        
        Parameters
        ----------
        a : float
            Semi-major axis [m]
        omega_rot : float, optional
            Earth's rotation rate [rad/s]. If None, uses current value.
            
        Returns
        -------
        float
            Tidal torque magnitude [N m]
            Positive means angular momentum transfer from Earth rotation to Moon orbit
        """
        if omega_rot is None:
            omega_rot = 2 * np.pi / self.const.EARTH_ROTATION_PERIOD
        
        omega_orb = np.sqrt(self.const.G * (self.const.M_EARTH + self.const.M_MOON) / a**3)
        
        # Use empirical calibration to match observed 3.8 cm/year
        # Required torque at current distance: ~1.2e11 N⋅m
        
        # Reference values at current configuration
        a_ref = self.const.SEMI_MAJOR_AXIS
        
        # Tidal torque scales as a^(-6) for constant Q
        # Calibrated to give 3.8 cm/year recession at current distance
        torque_ref = 1.192e11  # N⋅m, empirically calibrated
        
        torque = torque_ref * (a_ref / a)**6
        
        # Only applies when Earth rotates faster than Moon orbits
        if omega_rot <= omega_orb:
            torque = 0.0
        
        return torque
    
    def wave_torque(self, L_orb: float, L_rot: float, t: float) -> float:
        """
        Calculate hypothetical wave-mediated torque.
        
        Parameters
        ----------
        L_orb : float
            Orbital angular momentum [kg m^2 s^-1]
        L_rot : float
            Rotational angular momentum [kg m^2 s^-1]
        t : float
            Time [s]
            
        Returns
        -------
        float
            Wave-mediated torque [N m]
        """
        if self.alpha == 0:
            return 0.0
        
        phase = self.omega_wave * t + self.phase_0
        coupling_factor = (L_orb * L_rot) / ((L_orb + L_rot)**2)
        
        return self.alpha * coupling_factor * np.cos(phase)
    
    def derivatives(self, state: np.ndarray, t: float) -> np.ndarray:
        """
        Calculate time derivatives for ODE integration.
        
        Parameters
        ----------
        state : ndarray
            [L_orb, L_rot, a] - orbital momentum, rotational momentum, semi-major axis
        t : float
            Time [s]
            
        Returns
        -------
        ndarray
            Time derivatives [dL_orb/dt, dL_rot/dt, da/dt]
        """
        L_orb, L_rot, a = state
        
        # Current rotation rate
        omega_rot = L_rot / self.const.I_EARTH
        
        # Classical tidal torque
        # Positive torque means angular momentum transfer FROM Earth rotation TO Moon orbit
        gamma_tidal = self.tidal_torque(a, omega_rot)
        
        # Wave torque
        gamma_wave = self.wave_torque(L_orb, L_rot, t)
        
        # Angular momentum evolution
        # Sign convention: gamma_tidal > 0 means transfer FROM Earth rotation TO Moon orbit
        # Therefore: orbit gains (+gamma_tidal), rotation loses (-gamma_tidal)
        # Wave coupling modifies this: if gamma_wave > 0, it transfers FROM orbit TO rotation
        dL_orb_dt = gamma_tidal - gamma_wave  # Orbit gains from tidal, loses to wave
        dL_rot_dt = -gamma_tidal + gamma_wave  # Rotation loses to tidal, gains from wave
        
        # Semi-major axis evolution (assuming circular orbit, e≈0)
        mu = (self.const.M_EARTH * self.const.M_MOON) / \
             (self.const.M_EARTH + self.const.M_MOON)
        M_total = self.const.M_EARTH + self.const.M_MOON
        
        da_dt = (2 * a**2) / (mu * self.const.G * M_total) * dL_orb_dt
        
        return np.array([dL_orb_dt, dL_rot_dt, da_dt])
    
    def evolve(self, 
               t_span: Tuple[float, float],
               n_points: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evolve the Earth-Moon system over time.
        
        Parameters
        ----------
        t_span : tuple
            (t_start, t_end) in years
        n_points : int
            Number of time points
            
        Returns
        -------
        t : ndarray
            Time array [years]
        solution : ndarray
            Solution array with columns [L_orb, L_rot, a]
        """
        # Convert years to seconds
        t_start = t_span[0] * 365.25 * 86400
        t_end = t_span[1] * 365.25 * 86400
        t = np.linspace(t_start, t_end, n_points)
        
        # Initial conditions
        L_orb_0 = self.orbital_angular_momentum(
            self.const.SEMI_MAJOR_AXIS, 
            self.const.ECCENTRICITY
        )
        omega_earth = 2 * np.pi / self.const.EARTH_ROTATION_PERIOD
        L_rot_0 = self.const.I_EARTH * omega_earth
        a_0 = self.const.SEMI_MAJOR_AXIS
        
        initial_state = np.array([L_orb_0, L_rot_0, a_0])
        
        # Integrate ODEs
        solution = odeint(self.derivatives, initial_state, t)
        
        # Convert time back to years
        t_years = t / (365.25 * 86400)
        
        return t_years, solution


def plot_evolution(t: np.ndarray, 
                   solution: np.ndarray,
                   title: str = "Earth-Moon System Evolution"):
    """
    Plot the evolution of the Earth-Moon system.
    
    Parameters
    ----------
    t : ndarray
        Time array [years]
    solution : ndarray
        Solution array with columns [L_orb, L_rot, a]
    title : str
        Plot title
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))
    
    # Orbital angular momentum
    axes[0].plot(t, solution[:, 0] / 1e34)
    axes[0].set_ylabel(r'$L_{\mathrm{orb}}$ [$10^{34}$ kg m$^2$ s$^{-1}$]')
    axes[0].set_title(title)
    axes[0].grid(True, alpha=0.3)
    
    # Rotational angular momentum
    axes[1].plot(t, solution[:, 1] / 1e33)
    axes[1].set_ylabel(r'$L_{\mathrm{rot}}$ [$10^{33}$ kg m$^2$ s$^{-1}$]')
    axes[1].grid(True, alpha=0.3)
    
    # Semi-major axis
    axes[2].plot(t, solution[:, 2] / 1e8)
    axes[2].set_ylabel(r'Semi-major axis [$10^8$ m]')
    axes[2].set_xlabel('Time [years]')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def compare_models(alpha_values: list = [0.0, 1e-6, 1e-5],
                   t_span: Tuple[float, float] = (0, 10000)):
    """
    Compare evolution with different wave coupling strengths.
    
    Parameters
    ----------
    alpha_values : list
        List of alpha values to compare
    t_span : tuple
        Time span in years
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    for alpha in alpha_values:
        system = EarthMoonSystem(alpha=alpha)
        t, solution = system.evolve(t_span)
        
        label = f'α = {alpha:.0e}' if alpha > 0 else 'Classical (α = 0)'
        
        axes[0].plot(t, solution[:, 0] / 1e34, label=label)
        axes[1].plot(t, solution[:, 1] / 1e33, label=label)
        axes[2].plot(t, (solution[:, 2] - solution[0, 2]) * 100, label=label)
    
    axes[0].set_ylabel(r'$L_{\mathrm{orb}}$ [$10^{34}$ kg m$^2$ s$^{-1}$]')
    axes[0].set_title('Comparison of Classical and Wave-Rotational Models')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    axes[1].set_ylabel(r'$L_{\mathrm{rot}}$ [$10^{33}$ kg m$^2$ s$^{-1}$]')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    axes[2].set_ylabel('Distance change [cm]')
    axes[2].set_xlabel('Time [years]')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    """
    Example usage: Compare classical tidal evolution with wave-rotational coupling.
    """
    print("Wave-Rotational Hypothesis: Numerical Calculations")
    print("=" * 50)
    print()
    
    # Classical case
    print("Classical tidal evolution (no wave coupling):")
    system_classical = EarthMoonSystem(alpha=0.0)
    t, sol = system_classical.evolve((0, 10000), n_points=1000)
    
    distance_change = (sol[-1, 2] - sol[0, 2]) * 100  # Convert to cm
    print(f"  Lunar recession over 10,000 years: {distance_change:.2f} cm")
    print(f"  Average rate: {distance_change/10000:.4f} cm/year")
    print()
    
    # Wave-rotational case
    print("With wave-rotational coupling (α = 1e-5):")
    system_wave = EarthMoonSystem(alpha=1e-5, 
                                   omega_wave=2*np.pi/(1000*365.25*86400))
    t, sol = system_wave.evolve((0, 10000), n_points=1000)
    
    distance_change = (sol[-1, 2] - sol[0, 2]) * 100
    print(f"  Lunar recession over 10,000 years: {distance_change:.2f} cm")
    print(f"  Average rate: {distance_change/10000:.4f} cm/year")
    print()
    
    # Generate comparison plots
    print("Generating comparison plots...")
    fig = compare_models(alpha_values=[0.0, 1e-6, 1e-5], t_span=(0, 10000))
    
    print("Analysis complete.")
    print()
    print("Note: These calculations are theoretical and illustrative.")
    print("Actual parameter values require empirical determination.")
