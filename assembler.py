import sys
from typing import Dict, List, Optional

# Constants
REGISTER_OPCODES = {
    "R0": "000", "R1": "001", "R2": "010", "R3": "011",
    "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"
}
INSTRUCTION_TYPES = {
    "add": {"type": "A", "opcode": "0000000", "params": 3},
    "sub": {"type": "A", "opcode": "0000100", "params": 3},
    "mul": {"type": "A", "opcode": "0011000", "params": 3},
    "xor": {"type": "A", "opcode": "0101000", "params": 3},
    "or": {"type": "A", "opcode": "0101100", "params": 3},
    "and": {"type": "A", "opcode": "0110000", "params": 3},
    "addf": {"type": "A", "opcode": "1000000", "params": 3},
    "subf": {"type": "A", "opcode": "1000100", "params": 3},
    "mov": {"type": "C", "opcode": "0001100000", "params": 2},
    "movf": {"type": "B", "opcode": "10010", "params": 2},
    "mov_imm": {"type": "B", "opcode": "000100", "params": 2},
    "rs": {"type": "B", "opcode": "010000", "params": 2},
    "ls": {"type": "B", "opcode": "010010", "params": 2},
    "div": {"type": "C", "opcode": "0011100000", "params": 2},
    "not": {"type": "C", "opcode": "0110100000", "params": 2},
    "cmp": {"type": "C", "opcode": "0111000000", "params": 2},
    "ld": {"type": "D", "opcode": "001000", "params": 2},
    "st": {"type": "D", "opcode": "001010", "params": 2},
    "jmp": {"type": "E", "opcode": "011110000", "params": 1},
    "jlt": {"type": "E", "opcode": "111000000", "params": 1},
    "jgt": {"type": "E", "opcode": "111010000", "params": 1},
    "je": {"type": "E", "opcode": "111110000", "params": 1},
    "hlt": {"type": "F", "opcode": "1101000000000000", "params": 0}
}

class AssemblerError(Exception):
    """Custom exception for assembler errors."""
    pass

