import os
import subprocess

subprocess.check_call(['git', 'fetch', 'origin'])
all_branches = subprocess.check_output(['git', 'branch']).decode().split('\n')
all_branches = [word.replace('*', '').strip() for word in all_branches if word]
print(all_branches)

for branch in ['circleci_27', 'circleci_34', 'circleci_35']:
    if branch not in all_branches:
        subprocess.check_call(['git', 'branch', branch])
    subprocess.check_call(['git', 'checkout', branch])
    subprocess.check_call(['git', 'pull', 'origin', branch])
    subprocess.check_call(['git', 'merge', 'master', '--no-edit'])
    subprocess.check_call(['git', 'push', 'origin', branch])

subprocess.check_call(['git', 'checkout', 'master'])
