import os
import sys
from subprocess import check_call, check_output

commit_message = check_output('git log --format=%B |head -1', shell=True).decode()

if commit_message.startswith('SKIP BUILD'):
    print(commit_message)
    sys.exit(0)
else:
    command = 'mkdir $CIRCLE_ARTIFACTS/amber-build/ && '
              'cp amber*bz2 $CIRCLE_ARTIFACTS/amber-build/ && '
              'export PATH=/home/ubuntu/miniconda3/bin:$PATH && python scripts/upload_to_github.py'
    check_call(command, shell=True)
