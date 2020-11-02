"""CPU functionality."""

import sys
import os.path 

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MULT = 0b10100010
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Set up memory
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.halted = False 
        # Set up pc counter 
        self.pc = 0

    # Store value in specific RAM address
    def ram_write(self, value, address):
        self.ram[address] = value 

    # Return value of address stored in RAM
    def ram_read(self, address):
        value = self.ram[address]
        return value 

    def load(self, filename):
        """Load a program into memory."""
        address = 0

        filepath = os.path.join(os.path.dirname(__file__), filename)
        try:
            with open(filepath) as f:
                for line in f:
                    str_value = line.split("#")[0].strip()
                    try:
                        instruction = int(str_value, 2)
                        self.ram[address] = instruction
                        address += 1
                    except:
                        continue
        except:
            print(f'Could not find file: {filename}')
            sys.exit(1)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def execute(self, instruction, op_1, op_2):
        if instruction == HLT:
            self.halted = True
            self.pc += 1
        elif instruction == PRN:
            print(self.reg[op_1])
            self.pc += 2
        elif instruction == LDI:
            self.reg[op_1] = op_2
            self.pc += 3
        elif instruction == MULT:
            self.reg[op_1] *= self.reg[op_2]
            self.pc += 3
        else:
            sys.exit(1)

    def run(self):
        """Run the CPU."""
        while not self.halted:
            execute = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            self.execute(execute, operand_a, operand_b) 


