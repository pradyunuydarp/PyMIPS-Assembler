# PyMIPS-Assembler

# **MIPS Instruction Execution Simulator**

This repository provides simulators for executing **MIPS Instructions** in both **Non-Pipelined** and **Pipelined Processors**. These simulators are ideal for learning processor execution concepts, such as instruction cycles, pipeline stages, and hazard management.

---

## **Table of Contents**
- [**Overview**](#overview)
- [**Features**](#features)
- [**Installation**](#installation)
- [**Usage**](#usage)
  - [Non-Pipelined Processor](#non-pipelined-processor)
  - [Pipelined Processor](#pipelined-processor)
- [**Supported Instructions**](#supported-instructions)
- [**Input Format**](#input-format)
- [**Output Format**](#output-format)
- [**Files**](#files)
- [**Future Improvements**](#future-improvements)
- [**Contributing**](#contributing)
- [**License**](#license)

---

## **Overview**

The **MIPS Instruction Execution Simulator** provides:
- Emulation of MIPS assembly instructions using:
  - **Non-Pipelined Processor**: Sequential instruction processing.
  - **Pipelined Processor**: Parallel instruction processing across multiple stages.
- Support for detecting and handling **data hazards**, **control hazards**, and **stalls**.

---

## **Features**
- **Non-Pipelined Processor**:
  - Step-by-step execution of MIPS instructions.
- **Pipelined Processor**:
  - Parallel execution across `FETCH`, `DECODE`, `EXECUTE`, `MEMORY ACCESS`, and `WRITEBACK` stages.
  - Handles stalls and flushes for hazards.
- **Customizable Mappings**:
  - Define new instructions and register mappings using `opcodemapper.txt` and `regcodemapper.txt`.

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/pradyunuydarp/MIPS-Simulator.git
   cd MIPS-Simulator
   ```
2. Ensure you have **Python 3.x** installed.

3. Prepare input files:
   - `Output.txt`: Contains instructions for sorting numbers.
   - `fibonacci.txt`: Contains instructions for Fibonacci sequence generation.

---

## **Usage**

### **Non-Pipelined Processor**
1. Prepare input files (e.g., `Output.txt` or `fibonacci.txt`).
2. Execute the non-pipelined simulator:
   ```bash
   python non_pipelined_processor.py
   ```
3. Follow the instructions to select the desired operation.

### **Pipelined Processor**
1. Prepare input files (e.g., `Output.txt` or `fibonacci.txt`).
2. Execute the pipelined simulator:
   ```bash
   python pipelined_processor.py
   ```
3. Observe pipeline stages, hazards, and stalls during execution.

---

## **Supported Instructions**

### **R-Type Instructions**
| Instruction | Description      |
|-------------|------------------|
| `add`       | Addition         |
| `sub`       | Subtraction      |
| `slt`       | Set less than    |
| `sll`       | Shift left       |

### **I-Type Instructions**
| Instruction | Description              |
|-------------|--------------------------|
| `lw`        | Load word               |
| `sw`        | Store word              |
| `addi`      | Add immediate           |
| `beq`       | Branch if equal         |
| `bne`       | Branch if not equal     |

### **J-Type Instructions**
| Instruction | Description              |
|-------------|--------------------------|
| `j`         | Jump                    |
| `jal`       | Jump and link           |

### **M-Type Instructions**
| Instruction | Description              |
|-------------|--------------------------|
| `mul`       | Multiply                |

---

## **Input Format**

### **Instruction Format**
Input files contain MIPS assembly instructions in **binary format**. Each instruction follows the standard MIPS encoding scheme.

#### Example (`Output.txt`):
```
00000000001000100001100000100000  # add $3, $1, $2
00010000001000100000000000001010  # beq $1, $2, 10
10001100001000100000000000000100  # lw $2, 4($1)
```

---

## **Output Format**

### **Non-Pipelined Processor**
- Logs the sequential execution of instructions at each stage.

### **Pipelined Processor**
- Logs parallel execution in pipeline stages.
- Highlights hazards (data or control) and stalls/flushes.

---

## **Files**

| File                    | Description                                                |
|-------------------------|------------------------------------------------------------|
| `non_pipelined_processor.py` | Simulator for non-pipelined execution.                  |
| `pipelined_processor.py`     | Simulator for pipelined execution.                      |
| `opcodemapper.txt`          | Maps opcodes to MIPS instruction types.                 |
| `regcodemapper.txt`         | Maps register names to binary encodings.                |
| `Output.txt`               | Example input for a sorting program.                    |
| `fibonacci.txt`            | Example input for Fibonacci sequence generation.         |

---

## **Future Improvements**
- Implement hazard resolution for complex scenarios.
- Introduce advanced branch prediction algorithms.
- Extend instruction support to include floating-point operations.
- Add visualization tools for pipeline stages and execution flow.

---

## **Contributing**

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push:
   ```bash
   git commit -m "Feature: Add feature description"
   git push origin feature-name
   ```
4. Open a pull request on GitHub.

---

## **License**

This project is open-source and available under the [MIT License](LICENSE).

---

