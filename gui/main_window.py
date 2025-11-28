from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from midi.midi_manager import MidiManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drum MIDI App (Skeleton)")
        self.resize(1200, 800)

        # Backend objects
        self.midi_manager = MidiManager()

        # UI setup
        self._create_central_widget()
        self._connect_signals()

        # MIDI check / logging
        self._log_available_midi_ports()

    def _create_central_widget(self):
        central = QWidget(self)
        main_layout = QVBoxLayout(central)

        # Transport + MIDI strip (top bar)
        transport_widget = QWidget(central)
        transport_layout = QHBoxLayout(transport_widget)
        transport_layout.setContentsMargins(0, 0, 0, 0)
        transport_layout.setSpacing(8)

        # Transport buttons
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.record_button = QPushButton("Record")
        self.record_button.setCheckable(True)  # toggle on/off

        # MIDI input selector
        self.input_combo = QComboBox()

        # MIDI output selector
        self.output_combo = QComboBox()

        # Set Size Policy
        policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.input_combo.setSizePolicy(policy)
        self.output_combo.setSizePolicy(policy)

        self.input_combo.setFixedWidth(200)
        self.output_combo.setFixedWidth(200)

        # Test note button (for output)
        self.test_note_button = QPushButton("Test Note")

        # Refresh MIDI button
        self.refresh_midi_button = QPushButton("Refresh MIDI")

        # Left side: transport buttons
        transport_layout.addWidget(self.play_button)
        transport_layout.addWidget(self.stop_button)
        transport_layout.addWidget(self.record_button)

        # Spacer between transport and MIDI controls
        transport_layout.addStretch()

        # Right side: MIDI controls
        transport_layout.addWidget(QLabel("Out:"))
        transport_layout.addWidget(self.output_combo)

        transport_layout.addWidget(QLabel("In:"))
        transport_layout.addWidget(self.input_combo)

        transport_layout.addWidget(self.test_note_button)
        transport_layout.addWidget(self.refresh_midi_button)

        # --- Placeholder main area ---
        self.placeholder_label = QLabel(
            "Drum MIDI App\n(Timeline / Drum Grid will go here)"
        )
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("font-size: 18px; color: #555;")

        # Add to main layout
        main_layout.addWidget(transport_widget)
        main_layout.addWidget(self.placeholder_label, 1)

        self.setCentralWidget(central)

        # Fill MIDI combos
        self._refresh_midi_outputs()
        self._refresh_midi_inputs()

    def _connect_signals(self):
        # Transport
        self.play_button.clicked.connect(self._on_play_clicked)
        self.stop_button.clicked.connect(self._on_stop_clicked)
        self.record_button.toggled.connect(self._on_record_toggled)

        # MIDI I/O
        self.output_combo.currentTextChanged.connect(self._on_output_changed)
        self.input_combo.currentTextChanged.connect(self._on_input_changed)
        self.test_note_button.clicked.connect(self._on_test_note_clicked)
        self.refresh_midi_button.clicked.connect(self._on_refresh_midi_clicked)

    # MIDI combo population

    def _refresh_midi_outputs(self):
        """Fill the output combo box with available MIDI output ports."""
        ports = self.midi_manager.list_output_ports()

        self.output_combo.blockSignals(True)
        self.output_combo.clear()

        if not ports:
            # No outputs at all
            self.output_combo.addItem("No MIDI outputs")
            self.output_combo.setEnabled(False)
            self.test_note_button.setEnabled(False)
        else:
            # Placeholder + real ports
            self.output_combo.addItem("Select MIDI Output")
            # visually "placeholder-ish" (optional; doesn't affect logic)
            self.output_combo.setItemData(0, 0, Qt.UserRole - 1)

            self.output_combo.addItems(ports)
            self.output_combo.setEnabled(True)
            self.test_note_button.setEnabled(True)

            # Always start on placeholder, not first real port
            self.output_combo.setCurrentIndex(0)

        self.output_combo.blockSignals(False)

    def _refresh_midi_inputs(self):
        """Fill the input combo box with available MIDI input ports."""
        ports = self.midi_manager.list_input_ports()

        self.input_combo.blockSignals(True)
        self.input_combo.clear()

        if not ports:
            # No inputs at all
            self.input_combo.addItem("No MIDI inputs")
            self.input_combo.setEnabled(False)
        else:
            # Placeholder + real ports
            self.input_combo.addItem("Select MIDI Input")
            self.input_combo.setItemData(0, 0, Qt.UserRole - 1)

            self.input_combo.addItems(ports)
            self.input_combo.setEnabled(True)

            # Always start on placeholder, not first real port
            self.input_combo.setCurrentIndex(0)

        self.input_combo.blockSignals(False)

    def _log_available_midi_ports(self):
        out_ports = self.midi_manager.list_output_ports()
        in_ports = self.midi_manager.list_input_ports()

        print("MIDI outputs:")
        if not out_ports:
            print("  (none)")
        else:
            for name in out_ports:
                print(f"  - {name}")

        print("MIDI inputs:")
        if not in_ports:
            print("  (none)")
        else:
            for name in in_ports:
                print(f"  - {name}")

        if not out_ports and not in_ports:
            self.placeholder_label.setText(
                "No MIDI inputs or outputs found.\n"
                "(Is a virtual or hardware MIDI device available?)"
            )
        else:
            print(
                "MIDI ports detected.\n"
                "Select In/Out at the top and use 'Test Note'."
            )

    # Handlers / slots

    def _on_play_clicked(self):
        print("Play clicked")
        self.placeholder_label.setText("Play clicked\n(Placeholder: no audio yet)")

    def _on_stop_clicked(self):
        print("Stop clicked")
        self.placeholder_label.setText("Stop clicked\n(Placeholder: transport stopped)")

    def _on_record_toggled(self, checked: bool):
        if checked:
            print("Record started")
            self.record_button.setText("Recording...")
            self.placeholder_label.setText("Recording...\n(Placeholder: no MIDI yet)")
        else:
            print("Record stopped")
            self.record_button.setText("Record")
            self.placeholder_label.setText(
                "Recording stopped\n(Timeline / Drum Grid will go here)"
            )

    def _on_output_changed(self, name: str):
        # Ignore placeholder / no-devices entries
        if not name or name in ("Select MIDI Output", "No MIDI outputs"):
            return

        ok = self.midi_manager.select_output(name)
        if ok:
            self.placeholder_label.setText(f"Selected MIDI output:\n{name}")
        else:
            self.placeholder_label.setText(f"Failed to open MIDI output:\n{name}")

    def _on_input_changed(self, name: str):
        # Ignore placeholder / no-devices entries
        if not name or name in ("Select MIDI Input", "No MIDI inputs"):
            return

        ok = self.midi_manager.select_input(name)
        if ok:
            self.placeholder_label.setText(
                f"Selected MIDI input:\n{name}\n"
                "Incoming MIDI will be printed to the console."
            )
        else:
            self.placeholder_label.setText(f"Failed to open MIDI input:\n{name}")

    def _on_test_note_clicked(self):
        if self.midi_manager.current_output is None:
            self.placeholder_label.setText(
                "No MIDI output selected.\n"
                "Choose a device from the 'Out' dropdown first."
            )
            print("Test Note clicked, but no MIDI output selected.")
            return

        self.midi_manager.send_test_note()
        self.placeholder_label.setText(
            "Sent test drum note.\n"
            "If nothing is heard, check your MIDI routing."
        )

    def _on_refresh_midi_clicked(self):
        print("Refreshing MIDI inputs/outputs...")
        self._refresh_midi_outputs()
        self._refresh_midi_inputs()
        self._log_available_midi_ports()
        self.placeholder_label.setText(
            "Refreshed MIDI ports.\n"
        )
