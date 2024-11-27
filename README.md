# PyMIPS-Assembler

**MIPS Instruction Execution Simulator**
This repository contains implementations of MIPS Instruction Execution in both Non-Pipelined and Pipelined Processors. The simulators handle instruction fetching, decoding, execution, memory access, and write-back phases, supporting various MIPS instruction types (R, I, J, and M).

Table of Contents
Overview
Features
Installation
Usage
Non-Pipelined Processor
Pipelined Processor
Supported Instructions
Input Format
Output Format
Files
Future Improvements
Overview
The simulators emulate MIPS assembly language instructions with a focus on learning processor execution stages and pipelining concepts. It simulates:

Instruction lifecycle (FETCH, DECODE, EXECUTE, MEMORY ACCESS, WRITEBACK)
Pipeline hazards like data dependencies and control dependencies.
Features
Non-Pipelined Processor: Sequential instruction execution.
Pipelined Processor: Parallel execution using pipelining stages.
Support for:
Arithmetic operations
Memory access
Branching
Customizable Instructions: Add your own instruction mappings in opcodemapper.txt and regcodemapper.txt.
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/your-username/MIPS-Simulator.git
cd MIPS-Simulator
Ensure Python 3.x is installed.
Create the input instruction files:
Output.txt for sorting instructions.
fibonacci.txt for Fibonacci calculations.
Usage
Non-Pipelined Processor
Prepare input files (Output.txt or fibonacci.txt) with MIPS assembly instructions in binary format.
Run the simulator:
bash
Copy code
python non_pipelined_processor.py
Follow the prompts to choose the operation (e.g., sorting or Fibonacci calculation).
Pipelined Processor
Prepare input files (Output.txt or fibonacci.txt).
Run the pipelined processor:
bash
Copy code
python pipelined_processor.py
The program will simulate instruction execution with pipelining stages.
Supported Instructions
R-Type Instructions
add: Addition
sub: Subtraction
slt: Set less than
sll: Shift left logical
I-Type Instructions
lw: Load word
sw: Store word
addi: Add immediate
beq: Branch if equal
bne: Branch if not equal
J-Type Instructions
j: Jump
jal: Jump and link
M-Type Instructions
mul: Multiply
Input Format
Instruction Format
Instructions are expected in binary format. Each instruction should follow the MIPS encoding scheme.

Example (binary format in Output.txt):

javascript
Copy code
00000000001000100001100000100000  # add $3, $1, $2
00010000001000100000000000001010  # beq $1, $2, 10
10001100001000100000000000000100  # lw $2, 4($1)
Output Format
Non-Pipelined Processor
Sequential execution logs for each instruction lifecycle stage.
Pipelined Processor
Logs for each pipeline stage.
Clear indication of data/control hazards and stalls (if any).
Files
non_pipelined_processor.py: Main file for the non-pipelined simulator.
pipelined_processor.py: Main file for the pipelined simulator.
opcodemapper.txt: Maps opcodes to MIPS operations and types.
regcodemapper.txt: Maps register names to their binary encodings.
Output.txt: Sample input for sorting program.
fibonacci.txt: Sample input for Fibonacci program.
Future Improvements
Add hazard resolution for more complex scenarios.
Optimize pipeline handling for stalls and flushes.
Implement advanced branch prediction.
Extend instruction support (e.g., floating-point operations).
Visualize execution in the pipeline.
Contributing
Feel free to fork the repository and submit pull requests for improvements or new features.

License
This project is open source and available under the MIT License.
