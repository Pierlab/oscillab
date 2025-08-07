import numpy as np
import sounddevice as sd

from .oscillator import Oscillator
from .envelope import ADSREnvelope
from .filter import LowPassFilter
from .effects import DelayEffect, ReverbEffect


class Mixer:
    """Combine oscillators, envelope, filter and effects into a final signal."""

    def __init__(self, osc1: Oscillator, osc2: Oscillator,
                 envelope: ADSREnvelope,
                 lp_filter: LowPassFilter | None = None,
                 delay: DelayEffect | None = None,
                 reverb: ReverbEffect | None = None,
                 sample_rate: int = 44100) -> None:
        self.osc1 = osc1
        self.osc2 = osc2
        self.envelope = envelope
        self.filter = lp_filter
        self.delay = delay
        self.reverb = reverb
        self.sample_rate = sample_rate

    def generate(self, duration: float, note_off: float | None = None) -> np.ndarray:
        wave1 = self.osc1.generate(duration)
        wave2 = self.osc2.generate(duration)
        mix = wave1 + wave2
        mix = self.envelope.apply(mix, note_off)
        if self.filter is not None:
            mix = self.filter.process(mix)
        if self.delay is not None:
            mix = self.delay.process(mix)
        if self.reverb is not None:
            mix = self.reverb.process(mix)
        return mix

    def play(self, duration: float, note_off: float | None = None) -> None:
        audio = self.generate(duration, note_off)
        sd.play(audio, self.sample_rate)
        sd.wait()
