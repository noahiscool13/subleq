import tqdm


class BF_COMP:
    def __init__(self):
        self.s_out = "alloc_ds one 1\n" \
                     "alloc_ds zero 0\n" \
                     "alloc_ds bool\n" \
                     "alloc_ds pointer\n" \
                     "alloc_ds temp 0\n" \
                     "alloc_ds temp2 0\n"
        self.bracket_count = 0
        self.bracket_stack = []

    def comp(self, script):
        script = script.splitlines()
        for line in tqdm.tqdm(script):
            split = line.split()
            if line:
                c = split[0]
            else:
                c = ""

            if c == ".":
                self.s_out += "get data pointer temp\n" \
                              "out temp\n"
            if c == ",":
                self.s_out += "inp temp\n" \
                              "set data pointer temp\n"
            if c == ">":
                self.s_out += "add " + split[1] + " pointer\n"
            if c == "<":
                self.s_out += "sub " + split[1] + " pointer\n"
            if c == "+":
                self.s_out += "get data pointer temp\n" \
                              "add " + split[1] + " temp\n" \
                                                  "set data pointer temp\n"
            if c == "-":
                self.s_out += "get data pointer temp\n" \
                              "sub " + split[1] + " temp\n" \
                                                  "set data pointer temp\n"
            if c == "[":
                self.bracket_count += 1
                self.s_out += "get data pointer temp\n" \
                              "eq temp zero bool\n" \
                              "if bool\n" \
                              "jmp close_" + \
                              str(self.bracket_count) + \
                              "\n" \
                              "end\n" \
                              "label open_" + \
                              str(self.bracket_count) + \
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
                              "label close_" + \
                              str(bracket_num) + \
                              "\n"
            if c == "set":
                self.s_out += "set data pointer " + split[1] + "\n"
            if c == "move":
                self.s_out += "get data pointer temp\n" \
                              "set data pointer 0\n" \
                              "add pointer " \
                              + split[1] \
                              + " temp2\n" \
                                "set data temp2 temp\n"

        self.s_out += "alloc_ar data 30000\n"
        return self.s_out


def bf_comp(script):
    comp = BF_COMP()
    out = comp.comp(script)
    # print(out)
    return out


if __name__ == '__main__':
    with open("scripts/hannoi/hannoi.bf", "r") as file:
        s = bf_comp(file.read())

    print(s)
