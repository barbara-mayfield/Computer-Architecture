"""CPU functionality."""

import sys
import os.path 

HLT = 0b00000001 # HALT
LDI = 0b10000010 # LOAD IMMEDIATE
PRN = 0b01000111 # PRINT
PUSH = 0b01000101
POP  = 0b01000110
CALL = 0b01010000 
RET  = 0b00010001 # RETURN 
ADD  = 0b10100000
SUB = 0b10100001
MULT = 0b10100010
DIV = 0b10100011
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        self.ram = [0] * 256 # 256-byte RAM
        self.reg = [0] * 8 # Our register 
        self.halted = False 
        self.pc = 0 # Program counter, address of the current instruction
        self.SP = 7 # Stack pointer
        self.flag = 0b00000000


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

        if len(sys.argv) != 2:
            print(f"Invalid Input")
            print(f"Usage: ls8.py program_name")

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
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "CMP":
            first = self.reg[reg_a]
            second = self.reg[reg_b]
            if first == second:
                self.flag = 0b00000001
            elif first < second:
                self.flag = 0b00000100
            elif first > second:
                self.flag = 0b00000010
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
    
    def push(self, value):
        self.SP -= 1               
        self.ram[self.SP] = value

    def pop(self):    
        value = self.ram[self.SP]
        self.SP += 1
        return value 
    
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
        elif instruction == ADD:
            self.alu("ADD", op_1, op_2)
            self.pc += 3
        elif instruction == SUB:
            self.alu("SUB", op_1, op_2)
        elif instruction == MULT:
            self.alu("MUL", op_1, op_2)
            self.pc += 3
        elif instruction == DIV:
            self.alu("DIV", op_1, op_2)
        elif instruction == PUSH:
            # decrement stack pointer
            self.SP -= 1
            # write the val stored in reg onto stack
            self.ram_write(self.reg[op_1], self.reg[self.SP])
            self.pc += 2 
        elif instruction == POP:
            # save val on top of stack to given register
            top_val = self.ram_read(self.reg[self.SP])
            self.reg[op_1] = top_val 
            self.reg[self.SP] += 1
            self.pc += 2 
        elif instruction == CALL:
            return_addr = self.pc + 2
            self.push(return_addr)

            reg_num = self.ram[self.pc + 1]
            sub_addr = self.reg[reg_num]

            self.pc = sub_addr            
        elif instruction == RET:
            return_addr = self.pop()
            self.pc = return_addr 
        elif instruction == CMP:
            self.alu("CMP", op_1, op_2)
            self.pc += 3
        elif instruction == JMP:
            self.pc = self.reg[op_1]
        elif instruction == JEQ:
            if self.flag == 0b00000001:
                self.pc = self.reg[op_1]
            else:
                self.pc += 2
        elif instruction == JNE:
            if self.flag != 0b00000001:
                self.pc = self.reg[op_1]
            else:
                self.pc += 2 
        else:
            sys.exit(1)

    def run(self):
        """Run the CPU."""
        while not self.halted:
            execute = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            self.execute(execute, operand_a, operand_b) 


