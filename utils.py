import fnmatch
import os
import subprocess

def print_progress(fraction_completed, total_work=1.0):
    progress = fraction_completed/total_work
    print("█" * (int(20 * (progress))) + " %.1f%% \r" % (100 * progress,), end="", flush=True)


def findfiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)

def execute_bash(command):
    """Executes bash command, prints output and throws an exception on failure."""
    #print(subprocess.check_output(command.split(' '), shell=True))
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True)
    for line in process.stdout:
        print(line, end='', flush=True)
    process.wait()
    assert process.returncode == 0

def collect_files_with_ext(path, extension):
    paths = [(os.path.join(path, subpath), subpath) for subpath in os.listdir(path)]
    files = []
    for subpath, name in paths:
        if os.path.isdir(subpath):
            files += collect_files_with_ext(subpath, extension)
        else:
            if subpath.endswith(extension):
                files.append((subpath, name))
    return files
