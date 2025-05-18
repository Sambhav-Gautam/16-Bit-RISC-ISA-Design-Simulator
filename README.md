# 16-bit Instruction Set Architecture (ISA) Simulator

## Project Overview

This project implements a 16-bit Instruction Set Architecture (ISA) with a corresponding assembler and simulator. The ISA supports a variety of instructions, including arithmetic, logical, control flow, and floating-point operations. The assembler (`assembler.py`) translates assembly code into machine code, and the simulator (`simulator.py`) executes the machine code, emulating the behavior of a processor with 7 general-purpose registers, a FLAGS register, and a 256-byte memory.

### Key Features
- **16-bit ISA**: Instructions and data are 16 bits wide.
- **6 Encoding Types**: Instructions are categorized into Types A, B, C, D, E, and F, each with a unique binary format.
- **Instruction Set**: Includes arithmetic (e.g., `add`, `mul`), logical (e.g., `xor`, `and`), memory (`ld`, `st`), control flow (`jmp`, `jlt`), floating-point (`addf`, `subf`, `movf`), and halt (`hlt`) instructions.
- **Assembly Language**: Human-readable mnemonics for writing programs.
- **Tools**:
  - **Assembler**: Converts assembly code (e.g., `sim_test.txt`) into 16-bit machine code.
  - **Simulator**: Executes machine code, outputs register states and memory contents to `output.txt`.

## Instruction Set Architecture (ISA)

### Specifications
- **Registers**: 7 general-purpose registers (`R0` to `R6`) and a FLAGS register, each 16 bits.
- **Memory**: 256 bytes (128 words, as each word is 16 bits).
- **Data Types**:
  - Integer arithmetic (unsigned, whole numbers) for most instructions.
  - Floating-point arithmetic (8-bit format with 3-bit exponent and 5-bit mantissa) for `addf`, `subf`, and `movf`.
- **Addressing**: 7-bit memory addresses (0 to 127) for variables and jumps.
- **FLAGS Register**: 16-bit register with 4 active bits:
  - `V` (bit 3): Overflow flag (set by `add`, `sub`, `mul`, `div`, `addf`, `subf`).
  - `L` (bit 2): Less than flag (set by `cmp`).
  - `G` (bit 1): Greater than flag (set by `cmp`).
  - `E` (bit 0): Equal flag (set by `cmp`).
  - Bits 4–15 are unused and always 0.
- **Execution Model**: Von Neumann architecture with unified code and data memory. Execution starts at address 0 and stops at `hlt`.

### Instruction Set

| Opcode | Instruction | Semantics | Syntax | Type |
|--------|-------------|-----------|--------|------|
| `00000` | Addition | `reg1 = reg2 + reg3`. Sets overflow flag (`V=1`) and `reg1=0` if result ≥ 2¹⁶. | `add reg1 reg2 reg3` | A |
| `00001` | Subtraction | `reg1 = reg2 - reg3`. Sets overflow flag (`V=1`) and `reg1=0` if result < 0. | `sub reg1 reg2 reg3` | A |
| `00010` | Move Immediate | `reg1 = $Imm` (7-bit immediate, upper 9 bits zeroed). | `mov reg1 $Imm` | B |
| `00011` | Move Register | `reg1 = reg2`. | `mov reg1 reg2` | C |
| `00100` | Load | `reg1 = memory[mem_addr]`. | `ld reg1 mem_addr` | D |
| `00101` | Store | `memory[mem_addr] = reg1`. | `st reg1 mem_addr` | D |
| `00110` | Multiply | `reg1 = reg2 × reg3`. Sets overflow flag (`V=1`) and `reg1=0` if result ≥ 2¹⁶. | `mul reg1 reg2 reg3` | A |
| `00111` | Divide | `R0 = reg3 / reg4`, `R1 = reg3 % reg4`. If `reg4 = 0`, sets `V=1`, `R0=0`, `R1=0`. | `div reg3 reg4` | C |
| `01000` | Right Shift | `reg1 = reg1 >> $Imm` (7-bit immediate). | `rs reg1 $Imm` | B |
| `01001` | Left Shift | `reg1 = reg1 << $Imm` (7-bit immediate). | `ls reg1 $Imm` | B |
| `01010` | Exclusive OR | `reg1 = reg2 XOR reg3`. | `xor reg1 reg2 reg3` | A |
| `01011` | OR | `reg1 = reg2 OR reg3`. | `or reg1 reg2 reg3` | A |
| `01100` | AND | `reg1 = reg2 AND reg3`. | `and reg1 reg2 reg3` | A |
| `01101` | Invert | `reg1 = NOT reg2`. | `not reg1 reg2` | C |
| `01110` | Compare | Sets FLAGS based on `reg1` vs `reg2`: `E=1` if equal, `L=1` if less, `G=1` if greater. | `cmp reg1 reg2` | C |
| `01111` | Unconditional Jump | Jump to `mem_addr`. | `jmp mem_addr` | E |
| `11100` | Jump If Less Than | Jump to `mem_addr` if `L=1`. Resets FLAGS. | `jlt mem_addr` | E |
| `11101` | Jump If Greater Than | Jump to `mem_addr` if `G=1`. Resets FLAGS. | `jgt mem_addr` | E |
| `11111` | Jump If Equal | Jump to `mem_addr` if `E=1`. Resets FLAGS. | `je mem_addr` | E |
| `11010` | Halt | Stops execution. | `hlt` | F |
| `10000` | Float Addition | `reg1 = reg2 + reg3` (floating-point). Sets `V=1` and `reg1=0` if result ≥ 15.75. | `addf reg1 reg2 reg3` | A |
| `10001` | Float Subtraction | `reg1 = reg2 - reg3` (floating-point). Sets `V=1` and `reg1=0` if result ≤ 0. | `subf reg1 reg2 reg3` | A |
| `10010` | Move Float Immediate | `reg1 = $Imm` (8-bit floating-point immediate). | `movf reg1 $Imm` | B |

