import Task4CPU

class RegisterFile:
    def __init__(self):
        self.A1 = [""]
        self.A2 = [""]
        self.A3 = [""]
        self.RD1 = [""]
        self.RD2 = [""]
        self.WD1 = [""]
        self.registers = [""] * 32
        self.output_busRD1 = Task4CPU.Bus()
        self.output_busRD2 = Task4CPU.Bus()


    def read(self, DataBus):
        if not self.write_enable:
            instruction = DataBus.data
            self.A1 = instruction[6:11]
            self.A2 = instruction[11:16]
            self.A3 = instruction[16:21]
            self.RD1 = self.registers[int(self.A1, 2)]
            self.RD2 = self.registers[int(self.A2, 2)]


    def write(self, DataBus, control_signal):
        if control_signal:
            self.WD1 = DataBus.data
            self.registers[int(self.A3, 2)] = self.WD1

    def output(self):
        self.output_busRD1.data = self.RD1
        self.output_busRD2.data = self.RD2
