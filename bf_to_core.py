import tqdm

class BF_COMP:
    def __init__(self):
        self.s_out = "alloc_ds one 1\n" \
                     "alloc_ds zero 0\n" \
                     "alloc_ds bool\n" \
                     "alloc_ds pointer\n" \
                     "alloc_ds temp 0\n"
        self.bracket_count = 0
        self.bracket_stack = []

    def comp(self, script):
        for c in tqdm.tqdm(script):
            if c == ".":
                self.s_out+="get data pointer temp\n" \
                            "out temp\n"
            if c == ",":
                self.s_out +="inp temp\n" \
                             "set data pointer temp\n"
            if c == ">":
                self.s_out +="add one pointer\n"
            if c == "<":
                self.s_out += "sub one pointer\n"
            if c == "+":
                self.s_out += "get data pointer temp\n" \
                              "add one temp\n" \
                              "set data pointer temp\n"
            if c == "-":
                self.s_out += "get data pointer temp\n" \
                              "sub one temp\n" \
                              "set data pointer temp\n"
            if c == "[":
                self.bracket_count+=1
                self.s_out += "get data pointer temp\n" \
                              "eq temp zero bool\n" \
                              "if bool\n" \
                              "jmp close_" + \
                              str(self.bracket_count) +\
                              "\n" \
                              "end\n" \
                              "label open_" + \
                              str(self.bracket_count)+\
                              "\n"
                self.bracket_stack.append(self.bracket_count)
            if c == "]":
                bracket_num = self.bracket_stack.pop()
                self.s_out += "get data pointer temp\n" \
                              "eq temp zero bool\n" \
                              "if bool\n" \
                              "else\n" + \
                              "jmp open_" + \
                              str(bracket_num) + \
                              "\n" \
                              "end\n" \
                              "label close_"+\
                              str(bracket_num) + \
                              "\n"

        self.s_out += "alloc_ar data 30000\n"
        return self.s_out

def bf_comp(script):
    comp = BF_COMP()
    out = comp.comp(script)
    #print(out)
    return out

if __name__ == '__main__':
    #s = bf_comp(">>,>,<[>[->+>+<<]>[-<+>]<<-]>>>.")
    with open("scripts/hello_world/hello_world.bf","r") as file:
        s = bf_comp(file.read())

    with open("scripts/hello_world/hello_world.core","w") as file:
        file.write(s)
    import sasm,core_lang

    s = core_lang.compile_core(s)
    with open("scripts/hello_world/hello_world.asm","w") as file:
        file.write(s)
    s = sasm.assemble(s)
    a = ""
    with open("scripts/hello_world/hello_world.s","w") as file:
        c = 1
        for x in s:
            a+=str(x)+" "
            if c%3==0:
                a+="\n"
            c+=1
        file.write(a)
    #print(s)

    import secex

    secex.run(s)

