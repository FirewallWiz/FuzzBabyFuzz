import struct

class NVMeCommand:
    """
    Simplified NVMe-like command structure.
    Usually 64 bytes in real NVMe (Submission Queue Entry).
    We'll implement a smaller 16-byte version for demonstration.
    Layout:
    Byte 0: Opcode
    Byte 1: Flags
    Byte 2-3: Command ID
    Byte 4-7: Namespace Identifier (NSID)
    Byte 8-15: Data Pointer / LBA
    """
    def __init__(self, opcode=0, flags=0, cid=0, nsid=0, data_ptr=0):
        self.opcode = opcode
        self.flags = flags
        self.cid = cid
        self.nsid = nsid
        self.data_ptr = data_ptr

    def serialize(self):
        # < = little-endian, B = unsigned char (1), H = unsigned short (2), I = unsigned int (4), Q = unsigned long long (8)
        try:
            return struct.pack('<BBHIQ', self.opcode, self.flags, self.cid, self.nsid, self.data_ptr)
        except struct.error:
            # Fallback for mutated out-of-range values if we try to pack them directly
            # In a real fuzzer, we'd probably serialize first, then mutate the byte array.
            return b'\x00' * 16

    @classmethod
    def deserialize(cls, data):
        if len(data) < 16:
            raise ValueError("Data too short for command")
        opcode, flags, cid, nsid, data_ptr = struct.unpack('<BBHIQ', data[:16])
        return cls(opcode, flags, cid, nsid, data_ptr)
