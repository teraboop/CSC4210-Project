class Memory:

    def __init__(self, size):
        self.size = size
        self.data = [0] * size

    def read(self, address):
        if 0 <= address < self.size:
            return self.data[address]
        else:
            raise ValueError("Address out of bounds")

    def write(self, address, value):
        if 0 <= address < self.size:
            self.data[address] = value
        else:
            raise ValueError("Address out of bounds")
        
class SSD(Memory):

    def __init__(self, size):
        super().__init__(size)
        self.type = "SSD"

    def read(self, address):
        print(f"Reading from {self.type} at address {address}")
        return super().read(address)

    def write(self, address, value):
        print(f"Writing to {self.type} at address {address} with value {value}")
        super().write(address, value)

class RAM(Memory):

    def __init__(self, size):
        super().__init__(size)
        self.type = "RAM"

    def read(self, address):
        print(f"Reading from {self.type} at address {address}")
        return super().read(address)

    def write(self, address, value):
        print(f"Writing to {self.type} at address {address} with value {value}")
        super().write(address, value)

class Cache(Memory):

    def __init__(self, size):
        super().__init__(size)
        self.type = "Cache"

    def read(self, address):
        print(f"Reading from {self.type} at address {address}")
        return super().read(address)

    def write(self, address, value):
        print(f"Writing to {self.type} at address {address} with value {value}")
        super().write(address, value)

class CPU:

    def __init__(self, cache_size):
        self.L1_cache = Cache(cache_size)
        self.L2_cache = Cache(cache_size // 2)
        self.L3_cache = Cache(cache_size // 4)

    def read(self, memory, address):
        print(f"CPU reading from {memory.type} at address {address}")
        return memory.read(address)

    def write(self, memory, address, value):
        print(f"CPU writing to {memory.type} at address {address} with value {value}")
        memory.write(address, value)