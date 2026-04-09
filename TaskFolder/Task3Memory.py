import random


class Memory:

    def __init__(self, size):
        self.cycles = 0
        self.size = size
        self.data = [""] * size
        self.pending_transfers = []
        self.bandwidth = 4
        self.transfers_this_cycle = 0

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
    
    def find_open_address(self):
        for address in range(self.size):
            if self.read(address) == "":
                return address
        return None
    
    
        
class SSD(Memory):


    def __init__(self, size):
        super().__init__(size)
        self.type = "SSD"
        self.next = None

    def read(self, address):
        print(f"Reading from {self.type} at address {address}")
        return super().read(address)

    def write(self, address, value):
        print(f"Writing to {self.type} at address {address} with value {value}")
        super().write(address, value)

    def get_value(self, address):
        
        if address < self.size:
            value = self.read(address)
            return value if value != "" else None
        return None


class DRAM(Memory):


    def __init__(self, size):
        super().__init__(size)
        self.type = "DRAM"
        self.cached_addresses = set()
        self.bandwidth = 6
        self.next = None
        self.prev = None
    
    def has_address(self, address):
        return address in self.cached_addresses
    
    def get_value(self, address):
        if self.has_address(address):
            return self.read(address)
        return self.load_from_lower_level(self.prev, address)
    
    def load_from_lower_level(self, lower_level, address):
        value = lower_level.get_value(address)
        if value is not None:
            open_address = self.find_open_address()
            if open_address is not None:
                self.write(open_address, value)
                self.cached_addresses.add(open_address)
                return value
        return None
    
    def write_back(self, destination, local_address, value):
        if not isinstance(destination, (SSD, Cache)):
            raise ValueError("Destination must be SSD or Cache for DRAM transfer")
        value = self.read(local_address)
        match destination.type: 
            case "SSD":              
                destination_address = destination.find_open_address()
                destination.write(destination_address, value)
            case "Cache":
                if self.prev is None or destination != self.prev:
                    raise ValueError("Invalid transfer direction: DRAM can only transfer up to the previous level in the hierarchy")
                destination_address = destination.find_open_address()
                if destination_address is None:
                    evicted_address = destination.evict_lru()
                    print(f"Evicted address {evicted_address} from {destination.type} to make space for new transfer")
                    destination_address = evicted_address
                destination.write(destination_address, value)

        print(f"Transferred value {value} from {self.type} to {destination.type} at address {destination_address}")

class Cache(Memory):


    def __init__(self, size):
        super().__init__(size)
        self.type = "Cache"
        self.cached_addresses = set()
        self.access_times = {}
        self.dirty_addresses = {}
        self.bandwidth = 8
        self.hits = 0
        self.misses = 0
        self.next = None
        self.prev = None


    def write(self, address, value):
        super().write(address, value)
        self.dirty_addresses[address] = True

    def has_address(self, address):
        return address in self.cached_addresses
    
    def get_value(self, address):
        if self.has_address(address):
            self.hits += 1
            self.access_times[address] = self.cycles
            return self.read(address)
        self.misses += 1

        if self.prev is not None:
            return self.load_from_lower_level(self.prev, address)
        return None
    
    def load_from_lower_level(self, lower_cache, address):
        value = lower_cache.get_value(address)
        if value is not None:
            open_address = self.find_open_address()
            if open_address is not None:
                self.write(open_address, value)
                self.cached_addresses.add(open_address)
                self.dirty_addresses[open_address] = False
                return value
            else:
                evicted_address = self.evict_lru()
                if evicted_address is not None:
                    self.write(evicted_address, value)
                    self.cached_addresses.add(evicted_address)
                    self.dirty_addresses[evicted_address] = False
                    return value
        return None
    
    def write_back(self, destination, local_address, value):
        if not isinstance(destination, (Cache, DRAM)):
            raise ValueError("Destination must be DRAM or Cache for Cache to DRAM/Cache transfer")
        value = self.read(local_address)
        match destination.type: 
            case "DRAM":              
                destination_address = destination.find_open_address()
                destination.write(destination_address, value)
            case "Cache":
                if destination != self.prev:
                    raise ValueError("Invalid transfer direction: Cache can only transfer up to the previous level in the hierarchy")
                destination_address = destination.find_open_address()
                if destination_address is None:
                    evicted_address = destination.evict_lru()
                    print(f"Evicted address {evicted_address} from {destination.type} to make space for new transfer")
                    destination_address = evicted_address
                if destination_address is None:
                    raise ValueError("No available address in destination cache after eviction attempt")
                destination.write_back(destination.prev, destination_address, value)

        print(f"Transferred value {value} from {self.type} to {destination.type} at address {destination_address}")
    
    def evict_lru(self):
        if not self.cached_addresses:
            return None
        lru_address = min(self.cached_addresses, key=lambda a: self.access_times.get(a, 0))
        if self.prev is not None:
            value = self.read(lru_address)
            lower_address = self.prev.find_open_address()
            if lower_address is None and hasattr(self.prev, 'evict_lru'):
                self.prev.evict_lru()
                lower_address = self.prev.find_open_address()
            
            if lower_address is not None:
                self.prev.write(lower_address, value)
                if hasattr(self.prev, 'cached_addresses'):
                    self.prev.cached_addresses.add(lower_address)
                print(f"Write-back: {lru_address} from {self.type} to {self.prev.type}")

        self.cached_addresses.remove(lru_address)
        self.data[lru_address] = ""
        return lru_address

