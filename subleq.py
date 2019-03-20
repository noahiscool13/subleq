PRINT_INTERUPT = 1000
PRINT_VAL = 1001

prog = []

bf = "+++"




mem = [15, 17, -1, 17, -1, -1, 16, 1, -1, 16, 3, -1, 15, 15,
        0, 0, -1, 72, 101, 108, 108, 111, 44, 32, 119, 111,
        114, 108, 100, 33, 10, 0]

def lookup(val,d):
    while val in d:
        val = d[val]
    return val

def assemble(prog):
    splt_prog = prog.split()

    for p in range(len(splt_prog)):
        str_instr = str(splt_prog[p])
        splt_prog[p] = str_instr.replace("?",str(p+1))

    pos_dict = {}
    for p in range(len(splt_prog)):
        str_instr = str(splt_prog[p])
        if ":" in str_instr:
            splt_instr = str_instr.split(":")
            pos_dict[splt_instr[0]] = p

    for p in range(len(splt_prog)):
        str_instr = str(splt_prog[p])
        if str_instr in pos_dict:
            splt_prog[p] = lookup(str_instr,pos_dict)
        elif ":" in str_instr:
            splt_instr = str_instr.split(":")
            splt_prog[p] = int(lookup(splt_instr[1],pos_dict))
        else:
            splt_prog[p] = eval(splt_prog[p])

    return splt_prog



def run(memory):
    pc = 0
    while pc>=0:
        if memory[pc] == -1:
            memory[memory[pc + 1]] = ord(input("? "))
        elif memory[pc + 1] == -1:
            print(chr(memory[memory[pc]]), end="")
        else:
            memory[memory[pc + 1]] -= memory[memory[pc]]
            if memory[memory[pc + 1]] <= 0:
                pc = memory[pc + 2]
                continue
        pc+=3

p = assemble("""t:x y n
x:7 y:7 7
n:x y t""")

print(p)
run(p)


# t:x y n
# x:7 y:7 7
# n:x y t
#
# 3, 4, 6
# 7, 7, 7
# 3, 4, 0