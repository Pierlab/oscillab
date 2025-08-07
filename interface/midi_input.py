import mido
from threading import Thread
from typing import Callable


class MIDIInput:
    """Simple wrapper around mido to listen for MIDI note events."""

    def __init__(self, port_name: str | None = None) -> None:
        self.port_name = port_name
        self.thread: Thread | None = None
        self.running = False

    def _run(self, callback: Callable[[mido.Message], None]) -> None:
        with mido.open_input(self.port_name) as port:
            for msg in port:
                if not self.running:
                    break
                if msg.type in {"note_on", "note_off"}:
                    callback(msg)

    def listen(self, callback: Callable[[mido.Message], None]) -> None:
        if self.running:
            return
        self.running = True
        self.thread = Thread(target=self._run, args=(callback,), daemon=True)
        self.thread.start()

    def stop(self) -> None:
        self.running = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None
