import Task4MUX
import Task4BUS


class ALU:
    def __init__(self):
        self.ALUControl = ["000"]
        self.A = [""]
        self.B = [""]
        self.result = [""]
        self.MUX = Task4MUX.MUX(5)
        self.invertAMUX = Task4MUX.MUX(2)
        self.invertBMUX = Task4MUX.MUX(2)

    def operate(self, ALUControl, A, B, invert_A, invert_B):
        A = self.invertAMUX.mux([A, self.not_op(A)], invert_A)
        B = self.invertBMUX.mux([B, self.not_op(B)], invert_B)
        self.result[0] = self.MUX.mux(
            [self.add(A, B), self.subtract(A, B), self.and_op(A, B), self.or_op(A, B), self.not_op(A)], int(ALUControl, 2)
        )

    def _to_signed(self, binary):
        val = int(binary, 2)
        return val - (1 << 32) if val >= (1 << 31) else val

    def _to_bin32(self, val):
        return bin(val & 0xFFFFFFFF)[2:].zfill(32)

    def add(self, A, B):
        return self._to_bin32(self._to_signed(A) + self._to_signed(B))

    def subtract(self, A, B):
        return self._to_bin32(self._to_signed(A) - self._to_signed(B))

    def and_op(self, A, B):
        return self._to_bin32(int(A, 2) & int(B, 2))

    def or_op(self, A, B):
        return self._to_bin32(int(A, 2) | int(B, 2))

    def not_op(self, A):
        return self._to_bin32(~int(A, 2))

    def output(self):
        return Task4BUS.BUS.load_instruction(self.result)