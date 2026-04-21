import Task4BUS

class RegisterFile:
    def __init__(self):
        self.A1 = [""]
        self.A2 = [""]
        self.A3 = [""]
        self.RD1 = [""]
        self.RD2 = [""]
        self.WD1 = [""]
        self.registers = [""] * 32
        self.output_busRD1 = Task4BUS.BUS()
        self.output_busRD2 = Task4BUS.BUS()


    def read(self, DataBus):
        instruction = DataBus.data
        self.A1 = instruction[7:12]
        self.A2 = instruction[12:17]
        self.A3 = instruction[20:25]
        self.RD1 = self.registers[int(self.A1, 2)]
        self.RD2 = self.registers[int(self.A2, 2)]
        self.output()


    def write(self, DataBus, control_signal):
        if control_signal:
            self.WD1 = DataBus.data
            self.registers[int(self.A3, 2)] = self.WD1

    def output(self):
        self.output_busRD1.load_instruction(self.RD1)
        self.output_busRD2.load_instruction(self.RD2)
