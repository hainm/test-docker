#!/usr/bin/env python
'''
python copy_and_post_process_bin.py source_bin_folder target_bin_folder
'''

import os
import sys
from glob import glob
import subprocess

# relative to this script
# TODO: use env?
RECIPE_DIR = os.getenv('RECIPE_DIR',
        os.path.abspath(os.path.dirname(__file__) + '/../../'))

script_template = """
#!/usr/bin/env python

import os
import sys
import subprocess

{update_prefix}

{exe}_exe = os.path.join(prefix, 'bin', 'to_be_dispatched', '{exe}')
commands = [{exe}_exe, ] + sys.argv[1:]
try:
    subprocess.call(commands)
except KeyboardInterrupt:
    pass
""".strip()

# normal distribution (require user to set AMBERHOME)
amberhome_prefix_str = """
prefix = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
os.environ['AMBERHOME'] = prefix
""".strip()

# got from get_all_exe_paths_requiring_amberhome()
DISPATCHED_PROGRAMS = [
    'respgen',
    'match',
    'antechamber',
    'charmmgen',
    'bondtype',
    'residuegen',
    'am1bcc',
    'prepgen',
    'parmchk',
    'match_atomname',
    'parmcal',
    'acdoctor',
    'translate',
    'parmchk2',
    'atomtype',
    'reduce',  # add reduce to force copying to "to_be_dispatched" folder :D
]

# handle differently
EXTRA_PROGRAMS = ['reduce', 'xleap', 'tleap', 'nab']


def _check_requiring_amberhome(program_path):
    # check if program requiring amberhome
    try:
        output = subprocess.check_output(
            'grep "AMBERHOME is not set" {}'.format(program_path), shell=True)
        output = output.decode()
    except subprocess.CalledProcessError:
        output = ''
    return output


def _is_python_script(program_path):
    try:
        with open(program_path) as fh:
            return 'env python' in fh.readline()
    except UnicodeDecodeError:
        return False


def copy_to_target_folder(all_programs,
                          dispatched_programs,
                          source_bin_dir,
                          target_bin_dir,
                          dry_run=False,
                          script_template=script_template):
    # always assuming having PREFIX env

    prefix_for_script = amberhome_prefix_str
    target_bin_dispatched = os.path.join(target_bin_dir,
                                         'to_be_dispatched')
    assert os.path.exists(target_bin_dir), '{} must exists'.format(
        target_bin_dir)

    source_bin_dir_to_be_dispatch = os.path.join(source_bin_dir,
                                                 'to_be_dispatched')

    if (source_bin_dir != target_bin_dir and
            os.path.exists(source_bin_dir_to_be_dispatch)):
        # need to copy to_be_dispatched folder to target_bin_dir
        command = [
            'cp', '-r', os.path.join(source_bin_dir, 'to_be_dispatched'),
            target_bin_dir
        ]
        if dry_run:
            print(command)
        else:
            subprocess.check_call(command)
    else:
        if not os.path.exists(target_bin_dispatched):
            if dry_run:
                print("mkddir {}".format(target_bin_dispatched))
            else:
                os.mkdir(target_bin_dispatched)

    for program in all_programs:
        print('source_bin_dir', source_bin_dir)
        original_program_path = os.path.join(source_bin_dir, program)
        final_exe_path = os.path.join(target_bin_dir, program)

        if program in dispatched_programs:
            print('program', program)
            target_program_path = os.path.join(target_bin_dir,
                                               'to_be_dispatched', program)

            if not _is_python_script(original_program_path):
                # perform copying to to_be_dispatched folder
                command = ['cp', original_program_path, target_program_path]
                # if not dispatched yet
                if not dry_run:
                    subprocess.check_call(command)
                else:
                    print(command)

            # make dispatched python script
            if program not in EXTRA_PROGRAMS:
                print('patching {}'.format(final_exe_path))
                content = script_template.format(
                    exe=program, update_prefix=prefix_for_script)
                if not dry_run:
                    with open(final_exe_path, 'w') as fh:
                        fh.write(content)
                    subprocess.check_call(['chmod', '+x', final_exe_path])
            else:
                # handle differently, copy from RECIPE_DIR subfolder
                recipe_path = RECIPE_DIR
                program_path_in_recipe = os.path.join(
                    recipe_path, 'scripts', 'patch_amberhome', program)
                if os.path.exists(original_program_path):
                    if not _is_python_script(program_path_in_recipe):
                        command = [
                            'cp', program_path_in_recipe, target_bin_dispatched
                        ]
                        if not dry_run:
                            subprocess.check_call(command)
                        else:
                            print(command)
                    print('patching {}'.format(final_exe_path))
                    with open(program_path_in_recipe, 'r') as orig_fh:
                        content = orig_fh.read().format(
                            update_prefix=prefix_for_script)
                    if not dry_run:
                        with open(final_exe_path, 'w') as final_fh:
                            final_fh.write(content)
                        subprocess.check_call(['chmod', '+x', final_exe_path])
        else:
            command = ['cp', original_program_path, final_exe_path]
            if original_program_path != final_exe_path and not os.path.isdir(
                    original_program_path):
                if not dry_run:
                    subprocess.check_call(command)
                else:
                    print(command)


def get_all_exe_paths_requiring_amberhome():
    # Set[absolute of path]
    amberhome = os.getenv('AMBERHOME', '')
    source_bin_dir = os.path.join(amberhome, 'bin')
    amberbin_pattern = os.path.join(source_bin_dir, '*')

    all_exe = []
    for program_path in glob(amberbin_pattern):
        if os.path.isfile(program_path):
            output = _check_requiring_amberhome(program_path)
            all_exe.extend([
                line.split()[2] for line in output.split('\n')
                if 'matches' in line
            ])
    return set(
        os.path.basename(program_path) for program_path in all_exe
        if program_path)


def main():
    try:
        sys.argv.remove('--dry-run')
        dry_run = True
    except ValueError:
        dry_run = False

    source_bin_dir = os.path.abspath(sys.argv[1])
    target_bin_dir = os.path.abspath(sys.argv[2])

    if dry_run:
        print('dry run\n')
    all_programs = [
        os.path.basename(exe_path)
        for exe_path in glob(os.path.join(source_bin_dir, '*'))
    ]

    all_dispatched_programs = DISPATCHED_PROGRAMS + EXTRA_PROGRAMS

    if dry_run:
        print('all_programs: ', all_programs)
        print('all_dispatched_programs: ', all_dispatched_programs)

    copy_to_target_folder(
        all_programs,
        all_dispatched_programs,
        source_bin_dir,
        target_bin_dir,
        dry_run=dry_run,
        script_template=script_template)


if __name__ == '__main__':
    main()
