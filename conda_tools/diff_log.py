import sys

fn1, fn2 = sys.argv[1:]

def get_diff_lines(fn):
    with open(fn) as fh:
        return set([line for line in fh
                if line.startswith('diffing')])

for fn in get_diff_lines(fn1) - get_diff_lines(fn2):
    print(fn.strip())
