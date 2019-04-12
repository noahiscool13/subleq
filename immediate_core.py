from tqdm import tqdm


class Immediate:
    def __init__(self):
        self.ims = set()
        self.header = ""
        self.script = ""

    def register(self, value):
        val_pos = str(value).replace("-","min_")
        if value not in self.ims:
            self.ims.add(value)
            self.header += "alloc_ds immediate_val_" + val_pos + " " + str(value) + "\n"
        return "immediate_val_" + val_pos

    def replace_if_int(self, token):
        if token.lstrip("-").isdigit():
            return self.register(int(token))
        return token

    def compile_immediate(self, script):
        split_script = script.splitlines()
        for line in tqdm(split_script):
            if not line:
                continue
            tokens = line.split()
            if tokens[0] not in ["alloc_ds", "alloc_ar"]:
                self.script += " ".join([self.replace_if_int(v) for v in tokens])
            else:
                self.script += " ".join(tokens)
            self.script += "\n"

        return self.header+self.script


def compile_immediate(script):
    immediate = Immediate()
    return immediate.compile_immediate(script)


if __name__ == '__main__':
    script = "alloc_ds a 2\n" \
             "add 5 a\n" \
             "out a"
    print(compile_immediate(script))