class Assembler:
    def __init__(self):
        self.labels: Dict[str, str] = {}
        self.variables: Dict[str, str] = {}
        self.instructions: List[str] = []
        self.line_no: int = 0
        self.error: bool = False

    def binary_to_decimal(self, bin_value: str) -> int:
        """Convert binary string to decimal."""
        return sum(int(digit) << (len(bin_value) - i - 1) for i, digit in enumerate(bin_value))

    def decimal_to_binary(self, decimal: int, bits: int) -> str:
        """Convert decimal to binary with specified bits."""
        if decimal < 0:
            raise AssemblerError("Negative numbers not supported")
        binary = bin(decimal)[2:][::-1]
        binary = binary + "0" * (bits - len(binary))
        return binary[::-1][:bits]

    def validate_immediate(self, value: str) -> bool:
        """Check if immediate value is valid."""
        try:
            num = int(value[1:]) if value.startswith("$") else int(value)
            return 0 <= num <= 127
        except ValueError:
            return False

    def get_register_opcode(self, reg: str) -> Optional[str]:
        """Get opcode for a register."""
        return REGISTER_OPCODES.get(reg)

    def validate_label(self, label: str) -> bool:
        """Check if label exists and is not a variable."""
        return label in self.labels and label not in self.variables

    def validate_variable(self, var: str) -> bool:
        """Check if variable exists."""
        return var in self.variables

    def process_type_a(self, inst: str, opcode: str, params: int) -> str:
        """Process Type A instructions (3 registers)."""
        parts = inst.split()
        if len(parts) != params + 1:
            raise AssemblerError(f"Instruction must have {params} parameters")
        
        reg1 = self.get_register_opcode(parts[1])
        reg2 = self.get_register_opcode(parts[2])
        reg3 = self.get_register_opcode(parts[3])
        
        if not all([reg1, reg2, reg3]):
            raise AssemblerError("Invalid register name")
        
        return opcode + reg1 + reg2 + reg3

    def process_type_b(self, inst: str, opcode: str, params: int) -> str:
        """Process Type B instructions (register and immediate)."""
        parts = inst.split()
        if len(parts) != params + 1:
            raise AssemblerError(f"Instruction must have {params} parameters")
        
        reg = self.get_register_opcode(parts[1])
        if not reg:
            raise AssemblerError("Invalid register name")
        
        if not self.validate_immediate(parts[2]):
            raise AssemblerError("Invalid immediate value")
        
        imm = self.decimal_to_binary(int(parts[2][1:]), 7)
        return opcode + reg + imm

    def process_type_b_float(self, inst: str, opcode: str, params: int) -> str:
        """Process Type B floating-point instructions."""
        parts = inst.split()
        if len(parts) != params + 1:
            raise AssemblerError(f"Instruction must have {params} parameters")
        
        reg = self.get_register_opcode(parts[1])
        if not reg:
            raise AssemblerError("Invalid register name")
        
        try:
            float_val = float(parts[2][1:])
            imm = self.reverse_floating_pt(float_val)
            if not imm:
                raise AssemblerError("Invalid floating-point value")
            return opcode + reg + imm
        except ValueError:
            raise AssemblerError("Invalid floating-point format")

    def process_type_c(self, inst: str, opcode: str, params: int) -> str:
        """Process Type C instructions (2 registers)."""
        parts = inst.split()
        if len(parts) != params + 1:
            raise AssemblerError(f"Instruction must have {params} parameters")
        
        reg1 = self.get_register_opcode(parts[1])
        reg2 = self.get_register_opcode(parts[2])
        
        if not all([reg1, reg2]):
            raise AssemblerError("Invalid register name")
        
        return opcode + reg1 + reg2

    def process_type_d(self, inst: str, opcode: str, params: int) -> str:
        """Process Type D instructions (register and variable)."""
        parts = inst.split()
        if len(parts) != params + 1:
            raise AssemblerError(f"Instruction must have {params} parameters")
        
        reg = self.get_register_opcode(parts[1])
        if not reg:
            raise AssemblerError("Invalid register name")
        
        if not self.validate_variable(parts[2]):
            raise AssemblerError("Undefined variable")
        
        return opcode + reg + self.variables[parts[2]]

    def process_type_e(self, inst: str, opcode: str, params: int) -> str:
        """Process Type E instructions (label)."""
        parts = inst.split()
        if len(parts) != params + 1:
            raise AssemblerError(f"Instruction must have {params} parameters")
        
        label = parts[1]
        if not self.validate_label(label):
            raise AssemblerError("Undefined label or variable used as label")
        
        return opcode + self.labels[label]

    def floating_pt(self, binary: str) -> float:
        """Convert 8-bit floating-point to decimal."""
        exponent = binary[:3]
        mantissa = binary[3:]
        
        if exponent == "000":
            num = sum(int(mantissa[i]) * (2 ** (-i-1)) for i in range(5))
            return num * (2 ** -2)
        elif exponent != "111":
            num = 1 + sum(int(mantissa[i]) * (2 ** (-i-1)) for i in range(5))
            return num * (2 ** (self.binary_to_decimal(exponent) - 3))
        return 0.0

    def reverse_floating_pt(self, value: float) -> Optional[str]:
        """Convert decimal to 8-bit floating-point binary."""
        candidates = {}
        for i in range(256):
            binary = self.decimal_to_binary(i, 8)
            if binary.startswith("111"):
                continue
            float_val = self.floating_pt(binary)
            candidates[binary] = float_val
        
        for binary, float_val in candidates.items():
            if abs(float_val - value) < 1e-10:
                return binary
        return None

    def process_instruction(self, inst: str) -> None:
        """Process a single instruction."""
        self.line_no += 1
        inst = inst.strip()
        if not inst:
            return

        # Handle labels
        label = None
        if ":" in inst:
            label, inst = inst.split(":", 1)
            inst = inst.strip()
            if not inst:
                return

        # Parse instruction
        parts = inst.split()
        if not parts:
            raise AssemblerError("Empty instruction")

        opcode = parts[0]
        if opcode == "var":
            if len(parts) != 2:
                raise AssemblerError("Invalid variable declaration")
            if self.instructions:  # Variables must be declared first
                raise AssemblerError("Variables must be declared at the beginning")
            self.variables[parts[1]] = "0" * 7  # Placeholder, updated later
            return

        if opcode not in INSTRUCTION_TYPES:
            raise AssemblerError("Invalid instruction")

        inst_info = INSTRUCTION_TYPES[opcode]
        inst_type = inst_info["type"]
        inst_opcode = inst_info["opcode"]
        expected_params = inst_info["params"]

        try:
            if inst_type == "A":
                result = self.process_type_a(inst, inst_opcode, expected_params)
            elif inst_type == "B":
                if opcode == "movf":
                    result = self.process_type_b_float(inst, inst_opcode, expected_params)
                else:
                    result = self.process_type_b(inst, inst_opcode, expected_params)
            elif inst_type == "C":
                result = self.process_type_c(inst, inst_opcode, expected_params)
            elif inst_type == "D":
                result = self.process_type_d(inst, inst_opcode, expected_params)
            elif inst_type == "E":
                result = self.process_type_e(inst, inst_opcode, expected_params)
            elif inst_type == "F":
                result = inst_opcode
            else:
                raise AssemblerError("Unknown instruction type")
            
            print(result)
        except AssemblerError as e:
            self.error = True
            print(f"Error in line {self.line_no}: {str(e)}")
            sys.exit(1)

    def run(self, input_file: str) -> None:
        """Main assembler function."""
        try:
            with open(input_file, "r") as f:
                lines = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print("Error: Input file not found")
            sys.exit(1)

        # First pass: Collect labels and variables
        address = 0
        for line in lines:
            if not line:
                continue
            if ":" in line:
                label = line.split(":")[0].strip()
                self.labels[label] = self.decimal_to_binary(address, 7)
                if line.split(":")[1].strip():
                    address += 1
            elif line.startswith("var"):
                continue
            else:
                self.instructions.append(line)
                address += 1

        # Assign addresses to variables
        for line in lines:
            if line.startswith("var"):
                var_name = line.split()[1]
                self.variables[var_name] = self.decimal_to_binary(address, 7)
                address += 1

        # Validate hlt instruction
        if not lines or not lines[-1].strip().endswith("hlt"):
            print("Error: Program must end with hlt instruction")
            sys.exit(1)

        # Second pass: Process instructions
        for line in lines:
            self.process_instruction(line)

def main():
    assembler = Assembler()
    assembler.run("sim_test.txt")

if __name__ == "__main__":
    main()