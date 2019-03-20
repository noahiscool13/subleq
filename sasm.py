from string import ascii_letters

from tqdm import tqdm

name_chars = ascii_letters+"_"+"".join([str(x) for x in range(10)])

class Asm:
    def __init__(self):
        self.pos_dict = {}

    def lookup(self, val):
        while val in self.pos_dict:
            val = self.pos_dict[val]
        return val

    def substitute(self, val):
        for s in self.pos_dict.keys():
            subbing = True
            while subbing:
                subbing = False
                if s in val:
                    ind = val.index(s)
                    good_l = False
                    if ind == 0:
                        good_l = True
                        pad_l = ""
                    elif val[ind-1] not in name_chars:
                        good_l = True
                        pad_l = val[ind-1]

                    good_r = False
                    if ind+len(s) == len(val):
                        good_r = True
                        pad_r = ""
                    elif val[ind + len(s)] not in name_chars:
                        good_r = True
                        pad_r = val[ind + len(s)]

                    if good_l and good_r:
                        subbing = True
                        val = val.replace(pad_l+s+pad_r,pad_l+self.pos_dict[s]+pad_r)

        return val

    def assemble(self, prog):
        """
        Compiles Subleq_asm to Subleq

        >>> asm = "p1:1 p2:2 p3:3 ? ?+1 ?-1 p4:p1 p4 p2+1"
        >>> assemble(asm)
        [1, 2, 3, 4, 6, 5, 0, 6, 2]

        :param prog: Subleq_asm
        :return: Subleq
        """
        splt_prog = prog.split()

        for p in tqdm(range(len(splt_prog))):
            str_instr = str(splt_prog[p])
            splt_prog[p] = str_instr.replace("?", str(p + 1))

        self.pos_dict = {}
        for p in tqdm(range(len(splt_prog))):
            str_instr = str(splt_prog[p])
            if ":" in str_instr:
                splt_instr = str_instr.split(":")
                self.pos_dict[splt_instr[0]] = str(p)

        for p in tqdm(range(len(splt_prog))):
            str_instr = str(splt_prog[p])

            if ":" in str_instr:
                splt_instr = str_instr.split(":")
                splt_prog[p] = splt_instr[1]
            splt_prog[p] = self.substitute(splt_prog[p])
            splt_prog[p] = eval(splt_prog[p])

        return splt_prog


def assemble(prog):
    asm = Asm()
    return asm.assemble(prog)


if __name__ == '__main__':
    #asm = "p1:1 p2:2 p3:3 ? ?+1 ?-1 p4:p1 p4 p2+1"
    asm = "a:start start:a"
    print(assemble(asm))
