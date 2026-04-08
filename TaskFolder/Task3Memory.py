


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

    DRAM: next = None

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

    def get_value(self, address):
        
        if address < self.size:
            return self.read(address)
        return None


class DRAM(Memory):

    SSD: prev = None
    Cache: next = None

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
        return self.load_from_lower_level(self.prev, address)
    
    def load_from_lower_level(self, lower_level, address):
        value = lower_level.get_value(address)
        if value is not None:
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
        self.dirty_addresses = {}
        self.bandwidth = 8
        self.hits = 0
        self.misses = 0


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
            self.write(address, value)
            self.cached_addresses.add(address)
            self.dirty_addresses[address] = False
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
        self.DRAM.next = self.L3_cache
        self.DRAM.prev = self.SSD
        self.SSD.next = self.DRAM


    def read(self, local_address):
        return self.L1_cache.get_value(local_address)

    def hierarchy_memory_transfer(self, destination, local_address):
        if destination is not self.L1_cache:
            raise ValueError("Destination must be L1 Cache for CPU to follow hierarchy memory transfer")
        value = self.read(self, local_address)
        destination_address = destination.find_open_address()
        if destination_address is None:
            evicted_address = destination.evict_lru()
            print(f"Evicted address {evicted_address} from {destination.type} to make space for new transfer")
            destination_address = evicted_address
        destination.write(destination_address, value)
    
    def simulate_cycle(self):
        self.total_cycles += 1
        self.L1_cache.cycles += 1
        self.L2_cache.cycles += 1
        self.L3_cache.cycles += 1
        self.DRAM.cycles += 1
        self.SSD.cycles += 1
        
