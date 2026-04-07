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
        
    def hierarchy_memory_transfer(self, destination, address):
        value = self.read(address)
        destination.write(address, value)
        print(f"Transferred value {value} from {self.type} to {destination.type} at address {address}")
    
    def mem_flush
        
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

    def hierarchy_memory_transfer(self, destination, local_address):
        if not isinstance(destination, RAM):
            raise ValueError("Destination must be RAM for SSD to RAM transfer")
        value = self.read(local_address)
        for ram_address in range(destination.size):
            if destination.read(ram_address) == 0:
                destination.write(ram_address, value)
                destination_address = ram_address
                break
        print(f"Transferred value {value} from {self.type} to {destination.type} at address {destination_address}")

    

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

    def hierarchy_memory_transfer(self, destination, local_address):
        if not isinstance(destination, (SSD, Cache)):
            raise ValueError("Destination must be SSD or Cache for RAM to SSD/Cache transfer")
        if type(destination) == Cache and destination.prev is not None:
            raise ValueError("RAM can only transfer to L3 Cache in the CPU's cache hierarchy")
        value = self.read(local_address)
        for dest_address in range(destination.size):
            if destination.read(dest_address) == 0:
                destination.write(dest_address, value)
                destination_address = dest_address
                break
        print(f"Transferred value {value} from {self.type} to {destination.type} at address {destination_address}")

class Cache(Memory):

    Cache: next = None
    Cache: prev = None

    def __init__(self, size):
        super().__init__(size)
        self.type = "Cache"

    def read(self, address):
        print(f"Reading from {self.type} at address {address}")
        return super().read(address)

    def write(self, address, value):
        print(f"Writing to {self.type} at address {address} with value {value}")
        super().write(address, value)
    
    def hierarchy_memory_transfer(self, destination, local_address):
        if not isinstance(destination,(Cache, RAM)):
            raise ValueError("Destination must be RAM or Cache for Cache to RAM/Cache transfer")
        value = self.read(local_address)
        for ram_address in range(destination.size):
            if destination.read(ram_address) == 0:
                destination.write(ram_address, value)
                destination_address = ram_address
                break
        print(f"Transferred value {value} from {self.type} to {destination.type} at address {destination_address}")

class CPU:

    def __init__(self, cache_size, memory_size):
        self.data = [0] * memory_size // 8
        self.L1_cache = Cache(cache_size)
        self.L2_cache = Cache(cache_size // 2)
        self.L3_cache = Cache(cache_size // 4)
        self.L2_cache.next = self.L1_cache
        self.L3_cache.next = self.L2_cache
        self.L1_cache.prev = self.L2_cache
        self.L2_cache.prev = self.L3_cache

    def read(self, ):
        self.L1_cache.read()
    
    def hierarchy_memory_transfer(self, destination, local_address):
        if destination is not self.L3_cache:
            raise ValueError("Destination must be within the CPU's cache hierarchy")
        value = self.read(self, local_address)
        for cache_address in range(destination.size):
            if destination.read(cache_address) == 0:
                destination.write(cache_address, value)
                destination_address = cache_address
                print(f"Transferred value {value} from CPU to {destination.type} at address {destination_address}")
                break
        
