import numpy as np
from scipy import signal


class DelayEffect:
    """Simple delay effect using an IIR filter."""

    def __init__(self, time: float = 250.0, feedback: float = 0.3,
                 mix: float = 0.5, sample_rate: int = 44100) -> None:
        self.time = time  # milliseconds
        self.feedback = feedback
        self.mix = mix
        self.sample_rate = sample_rate

    def process(self, audio: np.ndarray) -> np.ndarray:
        """Apply the delay effect to an audio signal.

        A circular buffer is used to feed back the delayed signal
        according to the ``feedback`` and ``mix`` parameters.
        The output length matches the input length.
        """

        delay_samples = int(self.time / 1000.0 * self.sample_rate)
        if delay_samples <= 0:
            return audio

        buffer = np.zeros(delay_samples)
        output = np.zeros_like(audio)

        for i, sample in enumerate(audio):
            idx = i % delay_samples
            delayed_sample = buffer[idx]
            output[i] = (1 - self.mix) * sample + self.mix * delayed_sample
            buffer[idx] = sample + delayed_sample * self.feedback

        return output


class ReverbEffect:
    """Very basic reverb effect using convolution with an exponential impulse."""

    def __init__(self, room_size: float = 0.5, damping: float = 0.5,
                 mix: float = 0.3, sample_rate: int = 44100) -> None:
        self.room_size = room_size  # seconds
        self.damping = damping
        self.mix = mix
        self.sample_rate = sample_rate
        self._generate_impulse_response()

    def _generate_impulse_response(self) -> None:
        length = int(max(self.room_size, 0.01) * self.sample_rate)
        t = np.linspace(0, self.room_size, length, endpoint=False)
        impulse = np.random.randn(length) * np.exp(-self.damping * t)
        self.impulse = impulse

    def process(self, audio: np.ndarray) -> np.ndarray:
        wet = signal.fftconvolve(audio, self.impulse)[: len(audio)]
        return (1 - self.mix) * audio + self.mix * wet
