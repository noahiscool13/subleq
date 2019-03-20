from time import time

import sasm
import secex
import core_lang
import bf_to_core
import read_file
import os


def build(file,from_file = True):
    print("reading file")
    if from_file:
        with open(file,"r") as f:
            data = f.read()
        _,file_type = os.path.splitext(file)
        if file_type=="bf":
            file = bf_to_core.bf_comp(file)
        asm = read_file.read_subleq(file)
    else:
        asm = file
    print("assembling")
    subleq = sasm.assemble(asm)
    #subleq = asm
    print(subleq)
    print("running\nV v V")
    secex.run(subleq,mode="ascii")

def build_run(file,from_file = True):
    print("reading file")
    if from_file:
        asm = read_file.read_subleq(file)
    else:
        asm = file
    print("assembling")
    subleq = sasm.assemble(asm)
    #subleq = asm
    print(subleq)
    print("running\nV v V")
    t = time()
    secex.run(subleq,mode="ascii")
    t = time()-t
    print("This took: "+str(t)+" seconds\nThats "+str(t//60)+" min "+str(t-(t//60*60))+" sec")


if __name__ == '__main__':
    build_run("scripts/hannoi/hannoi.s")