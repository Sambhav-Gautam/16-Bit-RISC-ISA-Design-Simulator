import sys
from typing import Dict, List, Callable, Optional

# Constants
MEMORY_SIZE = 128
REGISTER_COUNT = 8
WORD_SIZE = 16
FLOAT_PRECISION = 8
INSTRUCTION_TYPES = {
    "00000": {"name": "add", "type": "A", "func": "addition"},
    "00001": {"name": "sub", "type": "A", "func": "subtraction"},
    "00010": {"name": "mov_imm", "type": "B", "func": "move_immediate"},
    "00011": {"name": "mov_reg", "type": "C", "func": "move_register"},
    "00100": {"name": "ld", "type": "D", "func": "load"},
    "00101": {"name": "st", "type": "D", "func": "store"},
    "00110": {"name": "mul", "type": "A", "func": "multiply"},
    "00111": {"name": "div", "type": "C", "func": "division"},
    "01000": {"name": "rs", "type": "B", "func": "right_shift"},
    "01001": {"name": "ls", "type": "B", "func": "left_shift"},
    "01010": {"name": "xor", "type": "A", "func": "xor"},
    "01011": {"name": "or", "type": "A", "func": "or_operation"},
    "01100": {"name": "and", "type": "A", "func": "and_operation"},
    "01101": {"name": "not", "type": "C", "func": "invert"},
    "01110": {"name": "cmp", "type": "C", "func": "compare"},
    "01111": {"name": "jmp", "type": "E", "func": "unconditional_jump"},
    "11100": {"name": "jlt", "type": "E", "func": "jump_if_lt"},
    "11101": {"name": "jgt", "type": "E", "func": "jump_if_gt"},
    "11111": {"name": "je", "type": "E", "func": "jump_if_eq"},
    "11010": {"name": "hlt", "type": "F", "func": "halt"},
    "10000": {"name": "addf", "type": "A", "func": "f_addition"},
    "10010": {"name": "movf", "type": "B", "func": "movf_immediate"}
}

class SimulatorError(Exception):
    """Custom exception for simulator errors."""
    pass

