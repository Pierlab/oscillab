import numpy as np


class ADSREnvelope:
    """ADSR (Attack, Decay, Sustain, Release) envelope generator.

    Parameters
    ----------
    attack : float
        Attack time in seconds.
    decay : float
        Decay time in seconds.
    sustain : float
        Sustain level between 0 and 1.
    release : float
        Release time in seconds.
    sample_rate : int, optional
        Audio sample rate, by default 44100.
    """

    def __init__(self, attack: float = 0.01, decay: float = 0.1,
                 sustain: float = 0.7, release: float = 0.2,
                 sample_rate: int = 44100) -> None:
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.sample_rate = sample_rate

    def generate(self, duration: float, note_off: float | None = None) -> np.ndarray:
        """Generate the ADSR envelope for a given duration.

        Parameters
        ----------
        duration : float
            Total duration in seconds, including the release phase.
        note_off : float | None, optional
            Time in seconds when the note is released (start of the
            release phase). If ``None``, the note is held for the whole
            duration minus the release time.

        Returns
        -------
        np.ndarray
            The ADSR envelope as a NumPy array.
        """
        sr = self.sample_rate
        total_samples = int(sr * duration)
        attack_samples = int(sr * self.attack)
        decay_samples = int(sr * self.decay)
        release_samples = int(sr * self.release)

        if note_off is None:
            note_off_samples = max(total_samples - release_samples, 0)
        else:
            note_off_samples = int(sr * note_off)

        sustain_samples = max(note_off_samples - attack_samples - decay_samples, 0)
        sustain_level = self.sustain

        env = np.zeros(total_samples)
        idx = 0

        # Attack
        if attack_samples > 0:
            env[idx:idx + attack_samples] = np.linspace(0, 1, attack_samples, endpoint=False)
            idx += attack_samples
        # Decay
        if decay_samples > 0:
            env[idx:idx + decay_samples] = np.linspace(1, sustain_level, decay_samples, endpoint=False)
            idx += decay_samples
        # Sustain
        if sustain_samples > 0:
            env[idx:idx + sustain_samples] = sustain_level
            idx += sustain_samples

        # Release
        remaining = total_samples - idx
        if remaining > 0:
            env[idx:] = np.linspace(env[idx-1] if idx > 0 else sustain_level, 0, remaining)

        return env

    def apply(self, audio: np.ndarray, note_off: float | None = None) -> np.ndarray:
        """Apply the envelope to an audio signal.

        Parameters
        ----------
        audio : np.ndarray
            Input audio signal.
        note_off : float | None, optional
            Time in seconds when the note is released.

        Returns
        -------
        np.ndarray
            The enveloped audio signal.
        """
        duration = len(audio) / self.sample_rate
        env = self.generate(duration, note_off)
        return audio * env[:len(audio)]
