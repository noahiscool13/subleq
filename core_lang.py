import math

from tqdm import tqdm


class Core:
    def __init__(self):
        self.s_out = "zero:0 tmp:0 ?+3\n"
        self.s_out += "one:1 min_one:-1 tmp_2:0\n"
        self.structure_stack = []
        self.label_count = 0

    def compile_core(self, script):
        split_script = script.splitlines()
        for line in tqdm(split_script):
            if not line:
                continue
            tokens = line.split()
            if tokens[0] == "alloc_ds":
                """
                > alloc_ds var_name [value]
                allocates a single value to a variable named var_name
                the default value is 0
                """
                self.s_out += "0 0 ?+3\n"
                self.s_out += tokens[1]
                if len(tokens) > 2:
                    self.s_out += ":" + tokens[2]
                else:
                    self.s_out += ":0"
                self.s_out += " 0 0\n"
            elif tokens[0] == "inp":
                """
                > inp var
                asks for a user input and stores it in variable var
                """
                self.s_out += "-1 " + tokens[1] + " ?\n"
            elif tokens[0] == "out":
                """
                > out var
                prints the value of variable var
                """
                self.s_out += tokens[1] + " -1 ?\n"
            elif tokens[0] == "sub":
                """
                > sub var_a var_b [var_c]
                subtracts the value of var_a from the value of var_b
                the result is saved in variable var_c
                if var_c is not given, the result is stored in var_b
                """
                if len(tokens) == 3:
                    self.s_out += tokens[1] + " " + tokens[2] + " ?\n"
                if len(tokens) == 4:
                    self.s_out += "tmp tmp ?\n"
                    self.s_out += tokens[3] + " " + tokens[3] + " ?\n"
                    self.s_out += tokens[2] + " tmp ?\n"
                    self.s_out += tokens[1] + " " + tokens[3] + " ?\n"
                    self.s_out += "tmp " + tokens[3] + " ?\n"

            elif tokens[0] == "add":
                """
                > add var_a var_b [var_c]
                adds the value of var_a from the value of var_b
                the result is saved in variable var_c
                if var_c is not given, the result is stored in var_b
                """
                if len(tokens) == 3:
                    self.s_out += "tmp tmp ?\n"
                    self.s_out += tokens[1] + " tmp ?\n"
                    self.s_out += "tmp " + tokens[2] + " ?\n"

                if len(tokens) == 4:
                    self.s_out += "tmp tmp ?\n"
                    self.s_out += tokens[3] + " " + tokens[3] + " ?\n"
                    self.s_out += tokens[1] + " tmp ?\n"
                    self.s_out += tokens[2] + " tmp ?\n"
                    self.s_out += "tmp " + tokens[3] + " ?\n"

            elif tokens[0] == "clr":
                """
                > clr var
                sets the value of variable var to 0
                """
                self.s_out += tokens[1] + " " + tokens[1] + " ?\n"
            elif tokens[0] == "label":
                """
                > label jmp_pos
                creates a label with name jmp_pos
                this can be used for jumps
                """
                self.s_out += tokens[1] + ":0 0 ?\n"
            elif tokens[0] == "jmp":
                """
                > jmp jmp_pos
                jump to label jmp_pos
                """
                self.s_out += "0 0 " + tokens[1] + "\n"
            elif tokens[0] == "cpy":
                """
                > cpy var_a var_b
                copy the value of variable var_a to var_b
                """
                self.s_out += "tmp tmp ?\n"
                self.s_out += tokens[2] + " " + tokens[2] + " ?\n"
                self.s_out += tokens[1] + " tmp ?\n"
                self.s_out += "tmp " + tokens[2] + " ?\n"
            elif tokens[0] == "mv":
                """
                > mv var_a var_b
                move the value of variable var_a to var_b
                """
                self.s_out += "tmp tmp ?\n"
                self.s_out += tokens[2] + " " + tokens[2] + " ?\n"
                self.s_out += tokens[1] + " tmp ?\n"
                self.s_out += "tmp " + tokens[2] + " ?\n"
                self.s_out += tokens[1] + " " + tokens[1] + " ?\n"
            elif tokens[0] == "if":
                """
                > if bool
                opens if statement
                > if bool
                > /your_if_code
                > end
                > /your_other_code
                if bool is more than 0, this will first run your_if_code
                and than continue with your_other_code.
                else, if bool is 0 or less than 0,
                it will jump straight to your_other_code
                """
                self.s_out += "tmp tmp ?\n"
                self.s_out += "tmp_2 tmp_2 ?\n"
                self.s_out += tokens[1] + " tmp_2 ?\n"
                self.label_count += 1
                self.structure_stack.append(["if", str(self.label_count)])
                self.s_out += "tmp_2 tmp if_false_" + str(self.label_count) + "\n"
            elif tokens[0] == "end":
                """
                see if
                """
                endable = self.structure_stack.pop()
                if endable[0] == "if":
                    self.s_out += "if_false_" + endable[1] + ":0 0 ?\n"
                if endable[0] == "else":
                    self.s_out += "if_end_" + endable[1] + ":0 0 ?\n"
                if endable[0] == "while":
                    self.s_out += "0 0 while_start_" + endable[1] + "\n"
                    self.s_out += "while_end_" + endable[1] + ":0 0 ?\n"
            elif tokens[0] == "else":
                endable = self.structure_stack.pop()
                assert endable[0] == "if"
                self.s_out += "0 0 if_end_" + endable[1] + "\n"
                self.s_out += "if_false_" + endable[1] + ":0 0 ?\n"
                self.structure_stack.append(["else", endable[1]])
            elif tokens[0] == "while":
                self.label_count += 1
                self.structure_stack.append(["while", str(self.label_count)])
                self.s_out += "while_start_" + str(self.label_count) + ":0 0 ?\n"
                self.s_out += "tmp tmp ?\n"
                self.s_out += "tmp_2 tmp_2 ?\n"
                self.s_out += tokens[1] + " tmp_2 ?\n"
                self.s_out += "tmp_2 tmp while_end_" + str(self.label_count) + "\n"
            elif tokens[0] == "alloc_ar":
                """
                > alloc_ar arr length
                allocates an array named arr of length length
                all values will be zero to start
                might be to long to keep alignment
                """
                length = math.ceil(int(tokens[2]) / 3) * 3
                self.s_out += "0 0 ?+" + str(length) + "\n"
                self.s_out += tokens[1] + ":0 0 0\n"
                for i in range((length // 3) - 1):
                    self.s_out += "0 0 0\n"
            elif tokens[0] == "get":
                """
                > get arr pos var
                does the same as:
                var = arr[pos]
                """
                self.label_count += 1
                self.s_out += "tmp tmp ?+3\n"
                self.s_out += "0 "+ tokens[1]+" ?\n"
                self.s_out += "?-3 tmp ?\n"
                self.s_out += tokens[2] + " tmp ?\n"
                self.s_out += "get_op_" + str(self.label_count) + " get_op_" + str(self.label_count) + " ?\n"
                self.s_out += "tmp get_op_" + str(self.label_count) + " ?\n"
                self.s_out += "tmp tmp ?\n"
                self.s_out += "get_op_" + str(self.label_count) + ":0 tmp ?\n"
                self.s_out += tokens[3] + " "+ tokens[3]+" ?\n"
                self.s_out += "tmp "+tokens[3]+" ?\n"
            elif tokens[0] == "set":
                """
                > set arr pos var
                does the same as:
                arr[pos] = var
                """
                self.label_count += 1
                self.s_out += "tmp tmp ?+3\n"
                self.s_out += "0 " + tokens[1] + " ?\n"
                self.s_out += "?-3 tmp ?\n"
                self.s_out += tokens[2] + " tmp ?\n"
                self.s_out += "set_op_final_" + str(self.label_count) + " set_op_final_" + str(self.label_count) + " ?\n"
                self.s_out += "set_op_clear_a_" + str(self.label_count) + " set_op_clear_a_" + str(
                    self.label_count) + " ?\n"
                self.s_out += "set_op_clear_b_" + str(self.label_count) + " set_op_clear_b_" + str(
                    self.label_count) + " ?\n"
                self.s_out += "tmp set_op_final_" + str(self.label_count) + " ?\n"
                self.s_out += "tmp set_op_clear_a_" + str(self.label_count) + " ?\n"
                self.s_out += "tmp set_op_clear_b_" + str(self.label_count) + " ?\n"
                self.s_out += "tmp tmp ?\n"
                self.s_out += "set_op_clear_a_" + str(self.label_count) + ":0 set_op_clear_b_" + str(
                    self.label_count) + ":0 ?\n"
                self.s_out += tokens[3]+" tmp ?\n"
                self.s_out += "tmp set_op_final_" + str(self.label_count) + ":0 ?\n"
            elif tokens[0] == "eq":
                """
                > eq var_a var_b bool
                if var_a equals var_b, bool is 1 else bool is 0
                """
                self.s_out+= tokens[3] + " "+ tokens[3] + " ?\n"
                self.s_out+= "min_one "+tokens[3]+ " ?\n"
                self.s_out += "tmp tmp ?\n"
                self.s_out += "tmp_2 tmp_2 ?\n"
                self.s_out += tokens[1] + " tmp ?\n"
                self.s_out += tokens[2] + " tmp_2 ?\n"
                self.s_out += "tmp tmp_2 ?+3\n"
                self.s_out += "one "+tokens[3]+" ?\n"
                self.s_out += "min_one tmp_2 ?+3\n"
                self.s_out += "0 0 ?+3\n"
                self.s_out += "one "+tokens[3]+" ?\n"



        self.s_out += "0 0 -1"
        return self.s_out


def compile_core(script):
    core = Core()
    return core.compile_core(script)


if __name__ == '__main__':
    # asm = compile_core("alloc_ds a 2\nalloc_ds b\nalloc_ds c\ninp b\nsub a b\nout b\nsub b a c\nout c\n" +
    #                   "inp a\nadd a b\nout b\nadd a b c\nout c\nclr a\nclr b\nclr c")
    with open("scripts/test.s", "r") as file:
        asm = compile_core(file.read())
        print(asm)
        import sbuild

        sbuild.build_run(asm, from_file=0)
