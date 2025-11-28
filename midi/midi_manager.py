import mido
import time

class MidiManager:
    """
    Small MIDI helper:
    - lists available MIDI input/output ports
    - opens selected ports
    - can send a simple test drum note to the output
    """

    def __init__(self):
        # Output
        self.current_output_name = None
        self.current_output = None

        # Input
        self.current_input_name = None
        self.current_input = None

        # Input callback
        self.input_callback = None

    # Output

    def list_output_ports(self):
        """Return a list of available MIDI output port names."""
        try:
            ports = mido.get_output_names()
        except Exception as e:
            print(f"Error listing MIDI output ports: {e}")
            ports = []
        return ports

    def select_output(self, name: str) -> bool:
        """Open the given MIDI output port by name."""
        # Close any existing port
        if self.current_output is not None:
            try:
                self.current_output.close()
            except Exception:
                pass
            self.current_output = None
            self.current_output_name = None

        if not name:
            return False

        try:
            self.current_output = mido.open_output(name)
            self.current_output_name = name
            print(f"Opened MIDI output: {name}")
            return True
        except Exception as e:
            print(f"Error opening MIDI output {name}: {e}")
            self.current_output = None
            self.current_output_name = None
            return False

    def send_test_note(self):
        """Send a single test drum hit (kick) to the current output."""
        if self.current_output is None:
            print("No MIDI output selected / open.")
            return

        # General MIDI: channel 0 test note
        msg_on = mido.Message("note_on", channel=0, note=60, velocity=100)

        self.current_output.send(msg_on)
        print("Sent test drum note (note 60).")

    def send_message(self, msg: mido.Message):
        if self.current_output is None:
            print("No MIDI output selected / open")
            return
        
        self.current_output.send(msg)

    # Input

    def list_input_ports(self):
        """Return a list of available MIDI input port names."""
        try:
            ports = mido.get_input_names()
        except Exception as e:
            print(f"Error listing MIDI input ports: {e}")
            ports = []
        return ports

    def select_input(self, name: str, callback=None) -> bool:
        """Open the given MIDI input port by name, printing incoming messages."""
        # Close any existing port
        if self.current_input is not None:
            try:
                self.current_input.close()
            except Exception:
                pass
            self.current_input = None
            self.current_input_name = None
            self.input_callback = None

        if not name:
            return False
        
        self.input_callback = callback

        try:
            # Use a callback that only prints
            self.current_input = mido.open_input(name, callback=self._handle_input_message)
            self.current_input_name = name
            print(f"Opened MIDI input: {name}")
            return True
        except Exception as e:
            print(f"Error opening MIDI input {name}: {e}")
            self.current_input = None
            self.current_input_name = None
            self.input_callback = None
            return False

    def _handle_input_message(self, message: mido.Message):
        """This is called from a background thread by mido."""
        ts = time.monotonic();
        # print(f"MIDI IN [{self.current_input_name}] @ {ts:.3f}: {message}")

        if self.input_callback is not None:
            try:
                self.input_callback(message, ts)
            except Exception as e:
                print(f"Error in input_callback: {e}")

    # Cleanup

    def close_all(self):
        """Close any open input/output ports."""
        if self.current_output is not None:
            try:
                self.current_output.close()
            except Exception:
                pass
            self.current_output = None
            self.current_output_name = None

        if self.current_input is not None:
            try:
                self.current_input.close()
            except Exception:
                pass
            self.current_input = None
            self.current_input_name = None
