class MUX:
    def __init__(self, num_inputs):
        self.num_inputs = num_inputs

    def mux(self, input_signals, select_signal):
        if select_signal < self.num_inputs:
            return input_signals[select_signal]
        else:
            raise ValueError("Select signal exceeds the number of inputs.")


class DeMUX:
    def __init__(self, num_inputs):
        self.num_inputs = num_inputs

    def demux(self, input_signal, select_signal):
        if select_signal < self.num_inputs:
            output_signals = [""] * self.num_inputs
            output_signals[select_signal] = input_signal
            return output_signals
        else:
            raise ValueError("Select signal exceeds the number of inputs.")