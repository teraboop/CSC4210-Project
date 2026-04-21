import Task4CPU


def main():
    cpu = Task4CPU.CPU()

    cpu.register_file.registers[0] = "00000000000000000000000000001100" # A = 12
    cpu.register_file.registers[1] = "00000000000000000000000000001010" # B = 10
    cpu.register_file.registers[2] = "00000000000000000000000000000110" # C = 6
    cpu.register_file.registers[3] = "00000000000000000000000000001111" # D = 15

    instructions = [
        "00000000000000001000001000110000", "00000000001000011001001100110000", "00000000010000110000000000110011"
    ]

    for i, instruction in enumerate(instructions):
        print(f"\n--- Instruction {i+1}: {instruction} ---")

        cpu.fetch(instruction)
        print(f"  [FETCH]     Instruction loaded")

        cpu.decode()
        print(f"  [DECODE]    opcode={instruction[26:]} | ALUOp={cpu.control_module.ALUOp} | "f"invert_A={cpu.control_module.invert_A} | invert_B={cpu.control_module.invert_B} | "f"RegWrite={cpu.control_module.RegWrite} | RegDst={cpu.control_module.RegDst} | "f"ALUSrc={cpu.control_module.ALUSrc} | Branch={cpu.control_module.Branch}")
        cpu.execute()
        print(f"  [EXECUTE]   A={cpu.ALU.A[0]} | B={cpu.ALU.B[0]} | Result={cpu.ALU.result}")

        cpu.write_back()
        rd = int(instruction[20:25], 2)
        print(f"  [WRITEBACK] t{rd} = {int(cpu.register_file.registers[rd], 2)}")

    print(f"\n=== Final Register Values ===")
    print(f"  t4 (A&B)   = {int(cpu.register_file.registers[4], 2)}, binary: {cpu.register_file.registers[4]}")
    print(f"  t6 (~C&D)  = {int(cpu.register_file.registers[6], 2)}, binary: {cpu.register_file.registers[6]}")
    print(f"  t0 (Y)     = {int(cpu.register_file.registers[0], 2)}, binary: {cpu.register_file.registers[0]}")

    A, B, C, D = 12, 10, 6, 15
    expected = (A & B) | ((~C & 0xFFFFFFFF) & D)
    actual = int(cpu.register_file.registers[0], 2)
    print(f"\n=== Verification: Y = A·B + C'·D ===")
    print(f"  Formula: ({A} & {B}) | (~{C} & {D}) = {expected & 0xFFFFFFFF}")
    print(f"  Y (t0)  = {actual}")
    print(f"  PASS" if actual == (expected & 0xFFFFFFFF) else "  FAIL")

main()