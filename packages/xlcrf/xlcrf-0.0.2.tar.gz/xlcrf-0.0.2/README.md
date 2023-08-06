# xlcrf

A tool (library + command line script) to create xlsx files for data
collection with input validation, given a standard description of the
dataset (xlsx file as well).


## usage
```
l@m740n:~$ xlcrf -h
usage: xlcrf [-h] [--f F] [--outdir OUTDIR]

optional arguments:
  -h, --help       show this help message and exit
  --f F            str: comma separated list of structure excels (default: )
  --outdir OUTDIR  str: directory where to export files (default: .)
```
eg this will produce `example1_CRF.xlsx`
```
xlcrf --f example1.xlsx
```

## examples of structure files
[here](https://github.com/lbraglia/xlcrf/tree/main/examples)
