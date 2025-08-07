import numpy as np
from scipy import signal

class Oscillator:
    """Basic oscillator capable of generating standard waveforms."""

    def __init__(self, waveform: str = "sine", frequency: float = 440.0,
                 detune: float = 0.0, volume: float = 1.0, sample_rate: int = 44100):
        self.waveform = waveform
        self.frequency = frequency
        self.detune = detune
        self.volume = volume
        self.sample_rate = sample_rate

    def _get_wave(self, t: np.ndarray) -> np.ndarray:
        freq = self.frequency + self.detune
        omega = 2 * np.pi * freq * t
        if self.waveform == "sine":
            return np.sin(omega)
        if self.waveform == "square":
            return signal.square(omega)
        if self.waveform == "sawtooth":
            return signal.sawtooth(omega)
        if self.waveform == "triangle":
            return signal.sawtooth(omega, 0.5)
        if self.waveform == "noise":
            return np.random.uniform(-1, 1, len(t))
        raise ValueError(f"Unknown waveform: {self.waveform}")

    def generate(self, duration: float) -> np.ndarray:
        """
        Generate the waveform for the given duration.

        Parameters
        ----------
        duration : float
            Duration in seconds.

        Returns
        -------
        np.ndarray
            Audio samples for the oscillator output.
        """
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, endpoint=False)
        wave = self._get_wave(t)
        return self.volume * wave
