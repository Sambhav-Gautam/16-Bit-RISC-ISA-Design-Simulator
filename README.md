## **Project Description**

### **Instruction Set Architecture (ISA) Description**

**16-bit ISA**

This project will focus on designing a 16-bit Instruction Set Architecture (ISA). This ISA will include a set of instructions and their corresponding opcodes, as well as the syntax for an assembly language that can be used to program it.

**6 Encoding Types**

The ISA will utilize 6 distinct encoding types for instructions. The specific details of these encoding types will be provided later in the project. 

**Key Components of the ISA**

* **Instruction Set:** A collection of operations that the processor can perform.
* **Opcodes:** Binary codes used to represent different instructions.
* **Assembly Language:** A low-level programming language that uses human-readable mnemonics to represent machine code instructions.

**Project Goals**

* Define the complete instruction set for the 16-bit ISA.
* Determine the opcodes for each instruction.
* Develop the syntax rules for the corresponding assembly language.
* Create a clear and concise description of the ISA's features and capabilities.

**Next Steps**

In the following sections, we will delve deeper into the details of the 6 encoding types, the instruction set, opcodes, and assembly language syntax.

# Instruction Set Table

| Opcode | Instruction | Semantics | Syntax | Type |
|--------|-------------|-----------|--------|------|
| 00000 | Addition | Performs reg1 = reg2 + reg3. If the computation overflows, then the overflow flag is set and 0 is written in reg1 | add reg1 reg2 reg3 | A |
| 00001 | Subtraction | Performs reg1 = reg2- reg3. In case reg3 > reg2, 0 is written to reg1 and overflow flag is set. | sub reg1 reg2 reg3 | A |
| 00010 | Move Immediate | Performs reg1 = $Imm where $Imm is a 7 bit value. | mov reg1 $Imm | B |
| 00011 | Move Register | Moves contents of reg2 into reg1. | mov reg1 reg2 | C |
| 00100 | Load | Loads data from mem_addr into reg1. | ld reg1 mem_addr | D |
| 00101 | Store | Stores data from reg1 to mem_addr. | st reg1 mem_addr | D |
| 00110 | Multiply | Performs reg1 = reg2 x reg3. If the computation overflows, then the overflow flag is set and 0 is written in reg1 | mul reg1 reg2 reg3 | A |
| 00111 | Divide | Performs reg3/reg4. Stores the quotient in R0 and the remainder in R1. If reg4 is 0 then overflow flag is set and content of R0 and R1 are set to 0 | div reg3 reg4 | C |
| 01000 | Right Shift | Right shifts reg1 by $Imm, where $Imm is a 7 bit value. | rs reg1 $Imm | B |
| 01001 | Left Shift | Left shifts reg1 by $Imm, where $Imm is a 7 bit value. | ls reg1 $Imm | B |
| 01010 | Exclusive OR | Performs bitwise XOR of reg2 and reg3. Stores the result in reg1. | xor reg1 reg2 reg3 | A |
| 01011 | Or | Performs bitwise OR of reg2 and reg3. Stores the result in reg1. | or reg1 reg2 reg3 | A |
| 01100 | And | Performs bitwise AND of reg2 and reg3. Stores the result in reg1. | and reg1 reg2 reg3 | A |
| 01101 | Invert | Performs bitwise NOT of reg2. Stores the result in reg1. | not reg1 reg2 | C |
| 01110 | Compare | Compares reg1 and reg2 and sets up the FLAGS register. | cmp reg1 reg2 | C |
| 01111 | Unconditional Jump | Jumps to mem_addr, where mem_addr is a memory address. | jmp mem_addr | E |
| 11100 | Jump If Less Than | Jump to mem_addr if the less than flag is set (less than flag = 1), where mem_addr is a memory address. | jlt mem_addr | E |
| 11101 | Jump If Greater Than | Jump to mem_addr if the greater than flag is set (greater than flag = 1), where mem_addr is a memory address. | jgt mem_addr | E |
| 11111 | Jump If Equal | Jump to mem_addr if the equal flag is set (equal flag = 1), where mem_addr is a memory address. | je mem_addr | E |
| 11010 | Halt | Stops the machine from executing until reset | hlt | F |

# Additional ISA Information

## Memory and Register Specifications
- `reg[i]` denotes register
- `mem_addr` is a memory address (must be an 7-bit binary number)
- `$Imm` denotes a constant value (must be an 7-bit binary number)
- The ISA has 7 general-purpose registers R0 to R6, and FLAGS register
- It uses 16-bit instructions and 16-bit data/addresses
- This results in a total address space of 256 bytes
- This ISA only supports whole number arithmetic
- If subtraction results in a negative number, for example "3 - 4", the reg value will be set to 0 and overflow bit will be set
- All the representations of the number are in binary (unsigned)
- The registers in assembly are denoted as R0, R1, R2, ... R6 and FLAGS

