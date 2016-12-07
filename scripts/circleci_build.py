import os
import sys
from subprocess import check_call, check_output

commit_message = check_output('git log --format=%B |head -1', shell=True).decode()

if commit_message.startswith('SKIP BUILD')
    print(commit_message)
    sys.exit(0)
else:
    command = "source scripts/install_miniconda.sh && source build.sh"
    check_call(command, shell=True)
