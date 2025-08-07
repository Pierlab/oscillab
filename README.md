# Oscillab

Simple modular audio synthesizer with a minimal PyQt5 interface.

## Installation

```bash
pip install -r requirements.txt
```

## Running the tests

Execute the test suite to ensure that the audio components and the UI
bindings work as expected:

```bash
pytest
```

## Launching the synthesizer

Start the graphical interface with:

```bash
python main.py
```

The window lets you:

- Choose a waveform for each oscillator.
- Adjust each oscillator's frequency.
- Click **Play note** to generate sound using the current settings.

Experiment with the controls to modify the timbre and pitch of the generated
note. Additional signal processors such as a low‑pass filter, delay and
reverb are already wired in and can be extended with more widgets.

In headless environments you can run the interface without display support:

```bash
QT_QPA_PLATFORM=offscreen python main.py
```

