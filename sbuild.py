from time import time

import sasm
import secex
import core_lang
import bf_to_core
import read_file
import os


class Build:
    def __init__(self, file, run=True, save=True, mode="ascii"):
        self.file = file
        self.run = run
        self.save = save
        self.mode = mode

    def build(self):
        print("reading file")
        _, file_type = os.path.splitext(self.file)
        with open(self.file, "r") as f:
            self.file = f.read()
        if file_type == ".bf":
            self.build_bf()
        if file_type == ".core":
            self.build_core()
        if file_type == ".asm":
            self.build_asm()
        if file_type == ".s":
            self.build_s()

    def build_s(self):
        if self.run:
            print("Running script:")
            secex.run(self.file, mode=self.mode)

    def build_asm(self):
        print("Building asm -> subleq:")
        self.file = sasm.assemble(self.file)
        self.build_s()

    def build_core(self):
        print("Building core -> asm:")
        self.file = core_lang.compile_core(self.file)
        self.build_asm()

    def build_bf(self):
        print("Building bf -> core:")
        self.file = bf_to_core.bf_comp(self.file)
        self.build_core()


def build(file, run=True, save=True, mode="ascii"):
    builder = Build(file, run, save, mode)
    builder.build()


if __name__ == '__main__':
    build("scripts/hannoi/hannoi.bf")
