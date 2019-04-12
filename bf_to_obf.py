import tqdm


class OBF_COMP:
    def __init__(self):
        self.s_out = ""

    def is_command(self, char):
        return char in "+-><.,[]"

    def match(self, script):
        first = script[0]
        if first in "+-><":
            p = 0
            while p < len(script) and script[p] == first:
                p += 1
            return [first + " " + str(p) + "\n", p]

        elif first == "[":
            if script[1:3] == "-]":
                return ["set 0\n", 3]
            if script[1:3] == "->":
                p_1 = 0
                while p_1 + 2 < len(script) and script[p_1 + 2] == ">":
                    p_1 += 1
                if script[p_1 + 2] == "+":
                    p_2 = 0
                    while p_2 + p_1 + 3 < len(script) and script[p_2 + p_1 + 3] == "<":
                        p_2 += 1
                    if p_1 == p_2:
                        if script[p_2 + p_1 + 3] == "]":
                            return ["move " + str(p_1) + "\n", p_1 * 2 + 4]
            if script[1:3] == "-<":
                p_1 = 0
                while p_1 + 2 < len(script) and script[p_1 + 2] == "<":
                    p_1 += 1
                if script[p_1 + 2] == "+":
                    p_2 = 0
                    while p_2 + p_1 + 3 < len(script) and script[p_2 + p_1 + 3] == ">":
                        p_2 += 1
                    if p_1 == p_2:
                        if script[p_2 + p_1 + 3] == "]":
                            return ["move -" + str(p_1) + "\n", p_1 * 2 + 4]

        return [first + "\n", 1]

    def comp(self, script):
        script = "".join(filter(self.is_command, script))
        while len(script):
            match = self.match(script)
            self.s_out += match[0]
            script = script[match[1]:]
        return self.s_out


def obf_comp(script):
    comp = OBF_COMP()
    out = comp.comp(script)
    return out


if __name__ == '__main__':
    # with open("scripts/hannoi/hannoi.bf", "r") as file:
    #     s = obf_comp(file.read())

    with open("scripts/hello_world/hello_world.bf", "r") as file:
        s = obf_comp("[->>>+<<<][-<+>][-<<+>]")

    print(s)