class Simulator:
    def __init__(self, input_file: str, output_file: str):
        self.pc: int = 0
        self.halted: bool = False
        self.memory: List[str] = ["0" * WORD_SIZE] * MEMORY_SIZE
        self.registers: List[float] = [0.0] * REGISTER_COUNT  # Using float for floating-point support
        self.input_file: str = input_file
        self.output_file: str = output_file

    def binary_to_decimal(self, bin_value: str) -> int:
        """Convert binary string to decimal."""
        return sum(int(digit) << (len(bin_value) - i - 1) for i, digit in enumerate(bin_value))

    def decimal_to_binary(self, decimal: int, bits: int) -> str:
        """Convert decimal to binary with specified bits."""
        if decimal < 0:
            raise SimulatorError("Negative numbers not supported")
        binary = bin(decimal)[2:][::-1]
        binary = binary + "0" * (bits - len(binary))
        return binary[::-1][:bits]

    def floating_pt(self, binary: str) -> float:
        """Convert 8-bit floating-point binary to decimal."""
        exponent = binary[:3]
        mantissa = binary[3:]
        if exponent == "000":
            num = sum(int(mantissa[i]) * (2 ** (-i-1)) for i in range(5))
            return num * (2 ** -2)
        elif exponent != "111":
            num = 1 + sum(int(mantissa[i]) * (2 ** (-i-1)) for i in range(5))
            return num * (2 ** (self.binary_to_decimal(exponent) - 3))
        return 0.0

    def reverse_floating_pt(self, value: float) -> str:
        """Convert decimal to 8-bit floating-point binary."""
        candidates = {}
        for i in range(256):
            binary = self.decimal_to_binary(i, FLOAT_PRECISION)
            if binary.startswith("111"):
                continue
            float_val = self.floating_pt(binary)
            candidates[binary] = float_val
        for binary, float_val in candidates.items():
            if abs(float_val - value) < 1e-10:
                return binary
        return "0" * FLOAT_PRECISION  # Default to zero if no match

    def increment_pc(self) -> None:
        """Increment program counter."""
        self.pc += 1

    def addition(self, inst: str) -> None:
        """Type A: Add two registers, store in destination, set overflow flag."""
        dest = self.binary_to_decimal(inst[7:10])
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        result = self.registers[src1] + self.registers[src2]
        if result < 2 ** WORD_SIZE:
            self.registers[dest] = result
            self.registers[7] = 0
        else:
            self.registers[dest] = result % (2 ** WORD_SIZE)
            self.registers[7] = 8  # Overflow
        self.increment_pc()

    def subtraction(self, inst: str) -> None:
        """Type A: Subtract two registers, store in destination, set overflow flag."""
        dest = self.binary_to_decimal(inst[7:10])
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        result = self.registers[src1] - self.registers[src2]
        if result >= 0:
            self.registers[dest] = result
            self.registers[7] = 0
        else:
            self.registers[dest] = 0
            self.registers[7] = 8  # Underflow
        self.increment_pc()

    def move_immediate(self, inst: str) -> None:
        """Type B: Move immediate value to register."""
        dest = self.binary_to_decimal(inst[6:9])
        value = self.binary_to_decimal(inst[9:])
        self.registers[dest] = float(value)
        self.registers[7] = 0
        self.increment_pc()

    def move_register(self, inst: str) -> None:
        """Type C: Copy value from one register to another."""
        dest = self.binary_to_decimal(inst[10:13])
        src = self.binary_to_decimal(inst[13:])
        self.registers[dest] = self.registers[src]
        self.registers[7] = 0
        self.increment_pc()

    def load(self, inst: str) -> None:
        """Type D: Load value from memory to register."""
        dest = self.binary_to_decimal(inst[6:9])
        addr = self.binary_to_decimal(inst[9:])
        self.registers[dest] = float(self.binary_to_decimal(self.memory[addr]))
        self.registers[7] = 0
        self.increment_pc()

    def store(self, inst: str) -> None:
        """Type D: Store register value to memory."""
        src = self.binary_to_decimal(inst[6:9])
        addr = self.binary_to_decimal(inst[9:])
        self.memory[addr] = self.decimal_to_binary(int(self.registers[src]), WORD_SIZE)
        self.registers[7] = 0
        self.increment_pc()

    def multiply(self, inst: str) -> None:
        """Type A: Multiply two registers, store in destination, set overflow flag."""
        dest = self.binary_to_decimal(inst[7:10])
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        result = self.registers[src1] * self.registers[src2]
        if result < 2 ** WORD_SIZE:
            self.registers[dest] = result
            self.registers[7] = 0
        else:
            self.registers[dest] = result % (2 ** WORD_SIZE)
            self.registers[7] = 8  # Overflow
        self.increment_pc()

    def division(self, inst: str) -> None:
        """Type C: Divide two registers, store quotient and remainder."""
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        if self.registers[src2] == 0:
            self.registers[0] = 0
            self.registers[1] = 0
            self.registers[7] = 8  # Divide by zero
        else:
            self.registers[0] = self.registers[src1] // self.registers[src2]
            self.registers[1] = self.registers[src1] % self.registers[src2]
            self.registers[7] = 0
        self.increment_pc()

    def right_shift(self, inst: str) -> None:
        """Type B: Right shift register by immediate value."""
        dest = self.binary_to_decimal(inst[6:9])
        shift = self.binary_to_decimal(inst[9:])
        self.registers[dest] = float(int(self.registers[dest]) >> shift)
        self.registers[7] = 0
        self.increment_pc()

    def left_shift(self, inst: str) -> None:
        """Type B: Left shift register by immediate value."""
        dest = self.binary_to_decimal(inst[6:9])
        shift = self.binary_to_decimal(inst[9:])
        self.registers[dest] = float(int(self.registers[dest]) << shift)
        self.registers[7] = 0
        self.increment_pc()

    def xor(self, inst: str) -> None:
        """Type A: Bitwise XOR of two registers."""
        dest = self.binary_to_decimal(inst[7:10])
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        self.registers[dest] = float(int(self.registers[src1]) ^ int(self.registers[src2]))
        self.registers[7] = 0
        self.increment_pc()

    def or_operation(self, inst: str) -> None:
        """Type A: Bitwise OR of two registers."""
        dest = self.binary_to_decimal(inst[7:10])
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        self.registers[dest] = float(int(self.registers[src1]) | int(self.registers[src2]))
        self.registers[7] = 0
        self.increment_pc()

    def and_operation(self, inst: str) -> None:
        """Type A: Bitwise AND of two registers."""
        dest = self.binary_to_decimal(inst[7:10])
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        self.registers[dest] = float(int(self.registers[src1]) & int(self.registers[src2]))
        self.registers[7] = 0
        self.increment_pc()

    def invert(self, inst: str) -> None:
        """Type C: Bitwise NOT of a register."""
        dest = self.binary_to_decimal(inst[10:13])
        src = self.binary_to_decimal(inst[13:])
        self.registers[dest] = float(65535 - int(self.registers[src]))
        self.registers[7] = 0
        self.increment_pc()

    def compare(self, inst: str) -> None:
        """Type C: Compare two registers, set flags."""
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        if self.registers[src1] == self.registers[src2]:
            self.registers[7] = 1  # Equal
        elif self.registers[src1] < self.registers[src2]:
            self.registers[7] = 4  # Less than
        else:
            self.registers[7] = 2  # Greater than
        self.increment_pc()

    def unconditional_jump(self, inst: str) -> None:
        """Type E: Jump to address."""
        self.pc = self.binary_to_decimal(inst[9:])
        self.registers[7] = 0

    def jump_if_lt(self, inst: str) -> None:
        """Type E: Jump if less than flag is set."""
        if self.registers[7] == 4:
            self.pc = self.binary_to_decimal(inst[9:])
        else:
            self.increment_pc()
        self.registers[7] = 0

    def jump_if_gt(self, inst: str) -> None:
        """Type E: Jump if greater than flag is set."""
        if self.registers[7] == 2:
            self.pc = self.binary_to_decimal(inst[9:])
        else:
            self.increment_pc()
        self.registers[7] = 0

    def jump_if_eq(self, inst: str) -> None:
        """Type E: Jump if equal flag is set."""
        if self.registers[7] == 1:
            self.pc = self.binary_to_decimal(inst[9:])
        else:
            self.increment_pc()
        self.registers[7] = 0

    def halt(self, inst: str) -> None:
        """Type F: Halt execution."""
        self.halted = True

    def f_addition(self, inst: str) -> None:
        """Type A: Add two floating-point registers."""
        dest = self.binary_to_decimal(inst[7:10])
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        x = self.floating_pt(self.decimal_to_binary(int(self.registers[src1]), 8))
        y = self.floating_pt(self.decimal_to_binary(int(self.registers[src2]), 8))
        result = x + y
        if result < 15.75:
            self.registers[dest] = result
            self.registers[7] = 0
        else:
            self.registers[dest] = 0
            self.registers[7] = 8  # Overflow
        self.increment_pc()

    def f_subtraction(self, inst: str) -> None:
        """Type A: Subtract two floating-point registers."""
        dest = self.binary_to_decimal(inst[7::fixed typo in and_operation
10])
        src1 = self.binary_to_decimal(inst[10:13])
        src2 = self.binary_to_decimal(inst[13:])
        x = self.floating_pt(self.decimal_to_binary(int(self.registers[src1]), 8))
        y = self.floating_pt(self.decimal_to_binary(int(self.registers[src2]), 8))
        result = x - y
        if result > 0:
            self.registers[dest] = result
            self.registers[7] = 0
        else:
            self.registers[dest] = 0
            self.registers[7] = 8  # Underflow
        self.increment_pc()

    def movf_immediate(self, inst: str) -> None:
        """Type B: Move floating-point immediate to register."""
        dest = self.binary_to_decimal(inst[5:8])
        value = self.floating_pt(inst[8:])
        self.registers[dest] = value
        self.registers[7] = 0
        self.increment_pc()

    def load_program(self) -> None:
        """Load program from input file into memory."""
        try:
            with open(self.input_file, "r") as f:
                lines = [line.strip() for line in f.readlines()]
            for i, line in enumerate(lines):
                if i < MEMORY_SIZE and line:
                    self.memory[i] = line.zfill(WORD_SIZE)
        except FileNotFoundError:
            raise SimulatorError("Input file not found")

    def run(self) -> None:
        """Execute the program."""
        self.load_program()
        instruction_map: Dict[str, Callable[[str], None]] = {
            opcode: getattr(self, info["func"])
            for opcode, info in INSTRUCTION_TYPES.items()
        }

        with open(self.output_file, "w") as f:
            while not self.halted:
                if self.pc >= MEMORY_SIZE:
                    raise SimulatorError("Program counter out of bounds")
                
                inst = self.memory[self.pc]
                opcode = inst[:5]
                
                if opcode not in instruction_map:
                    raise SimulatorError(f"Invalid opcode at PC {self.pc}")

                # Execute instruction
                instruction_map[opcode](inst)

                # Output state
                output = f"{self.decimal_to_binary(self.pc, 7)}        "
                for reg in self.registers:
                    binary = self.reverse_floating_pt(reg)
                    output += f"00000000{binary} "
                print(output.strip())
                f.write(output + "\n")

            # Output memory
            for i, mem_val in enumerate(self.memory):
                print(mem_val, end="" if i == len(self.memory) - 1 else "\n")
                f.write(mem_val + ("\n" if i < len(self.memory) - 1 else ""))

def main():
    simulator = Simulator("sim_test.txt", "output.txt")
    try:
        simulator.run()
    except SimulatorError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()