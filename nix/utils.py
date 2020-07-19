import random
import os
import nixio as nix
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()
file_extensions = ['.nix', '.h5']


def generate_experiment_id():
    while True:
        experiment_id = str(random.randint(10000, 99999))
        if not fs.exists('experiments/' + experiment_id + '/'):
            break

    return experiment_id


def is_file_exists(experiment_id, file_name):
    if fs.exists('experiments/' + experiment_id + '/' + file_name):
        return True
    return False


def check_unique_file_names(files):
    if len(files) == 1:
        return True

    for i in range(0, len(files) - 1):
        for j in range(i + 1, len(files) - 1):
            if files[i].name.lower() == files[j].name.lower():
                return False

    return True


def check_files_names_experiment(files, experiment_id):
    if not check_unique_file_names(files):
        return False
    experiment_files = get_file_names(experiment_id)
    for file in files:
        for experiment_file in experiment_files:
            if file.name.lower() == experiment_file:
                return False
    return True


def check_file_extensions(files):
    correct_suffix = False
    for file in files:
        for i in range(len(file_extensions)):
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
        for i in range(len(file_extensions)):
            if file.endswith(file_extensions[i]):
                nix_files.append(file)
                break
    nix_files.sort()
    return nix_files


def get_transformed_names(experiment_id):
    all_files = fs.listdir('experiments/' + experiment_id + '/')[1]
    json_ld_files = list()
    # loop files in directory
    for file in all_files:
        if file.endswith('.jsonld'):
            json_ld_files.append(file)
    json_ld_files.sort()
    return json_ld_files


def read_file(experiment_id, file_name):
    file = fs.open('experiments/' + experiment_id + '/' + file_name)
    return file.read()


def open_nix_file(experiment_id, file_name):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, '../media/experiments/' + experiment_id + '/' + file_name)
    nix_file = nix.File.open(file_path, nix.FileMode.ReadOnly)
    return nix_file


def create_json_ld_file (experiment_id, file_name, content):
    file = fs.open('experiments/' + experiment_id + '/' + file_name, 'w')
    file.write(content)
