import Task3Memory
import random
def main():
    simulated_cpu = Task3Memory.CPU()
    with open("TaskFolder/instructions.txt", "r") as f:
        address = 0
        for line in f:
            instruction = line.strip()
            simulated_cpu.SSD.write(address, instruction)
            address += 1
    
    num_instructions = address
    print(f"Loaded {num_instructions} instructions into SSD\n")
    
    # Run simulation: fetch instructions and execute
    num_accesses = 200
    for access_num in range(num_accesses):
        # Randomly select an instruction address from the loaded SSD range
        instr_address = random.randint(0, num_instructions - 1)
        instruction = simulated_cpu.L1_cache.get_value(instr_address)
        
        # Store temporarily
        reg_address = simulated_cpu.find_open_register()
        if reg_address is not None:
            simulated_cpu.write_register(reg_address, instruction)
            simulated_cpu.execute_instruction(instruction, reg_address)
        
        simulated_cpu.simulate_cycle()
    
    # Generate output report
    print("\n" + "="*60)
    print("MEMORY HIERARCHY SIMULATION REPORT")
    print("="*60)
    
    # 1. Memory hierarchy configuration
    print("\n1. MEMORY HIERARCHY CONFIGURATION:")
    print(f"   L1 Cache:  {simulated_cpu.L1_cache.size} instructions")
    print(f"   L2 Cache:  {simulated_cpu.L2_cache.size} instructions")
    print(f"   L3 Cache:  {simulated_cpu.L3_cache.size} instructions")
    print(f"   DRAM:      {simulated_cpu.DRAM.size} instructions")
    print(f"   SSD:       {simulated_cpu.SSD.size} instructions")
    
    # 2. Cache hits/misses
    print("\n2. CACHE HIT/MISS STATISTICS:")
    print(f"   L1: Hits={simulated_cpu.L1_cache.hits}, Misses={simulated_cpu.L1_cache.misses}")
    print(f"   L2: Hits={simulated_cpu.L2_cache.hits}, Misses={simulated_cpu.L2_cache.misses}")
    print(f"   L3: Hits={simulated_cpu.L3_cache.hits}, Misses={simulated_cpu.L3_cache.misses}")
    
    # 3. Final state of each memory level
    print("\n3. FINAL STATE - CACHED ADDRESSES:")
    print(f"   L1: {len(simulated_cpu.L1_cache.cached_addresses)} addresses cached")
    print(f"   L2: {len(simulated_cpu.L2_cache.cached_addresses)} addresses cached")
    print(f"   L3: {len(simulated_cpu.L3_cache.cached_addresses)} addresses cached")
    print(f"   DRAM: {len(simulated_cpu.DRAM.cached_addresses)} addresses cached")
    
    # 4. Performance metrics
    print("\n4. PERFORMANCE METRICS:")
    print(f"   Total cycles: {simulated_cpu.total_cycles}")
    print(f"   Instructions executed: {simulated_cpu.instruction_count}")
    l1_hit_rate = (simulated_cpu.L1_cache.hits / 
                   (simulated_cpu.L1_cache.hits + simulated_cpu.L1_cache.misses) 
                   if (simulated_cpu.L1_cache.hits + simulated_cpu.L1_cache.misses) > 0 else 0)
    print(f"   L1 Hit Rate: {l1_hit_rate:.2%}")

    # 5. First 10 items from each memory level
    print("\n5. FIRST 10 ITEMS IN EACH MEMORY LEVEL:")
    print(f"\n   L1 Cache (first 10):")
    for i in range(min(10, len(simulated_cpu.L1_cache.data))):
        print(f"      [{i}]: {simulated_cpu.L1_cache.data[i]}")
    
    print(f"\n   L2 Cache (first 10):")
    for i in range(min(10, len(simulated_cpu.L2_cache.data))):
        print(f"      [{i}]: {simulated_cpu.L2_cache.data[i]}")
    
    print(f"\n   L3 Cache (first 10):")
    for i in range(min(10, len(simulated_cpu.L3_cache.data))):
        print(f"      [{i}]: {simulated_cpu.L3_cache.data[i]}")
    
    print(f"\n   DRAM (first 10):")
    for i in range(min(10, len(simulated_cpu.DRAM.data))):
        print(f"      [{i}]: {simulated_cpu.DRAM.data[i]}")
    
    print(f"\n   SSD (first 10):")
    for i in range(min(10, len(simulated_cpu.SSD.data))):
        print(f"      [{i}]: {simulated_cpu.SSD.data[i]}")

if __name__ == "__main__":
    main()