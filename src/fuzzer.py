import time
import logging
import random
from protocol import NVMeCommand
from mutator import Mutator
from mock_target import MockNVMeController

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Fuzzer:
    """
    The main fuzzer engine that orchestrates corpus selection, mutation, and execution.
    """
    def __init__(self, target, iterations=1000):
        self.target = target
        self.iterations = iterations
        self.mutator = Mutator()
        self.crashes_found = 0
        
        # Base seed corpus of valid NVMe commands
        self.corpus = [
            NVMeCommand(opcode=0x01, nsid=1, data_ptr=0x1000).serialize(), # Valid Read
            NVMeCommand(opcode=0x02, nsid=1, data_ptr=0x2000).serialize(), # Valid Write
            NVMeCommand(opcode=0x03, nsid=0, data_ptr=0x0000).serialize(), # Valid Format
            NVMeCommand(opcode=0x04, nsid=0, data_ptr=0x0000).serialize()  # Valid Reset
        ]

    def run(self):
        logging.info(f"Starting fuzzing campaign with {self.iterations} iterations...")
        start_time = time.time()

        for i in range(self.iterations):
            # 1. Select a random seed from the corpus
            seed_data = random.choice(self.corpus)
            
            # 2. Mutate the seed
            mutated_data = self.mutator.mutate(seed_data)
            
            # 3. Send to target
            result = self.target.process_command(mutated_data)
            
            # 4. Triage results
            if result == "FATAL_CRASH":
                self.crashes_found += 1
                logging.error(f"Crash detected on iteration {i}!")
                logging.error(f"Payload (hex): {mutated_data.hex()}")
                
        end_time = time.time()
        logging.info("-" * 40)
        logging.info(f"Fuzzing completed in {end_time - start_time:.4f} seconds.")
        logging.info(f"Total crashes found: {self.crashes_found}")
        
        if self.crashes_found > 0:
            logging.info("Unique crash signatures identified:")
            for reason in set(self.target.crash_log):
                logging.info(f" -> {reason}")

if __name__ == "__main__":
    print("=======================================")
    print("       NVMe Lite Fuzzer v1.0           ")
    print("       Author: Pratik Roy (PoliTo)     ")
    print("=======================================\n")
    
    # Initialize the test harness target
    target = MockNVMeController()
    
    # Run a quick fuzzing campaign
    fuzzer = Fuzzer(target, iterations=5000)
    fuzzer.run()
