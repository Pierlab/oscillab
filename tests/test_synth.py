import os
import sys
import types
from pathlib import Path
import numpy as np
from unittest.mock import MagicMock
import pytest

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ensure PyQt5 runs in headless mode for tests
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# Provide a minimal mock for sounddevice to avoid PortAudio dependency during tests
sd_mock = types.SimpleNamespace(play=lambda *a, **k: None, wait=lambda: None)
sys.modules.setdefault("sounddevice", sd_mock)

from audio.oscillator import Oscillator
from audio.effects import DelayEffect, ReverbEffect

try:
    from interface.ui import SynthUI
    UI_AVAILABLE = True
except Exception:
    UI_AVAILABLE = False


def test_oscillator_frequency():
    osc = Oscillator(waveform="sine", frequency=440.0)
    samples = osc.generate(1.0)
    assert len(samples) == 44100
    freq = np.fft.rfftfreq(len(samples), 1 / osc.sample_rate)
    fft = np.abs(np.fft.rfft(samples))
    peak_freq = freq[np.argmax(fft)]
    assert abs(peak_freq - 440.0) < 1.0


def test_delay_and_reverb_effects():
    sample_rate = 44100
    impulse = np.zeros(sample_rate)
    impulse[0] = 1.0

    delay = DelayEffect(time=100.0, feedback=0.0, mix=1.0, sample_rate=sample_rate)
    delayed = delay.process(impulse)
    delay_samples = int(0.1 * sample_rate)
    assert np.isclose(delayed[0], 0.0)
    assert np.isclose(delayed[delay_samples], 1.0)

    reverb = ReverbEffect(room_size=0.2, damping=0.5, mix=1.0, sample_rate=sample_rate)
    reverbed = reverb.process(impulse)
    assert np.count_nonzero(reverbed[1:]) > 0


def test_ui_triggers_mixer_play():
    if not UI_AVAILABLE:
        pytest.skip("PyQt5 not available")
    ui = SynthUI()
    called = {"play": False}

    def fake_play(duration, note_off=None):
        called["play"] = True

    ui.mixer.play = MagicMock(side_effect=fake_play)
    ui.play_note()
    assert called["play"]
    assert ui.osc1.frequency == 440.0
    assert ui.osc2.frequency == 440.0
