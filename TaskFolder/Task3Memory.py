


class Memory:

    def __init__(self, size):
        self.size = size
        self.data = [0] * size
        self.pending_transfers = []
        self.cycles = 0
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
        if not isinstance(destination, DRAM):
            raise ValueError("Destination must be DRAM for SSD to DRAM transfer")
        value = self.read(local_address)
        destination_address = destination.find_open_address()
        destination.write(destination_address, value)
        print(f"Transferred value {value} from {self.type} to {destination.type} at address {destination_address}")


class DRAM(Memory):
    def __init__(self, size):
        super().__init__(size)
        self.type = "DRAM"
        self.cached_addresses = set()
        self.bandwidth = 6
    
    def has_address(self, address):
        return address in self.cached_addresses
    
    def get_value(self, address):
        if self.has_address(address):
            return self.read(address)
        return None
    
    def load_from_ssd(self, ssd, address):
        if address < ssd.size:
            value = ssd.read(address)
            self.write(address, value)
            self.cached_addresses.add(address)
            return value
        return None

class Cache(Memory):

    Cache: next = None
    Cache: prev = None

    def __init__(self, size):
        super().__init__(size)
        self.type = "Cache"
        self.cached_addresses = set()
        self.access_times = {}
        self.bandwidth = 8
        self.hits = 0
        self.misses = 0


    def has_address(self, address):
        return address in self.cached_addresses
    
    def get_value(self, address):
        if self.has_address(address):
            self.hits += 1
            self.access_times[address] = self.cycles
            return self.read(address)
        self.misses += 1
        return None
    
    def load_from_lower_level(self, lower_cache, address):
        value = lower_cache.get_value(address)
        if value is not None:
            self.write(address, value)
            self.cached_addresses.add(address)
            return value
        return None
    
    def hierarchy_memory_transfer(self, destination, local_address, direction):
        if not isinstance(destination, (Cache, DRAM)):
            raise ValueError("Destination must be DRAM or Cache for Cache to DRAM/Cache transfer")
        value = self.read(local_address)
        match direction:
            case "up":
                match destination.type: 
                    case "DRAM":              
                        destination_address = destination.find_open_address()
                        destination.write(destination_address, value)
                    case "Cache":
                        if self.prev is None or destination != self.prev:
                            raise ValueError("Invalid transfer direction: Cache can only transfer up to the previous level in the hierarchy")
                        destination_address = destination.find_open_address()
                        if destination_address is None:
                            evicted_address = destination.evict_lru()
                            print(f"Evicted address {evicted_address} from {destination.type} to make space for new transfer")
                            destination_address = evicted_address
                        destination.write(destination_address, value)
            case "down":               
                if self.next is None or destination != self.next:
                    raise ValueError("Invalid transfer direction: Cache can only transfer down to the next level in the hierarchy")
                destination_address = destination.find_open_address()
                destination.write(destination_address, value)

                    
        print(f"Transferred value {value} from {self.type} to {destination.type} at address {destination_address}")
    
    def evict_lru(self):
        if self.cached_addresses:
            lru_address = min(self.cached_addresses, key=lambda a: self.access_times.get(a, 0))
            self.data[lru_address] = 0
            self.cached_addresses.remove(lru_address)
            self.data[lru_address] = 0
            return lru_address

class CPU:

    def __init__(self, cache_size = 256): 
        self.total_cycles = 0
        self.instruction_count = 0
        self.data = [0] * cache_size // 8
        self.L1_cache = Cache(cache_size // 4)
        self.L2_cache = Cache(cache_size // 2)
        self.L3_cache = Cache(cache_size)
        self.L2_cache.bandwidth = 12
        self.L1_cache.bandwidth = 16
        self.DRAM = DRAM(cache_size * 256)
        self.SSD = SSD(cache_size * 2048)
        self.L2_cache.next = self.L1_cache
        self.L3_cache.next = self.L2_cache
        self.L1_cache.prev = self.L2_cache
        self.L2_cache.prev = self.L3_cache

    def read(self, local_address):
        value = self.L1_cache.get_value(local_address)
        if value is None:
            value = self.L2_cache.load_from_lower_level(self.L3_cache, local_address)
        if value is None:
            value = self.L2_cache.load_from_lower_level(self.DRAM, local_address)
        if value is None:
            self.DRAM.load_from_ssd(self.SSD, local_address)
        


    def hierarchy_memory_transfer(self, destination, local_address):
        if destination is not self.L1_cache:
            raise ValueError("Destination must be L1 Cache for CPU to follow hierarchy memory transfer")
        value = self.read(self, local_address)
        destination_address = destination.find_open_address()
        destination.write(destination_address, value)
    
    def simulate_cycle(self):
        self.total_cycles += 1
        self.L1_cache.cycles += 1
        self.L2_cache.cycles += 1
        self.L3_cache.cycles += 1
        self.DRAM.cycles += 1
        self.SSD.cycles += 1
        
