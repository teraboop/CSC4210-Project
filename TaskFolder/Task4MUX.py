class MUX:
    def __init__(self, num_inputs):
        self.num_inputs = num_inputs

    def mux(self, input_signals, select_signal):
        if select_signal < self.num_inputs:
            result = input_signals[select_signal]
            return result() if callable(result) else result
        else:
            raise ValueError("Select signal exceeds the number of inputs.")