class CPU:

    def __init__(self, cache_size = 256): 
        self.total_cycles = 0
        self.instruction_count = 0
        self.access_times = {}
        self.registers = [""] * (cache_size // 8)
        self.L1_cache = Cache(cache_size // 4)
        self.L2_cache = Cache(cache_size // 2)
        self.L3_cache = Cache(cache_size)
        self.L2_cache.bandwidth = 12
        self.L1_cache.bandwidth = 16
        self.DRAM = DRAM(cache_size * 16)
        self.SSD = SSD(cache_size * 64)
        self.L2_cache.next = self.L1_cache
        self.L3_cache.next = self.L2_cache
        self.L1_cache.prev = self.L2_cache
        self.L2_cache.prev = self.L3_cache
        self.L3_cache.prev = self.DRAM
        self.DRAM.next = self.L3_cache
        self.DRAM.prev = self.SSD
        self.SSD.next = self.DRAM


    def read_into_register(self, local_address, data):
        self.simulate_cycle()
        self.registers[local_address] = data
        return local_address

    def read_from_register(self, address):
        self.simulate_cycle()
        return self.registers[address]

    def write_back(self, destination, local_address):
        if destination is not self.L1_cache:
            raise ValueError("Destination must be L1 Cache for CPU to follow hierarchy memory transfer")
        value = self.read_from_register(local_address)
        destination_address = destination.find_open_address()
        if destination_address is None:
            evicted_address = destination.evict_lru()
            print(f"Evicted address {evicted_address} from {destination.type} to make space for new transfer")
            destination_address = evicted_address
        for i in range(random.randint(1, 5)):  # Simulate multiple cycles for CPU memory transfer
            self.simulate_cycle()
        destination.write_back(destination.prev, destination_address, value)
        self.registers[local_address] = ""
    
    def simulate_cycle(self):
        self.total_cycles += 1
        for memory in [self.L1_cache, self.L2_cache, self.L3_cache, self.DRAM, self.SSD]:
            memory.cycles += 1

    def execute_instruction(self, instruction, register_address):
        self.instruction_count += 1
        for _ in range(random.randint(1, 3)): # Simulate multiple cycles for instruction execution
            self.simulate_cycle()
        self.write_back(self.L1_cache, register_address)
        self.registers[register_address] = ""

    def write_register(self, local_address, value):
        self.registers[local_address] = value
        self.simulate_cycle()

    def find_open_register(self):
        for address in range(len(self.registers)):
            if self.registers[address] == "":
                return address
        return None

        
        
        
