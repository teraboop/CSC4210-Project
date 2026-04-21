class ControlModule:
    def __init__(self):
        self.RegDst = 0
        self.ALUSrc = 0
        self.MemtoReg = 0
        self.RegWrite = 0
        self.MemRead = 0
        self.MemWrite = 0
        self.Branch = 0
        self.ALUOp = '000'
        self.invert_A = 0
        self.invert_B = 0

    def generate_control_signals(self, BUS):
        opcode = BUS.data[26:32]
        funct3 = BUS.data[17:20]
        self.invert_A = 0
        self.invert_B = 0
        if opcode == '110011': # OR instruction
            self.RegDst = 1
            self.ALUSrc = 0
            self.MemtoReg = 0
            self.RegWrite = 1
            self.MemRead = 0
            self.MemWrite = 0
            self.Branch = 0
            self.ALUOp = '011'
            if funct3 == '001':
                self.invert_A = 1
            elif funct3 == '010':
                self.invert_B = 1

        elif opcode == '110000': # AND instruction
            self.RegDst = 1
            self.ALUSrc = 0
            self.MemtoReg = 0
            self.RegWrite = 1
            self.MemRead = 0
            self.MemWrite = 0
            self.Branch = 0
            self.ALUOp = '010'
            if funct3 == '001':
                self.invert_A = 1
            elif funct3 == '010':
                self.invert_B = 1