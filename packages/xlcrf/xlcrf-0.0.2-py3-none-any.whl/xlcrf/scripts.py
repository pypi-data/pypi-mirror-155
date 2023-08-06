import os
from xlcrf.CRF import CRF
from xlcrf.argparser import argparser

def main():
    # argparseing
    opts = (
        # (param, help, default, type)
        ('f', 'str: comma separated list of structure excels', '', str),
        ('outdir', 'str:  directory where to export files', '.', str)
        # # --random
        # ('random',
        #  'bool: random ordering? (default: False)',
        #  False,
        #  bool),
        # # --n
        # ('n',
        #  'int: n. of records (if negative - the default - take them all)',
        #  -1, # 
        #  int),
    )
    args = argparser(opts)
    f = args['f']
    outdir = args['outdir']
    # outfiles
    outfile = os.path.basename(os.path.splitext(f)[0] + "_CRF.xlsx")
    outpath = os.path.join(outdir, outfile)
    ex1 = CRF()
    ex1.read_structure(f)
    ex1.create(outpath)
    return(0)
