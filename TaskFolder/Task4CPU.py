import Task4RegisterFile
import Task4BUS
import Task4ALU
import Task4MUX
import Task4ControlModule


class CPU:
    def __init__(self):
        self.PC = 0
        self.register_file = Task4RegisterFile.RegisterFile()
        self.InputBus = Task4BUS.BUS()
        self.ALU = Task4ALU.ALU()
        self.control_module = Task4ControlModule.ControlModule()

    def fetch(self, instruction):
        self.InputBus.load_instruction(instruction)

    def decode(self):
        self.control_module.generate_control_signals(self.InputBus)
        self.register_file.read(self.InputBus)

    def execute(self):
        self.ALU.operate(
            self.control_module.ALUOp,
            self.register_file.output_busRD1.data,
            self.register_file.output_busRD2.data,
            self.control_module.invert_A,
            self.control_module.invert_B
        )

    def write_back(self):
        self.register_file.write(self.ALU.output(), self.control_module.RegWrite)