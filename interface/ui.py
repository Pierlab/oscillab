import sys
from PyQt5 import QtWidgets

from audio import (
    Oscillator,
    ADSREnvelope,
    LowPassFilter,
    DelayEffect,
    ReverbEffect,
    Mixer,
)


class SynthUI(QtWidgets.QMainWindow):
    """Basic graphical interface to interact with the synthesizer."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Python Synth")
        self.sample_rate = 44100

        # Audio components
        self.osc1 = Oscillator()
        self.osc2 = Oscillator()
        self.envelope = ADSREnvelope()
        self.filter = LowPassFilter()
        self.delay = DelayEffect()
        self.reverb = ReverbEffect()
        self.mixer = Mixer(
            self.osc1, self.osc2, self.envelope,
            self.filter, self.delay, self.reverb,
            self.sample_rate,
        )

        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)
        self.setCentralWidget(central)

        waveforms = ["sine", "square", "sawtooth", "triangle", "noise"]
        self.combo1 = QtWidgets.QComboBox()
        self.combo1.addItems(waveforms)
        self.combo1.currentTextChanged.connect(lambda w: setattr(self.osc1, "waveform", w))
        layout.addWidget(QtWidgets.QLabel("Oscillator 1 waveform"))
        layout.addWidget(self.combo1)

        self.combo2 = QtWidgets.QComboBox()
        self.combo2.addItems(waveforms)
        self.combo2.currentTextChanged.connect(lambda w: setattr(self.osc2, "waveform", w))
        layout.addWidget(QtWidgets.QLabel("Oscillator 2 waveform"))
        layout.addWidget(self.combo2)

        play_btn = QtWidgets.QPushButton("Play A4")
        play_btn.clicked.connect(self.play_note)
        layout.addWidget(play_btn)

    def play_note(self) -> None:
        self.osc1.frequency = 440.0
        self.osc2.frequency = 440.0
        self.mixer.play(1.0)


def run() -> None:
    app = QtWidgets.QApplication(sys.argv)
    ui = SynthUI()
    ui.show()
    app.exec_()


if __name__ == "__main__":
    run()
