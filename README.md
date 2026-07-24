## About ME & Project Context

As an Cybersec engineering student at **Politecnico di Torino**, I have focused on building a versatile skill set that spans low-level embedded systems, security tooling, and software engineering. 

I created this mid-level fuzzer to bridge the gap between my academic foundation and practical implementations. It practically demonstrates my understanding of operating system fundamentals (concurrency, memory management), security testing methodologies (defect discovery, crash triage), and protocol boundary analysis.

## Project Overview

This project is a conceptual fuzzing framework built to demonstrate core principles of protocol fuzzing, specifically tailored for standard storage protocols. It showcases a hands-on understanding of protocol parsing, mutation-based fuzzing, and test harness integration.

## Architecture & Design

The framework is divided into several modular components that mirror real-world fuzzer design:

1. **Protocol Definition (`src/protocol.py`)**: 
   Implements a simplified 16-byte NVMe-like command structure. It handles serialization (encoding to raw bytes) and deserialization. This represents how a host driver structures a Submission Queue Entry (SQE).
   
2. **Mutator Engine (`src/mutator.py`)**: 
   A custom byte-level mutation engine applying various fuzzing strategies:
   * Bit flipping
   * Byte flipping
   * Magic number insertion (boundary values)
   * Random byte replacement
   
3. **Mock Target Harness (`src/mock_target.py`)**: 
   A simulated storage controller designed to act as the Device Under Test (DUT). It parses incoming binary data and contains intentional vulnerabilities (simulated null pointer dereferences, buffer overflows, and state machine violations) that the fuzzer is meant to discover.

4. **Fuzzer Core (`src/fuzzer.py`)**: 
   The orchestrator. It maintains a seed corpus of valid commands, iteratively applies mutations, transmits them to the mock target, and performs basic crash logging/triage.

## How to Run

1. Ensure you have **Python 3.x** installed.
2. Clone or download this repository.
3. Open a terminal and navigate to the project root directory.
4. Execute the fuzzer script:

```bash
python src/fuzzer.py
```

## Example Execution Output

As the fuzzer runs its campaign, it will uncover the intentionally planted bugs in the mock target. You will see output similar to this:

```text
=======================================
       NVMe Lite Fuzzer v1.0           
       Author: Pratik Roy (PoliTo)     
=======================================

2026-07-24 20:30:00,000 - INFO - Starting fuzzing campaign with 5000 iterations...
2026-07-24 20:30:00,010 - ERROR - Crash detected on iteration 42!
...
2026-07-24 20:30:00,150 - INFO - Total crashes found: 28
2026-07-24 20:30:00,150 - INFO - Unique crash signatures identified:
2026-07-24 20:30:00,150 - INFO -  -> Buffer overflow in WRITE command namespace allocation
2026-07-24 20:30:00,150 - INFO -  -> Null pointer dereference in READ command handling
2026-07-24 20:30:00,150 - INFO -  -> State machine violation: FORMAT command received while in state FORMATTING
```


* **Coverage-Guided Fuzzing**: Integrate with tools like `AFL++` or `libFuzzer` using Python bindings to generate coverage signals, moving from black-box random mutation to grey-box intelligent fuzzing.
* **Full Protocol Specifications**: Expand `protocol.py` to support the complete 64-byte SQE and 16-byte CQE NVMe specification, including PRP/SGL list handling and vendor-specific opcodes.
* **Hardware/Emulator Integration**: Replace `mock_target.py` with a robust test harness (e.g., using `SPDK` or `vfio-pci`) to inject raw PCIe packets directly into physical NVMe drives, UFS endpoints, or QEMU emulators.
* **Automated Crash Minimization**: Implement a mechanism that takes a crashing input and systematically trims bytes to find the minimal reproducible test case, aiding root cause analysis.
