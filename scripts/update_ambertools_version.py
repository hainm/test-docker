import os
import sys
from glob import glob

def main(old_version, new_version):
    template_words = [
            'amber{}',
            'AMBER{}',
            'AmberTools{}',
            'set version = {}',
    ]
    old_words = [x.format(old_version) for x in template_words]
    new_words = [x.format(new_version) for x in template_words]
    
    for fn in glob('*') + glob('*/*'):
        if os.path.isfile(fn):
            with open(fn) as fh:
                content = fh.read()
    
            for old_word, new_word in zip(old_words, new_words):
                content = content.replace(old_word, new_word)
    
            with open(fn, 'w') as fh:
                fh.write(content)

if __name__ == '__main__':
    old_version, new_version = sys.argv[1:]
    main(old_version, new_version)