## Note on Move Immediate Instruction
"mov reg $Imm": This instruction copies the $Imm(7-bit) value in the register's lower 7 bits. The upper 9 bits are zeroed out.

## FLAGS Register
The structure of the FLAGS register is as follows:

| Unused 12 bits | V | L | G | E |
|----------------|---|---|---|---|
| 15 14 13 12 11 10 9 8 7 6 5 4 | 3 | 2 | 1 | 0 |

The semantics of the flags register are:
- Overflow (V): This flag is set by (add, sub, mul, div) when the result of the operation overflows. This shows the overflow status for the last executed instruction.
- Less than (L): This flag is set by the "cmp reg1 reg2" instruction if reg1 < reg2
- Greater than (G): This flag is set by the "cmp reg1 reg2" instruction if reg1 > reg2
- Equal (E): This flag is set by the "cmp reg1 reg2" instruction if reg1 = reg2

The default state of the FLAGS register is all zeros. If an instruction does not set the FLAGS register after the execution, the FLAGS register is reset to zero.

## Operations on FLAGS Register
- The only operation allowed is the "mov reg1 FLAGS", where reg1 can be any of the registers from R0 to R6. This instruction reads FLAGS register and writes the data into reg1.
- All other operations on the FLAGS register are prohibited.
- The cmp instruction can directly write to the FLAGS register. Similarly, conditional jump instructions can read the FLAGS register.

## Example
Suppose R0 has 1110_1010_1000_1110 stored, and mov R0 R13 is executed.
The final value of R0 will be 0000_0000_0101_1101.

## Example of Conditional Jump
1. mov R5, R1 10
2. cmp R5 R1 will set the L (less than) flag in the FLAGS register.
3. jlt 001001 will read the FLAGS register and figure out that the L flag was set, and then jump to address 001001.
# ISA Binary Encoding

The ISA has 6 types of instructions with distinct encoding styles. However, each instruction is 16 bits, regardless of the type.

## Type A: 3 register type

| Opcode (5 bits) | Unused (2 bits) | reg1 (3 bits) | reg2 (3 bits) | reg3 (3 bits) |
|-----------------|-----------------|---------------|---------------|---------------|
| 15 14 13 12 11  | 10 9            | 8 7 6         | 5 4 3         | 2 1 0         |

## Type B: register and immediate type

| opcode (5 bits) | Unused (1 bit) | reg1 (3 bits) | Immediate Value (7 bits) |
|-----------------|----------------|---------------|--------------------------|
| 15 14 13 12 11  | 10             | 9 8 7         | 6 5 4 3 2 1 0            |

## Type C: 2 registers type

| Opcode (5 bits) | Unused (5 bits) | reg1 (3 bits) | reg2 (3 bits) |
|-----------------|-----------------|---------------|---------------|
| 15 14 13 12 11  | 10 9 8 7 6      | 5 4 3         | 2 1 0         |

## Type D: register and memory address type

| opcode (5 bits) | Unused (1 bit) | reg1 (3 bits) | Memory Address (7 bits) |
|-----------------|----------------|---------------|-------------------------|
| 15 14 13 12 11  | 10             | 9 8 7         | 6 5 4 3 2 1 0           |

## Type E: memory address type

| opcode (5 bits) | unused (4 bits) | Memory Address (7 bits) |
|-----------------|-----------------|-------------------------|
| 15 14 13 12 11  | 10 9 8 7        | 6 5 4 3 2 1 0           |

## Type F: halt

| opcode (5 bits) | unused (11 bits)           |
|-----------------|-----------------------------|
| 15 14 13 12 11  | 10 9 8 7 6 5 4 3 2 1 0      |

# **Binary Representation and Executable Syntax**

## Register Addresses

| Register | Address |
|---|---|
| R0 | 000 |
| R1 | 001 |
| R2 | 010 |
| R3 | 011 |
| R4 | 100 |
| R5 | 101 |
| R6 | 110 |
| FLAGS | 111 |

## Binary Structure

| Section | Content |
|---|---|
| Code | Machine instructions |
| Halt | `hlt` instruction (last instruction) |
| Variables | Data storage |

**Executable Binary Syntax**

* The machine starts executing code from address 0.
* The code execution continues until it encounters the `hlt` instruction.
* There must be only one `hlt` instruction in the entire program, and it must be the last instruction.
* The ISA follows von-Neumann architecture with a unified code and data memory.
* Variables must be allocated in the binary in program order.
