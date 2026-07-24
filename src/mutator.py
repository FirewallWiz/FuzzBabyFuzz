import random

class Mutator:
    """
    Applies various mutation strategies to a byte array.
    This simulates standard fuzzing generation techniques.
    """
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    def mutate(self, data: bytes) -> bytes:
        data_list = bytearray(data)
        if not data_list:
            return data
        
        strategies = [
            self._bit_flip,
            self._byte_flip,
            self._magic_number,
            self._random_byte
        ]
        
        # Apply 1 to 3 random mutations to simulate fuzzing variations
        num_mutations = random.randint(1, 3)
        for _ in range(num_mutations):
            strategy = random.choice(strategies)
            strategy(data_list)
            
        return bytes(data_list)

    def _bit_flip(self, data: bytearray):
        """Flips a single random bit."""
        idx = random.randint(0, len(data) - 1)
        bit = random.randint(0, 7)
        data[idx] ^= (1 << bit)

    def _byte_flip(self, data: bytearray):
        """Flips an entire random byte."""
        idx = random.randint(0, len(data) - 1)
        data[idx] ^= 0xFF

    def _magic_number(self, data: bytearray):
        """Inserts known problematic integers (boundary values)."""
        magic_numbers = [0x00, 0xFF, 0x7F, 0x80, 0xFFFF, 0x0000, 0xFFFFFFFF, 0x7FFFFFFF]
        idx = random.randint(0, len(data) - 1)
        val = random.choice(magic_numbers)
        
        # Try to insert it if it fits
        if val <= 0xFF:
            data[idx] = val
        elif val <= 0xFFFF and idx < len(data) - 1:
            data[idx] = val & 0xFF
            data[idx+1] = (val >> 8) & 0xFF

    def _random_byte(self, data: bytearray):
        """Replaces a byte with a completely random value."""
        idx = random.randint(0, len(data) - 1)
        data[idx] = random.randint(0, 255)
