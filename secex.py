from time import sleep


def run(memory,mode="ascii"):
    pc = 0
    while pc>=0:
        #print(pc)
        #print(memory)
        #sleep(0.05)
        if memory[pc] == -1:
            if mode == "ascii":
                memory[memory[pc + 1]] = ord(input("? "))
            else:
                memory[memory[pc + 1]] = int(input("? "))
        elif memory[pc + 1] == -1:
            if mode == "ascii":
                print(chr(memory[memory[pc]]), end="")
            else:
                print(memory[memory[pc]])
        else:
            memory[memory[pc + 1]] -= memory[memory[pc]]
            if memory[memory[pc + 1]] <= 0:
                pc = memory[pc + 2]
                continue
        pc+=3

