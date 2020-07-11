import uuid
import random
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()
file_extensions = ['.nix', '.h5']


def generate_experiment_id():
    while True:
        experiment_id = str(random.randint(10000, 99999))
        if not fs.exists('experiments/' + experiment_id + '/'):
            break

    return experiment_id


def check_unique_file_names(files):
    if len(files) == 1:
        return True

    for i in range(0, len(files)-1):
        for j in range(i+1, len(files) - 1):
            if files[i].name == files[j].name:
                return False

    return True


def check_file_extensions(files):
    correct_suffix = False
    for file in files:
        for i in range(0, len(file_extensions) - 1):
            if file.name.endswith(file_extensions[i]):
                correct_suffix = True
                break
        if not correct_suffix:
            return False

        correct_suffix = False
    return True


def save_files(files, experiment_id):
    for file in files:
        fs.save('experiments/' + experiment_id + '/' + file.name.lower(), file)


def is_experiment_exists(experiment_id):
    if not fs.exists('experiments/' + experiment_id + '/'):
        return False
    return True


def get_file_names(experiment_id):
    all_files = fs.listdir('experiments/' + experiment_id + '/')[1]
    nix_files = list()
    # loop files in directory
    for file in all_files:
        for i in range(0, len(file_extensions) - 1):
            if file.endswith(file_extensions[i]):
                nix_files.append(file)
                break

    return nix_files