### Notes
- **Registers**: `R0`–`R6`, `FLAGS`. Register addresses are 3-bit (e.g., `R0=000`, `FLAGS=111`).
- **Immediate Values**:
  - `$Imm` in Type B is 7-bit for `mov`, `rs`, `ls` (0 to 127).
  - `$Imm` in `movf` is 8-bit floating-point (3-bit exponent, 5-bit mantissa, range ≈0.03125 to 15.75).
- **Memory Addresses**: 7-bit (0 to 127), resolved to variables or labels by the assembler.
- **FLAGS Operations**: Only `mov reg FLAGS` reads FLAGS; `cmp` writes FLAGS; jumps (`jlt`, `jgt`, `je`) read and reset FLAGS.
- **Floating-Point Format**: 8-bit (3-bit exponent, 5-bit mantissa). Exponent `000` is a special case (denormalized), `111` is invalid.

### Binary Encoding

Each instruction is 16 bits, categorized into 6 types:

#### Type A: 3 Registers
| Opcode (5) | Unused (2) | Reg1 (3) | Reg2 (3) | Reg3 (3) |
|----|----|----|----|----|
| 15–11 | 10–9 | 8–6 | 5–3 | 2–0 |

#### Type B: Register and Immediate
| Opcode (5) | Unused (1) | Reg1 (3) | Immediate (7 or 8) |
|----|----|----|----|
| 15–11 | 10 | 9–7 | 6–0 (or 7–0 for `movf`) |

#### Type C: 2 Registers
| Opcode (5) | Unused (5) | Reg1 (3) | Reg2 (3) |
|----|----|----|----|
| 15–11 | 10–6 | 5–3 | 2–0 |

#### Type D: Register and Memory Address
| Opcode (5) | Unused (1) | Reg1 (3) | Mem_Addr (7) |
|----|----|----|----|
| 15–11 | 10 | 9–7 | 6–0 |

#### Type E: Memory Address
| Opcode (5) | Unused (4) | Mem_Addr (7) |
|----|----|----|
| 15–11 | 10–7 | 6–0 |

#### Type F: Halt
| Opcode (5) | Unused (11) |
|----|----|
| 15–11 | 10–0 |

### Register Addresses
| Register | Address |
|----------|---------|
| R0       | `000`   |
| R1       | `001`   |
| R2       | `010`   |
| R3       | `011`   |
| R4       | `100`   |
| R5       | `101`   |
| R6       | `110`   |
| FLAGS    | `111`   |

## Assembly Language Syntax

- **Mnemonics**: Use instruction names (e.g., `add`, `mov`, `jmp`) followed by operands.
- **Registers**: `R0`–`R6`, `FLAGS`.
- **Immediates**: `$value` (e.g., `$10` for decimal 10, converted to 7-bit binary).
- **Memory Addresses**: Variable names or labels (resolved to 7-bit addresses by assembler).
- **Labels**: Defined as `label:`, used in jumps (e.g., `jmp label`).
- **Variables**: Declared with `var name` at the program start, used in `ld`/`st`.
- **Halt**: `hlt` must be the last instruction.

### Example Program
```assembly
var x
mov R1 $10    ; R1 = 10
st R1 x       ; Store R1 to variable x
ld R2 x       ; Load x to R2
cmp R1 R2     ; Compare R1 and R2 (sets E=1)
je end        ; Jump to end if equal
add R1 R1 R2  ; R1 = R1 + R2 (not executed)
end:
hlt           ; Stop execution