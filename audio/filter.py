import numpy as np
from scipy import signal


class LowPassFilter:
    """Simple digital low-pass filter with resonance control."""

    def __init__(self, cutoff_frequency: float = 1000.0, resonance: float = 0.707,
                 sample_rate: int = 44100) -> None:
        self.cutoff_frequency = cutoff_frequency
        self.resonance = resonance
        self.sample_rate = sample_rate
        self._update_coefficients()

    def _update_coefficients(self) -> None:
        """Compute biquad coefficients for the current parameters."""
        w0 = 2 * np.pi * self.cutoff_frequency / self.sample_rate
        cos_w0 = np.cos(w0)
        sin_w0 = np.sin(w0)
        alpha = sin_w0 / (2 * max(self.resonance, 1e-5))

        b0 = (1 - cos_w0) / 2
        b1 = 1 - cos_w0
        b2 = (1 - cos_w0) / 2
        a0 = 1 + alpha
        a1 = -2 * cos_w0
        a2 = 1 - alpha

        # Normalize coefficients
        self.b = np.array([b0, b1, b2]) / a0
        self.a = np.array([1, a1 / a0, a2 / a0])

    def process(self, audio: np.ndarray) -> np.ndarray:
        """Apply the low-pass filter to an audio signal."""
        return signal.lfilter(self.b, self.a, audio)
