import struct

class MockNVMeController:
    """
    A simulated storage controller to test our fuzzer against.
    It contains intentional "bugs" designed to be discovered by fuzzing.
    """
    def __init__(self):
        self.state = "READY"
        self.crash_log = []

    def process_command(self, raw_data: bytes) -> str:
        if len(raw_data) != 16:
            return "ERROR: Invalid command size"

        try:
            opcode, flags, cid, nsid, data_ptr = struct.unpack('<BBHIQ', raw_data)
        except struct.error:
            return "ERROR: Malformed data"

        # --- INTENTIONAL VULNERABILITIES ---

        # Vulnerability 1: Null pointer dereference simulation on READ command
        if opcode == 0x01 and data_ptr == 0x00:
            self._crash("Null pointer dereference in READ command handling")
            return "FATAL_CRASH"

        # Vulnerability 2: Integer/Buffer overflow simulation when NSID is extremely large on WRITE
        if opcode == 0x02 and nsid > 0xFFFF0000:
            self._crash("Buffer overflow in WRITE command namespace allocation")
            return "FATAL_CRASH"

        # Vulnerability 3: State machine violation
        if opcode == 0x03:
            if self.state != "READY":
                self._crash(f"State machine violation: FORMAT command received while in state {self.state}")
                return "FATAL_CRASH"
            self.state = "FORMATTING"
        
        # Simulate completing format and returning to ready
        if opcode == 0x04:
            self.state = "READY"

        return "SUCCESS"

    def _crash(self, reason):
        # In a real environment, this would be a firmware panic, kernel panic, or assertion failure.
        self.crash_log.append(reason)
        # Reset state after a simulated crash so the fuzzer can keep running
        self.state = "READY"
