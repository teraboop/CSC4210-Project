from unittest import case


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
    
    def find_open_address(self):
        for address in range(self.size):
            if self.read(address) == 0:
                return address
        return None
    
    
        
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
        destination_address = destination.find_open_address()
        destination.write(destination_address, value)
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
        destination_address = destination.find_open_address()
        destination.write(destination_address, value)
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
    
    def hierarchy_memory_transfer(self, destination, local_address, direction):
        if not isinstance(destination, (Cache, RAM)):
            raise ValueError("Destination must be RAM or Cache for Cache to RAM/Cache transfer")
        value = self.read(local_address)
        match direction:
            case "up":
                match destination.type: 
                    case "RAM":              
                        destination_address = destination.find_open_address()
                        destination.write(destination_address, value)
                    case "Cache":
                        if self.prev is None or destination != self.prev:
                            raise ValueError("Invalid transfer direction: Cache can only transfer up to the previous level in the hierarchy")
                        destination_address = destination.find_open_address()
                        destination.write(destination_address, value)
            case "down":               
                if self.next is None or destination != self.next:
                    raise ValueError("Invalid transfer direction: Cache can only transfer down to the next level in the hierarchy")
                destination_address = destination.find_open_address()
                destination.write(destination_address, value)

                    
        print(f"Transferred value {value} from {self.type} to {destination.type} at address {destination_address}")

class CPU:

    def __init__(self, cache_size = 256): 
        self.data = [0] * cache_size // 8
        self.L1_cache = Cache(cache_size // 4)
        self.L2_cache = Cache(cache_size // 2)
        self.L3_cache = Cache(cache_size)
        self.RAM = RAM(cache_size * 256)
        self.SSD = SSD(cache_size * 4096)
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
        destination_address = destination.find_open_address()
        destination.write(destination_address, value)
        
