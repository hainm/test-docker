import os
import sys
from subprocess import call, check_output

commit_message = check_output('git log --format=%B | head -1', shell=True).decode()

if '[skip build]' in commit_message.lower():
    print(commit_message)
    sys.exit(0)
else:
    # TODO : build in parallel
    commands = ['bash scripts/install_miniconda.sh',
                'bash scripts/run_docker_build.sh ambertools 2.7',
                'bash scripts/run_docker_build.sh ambertools 3.4',
                'bash scripts/run_docker_build.sh ambertools 3.5',
                'bash scripts/run_docker_build.sh ambermini 2.7',
                'bash scripts/run_docker_build.sh ambermini 3.4',
                'bash scripts/run_docker_build.sh ambermini 3.5',
    ] 
    for command in commands:
        print(command)
        call(command, shell=True)
