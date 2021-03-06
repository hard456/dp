import random
import os
import nixio as nix
from django.core.files.storage import FileSystemStorage
from nix import converter

file_extensions = ['.nix', '.h5']


# generates an experiment identifier
def generate_experiment_id():
    while True:
        experiment_id = str(random.randint(10000, 99999))
        if not experiment_exists(experiment_id):
            break
    return experiment_id


# checks the existence of the file
def file_exists(experiment_id, file_name):
    fs = FileSystemStorage()
    if fs.exists('experiments/' + experiment_id + '/' + file_name):
        return True
    return False


# converts metadata for the selected NIX file
def convert_metadata(experiment_id, file):
    new_name = file.split('.')[0] + '.jsonld'
    if not file_exists(experiment_id, new_name):
        try:
            nix_file = open_nix_file(experiment_id, file)
            content = converter.convert_metadata(nix_file)
            create_json_ld_file(experiment_id, new_name, content)
        except:
            return False
    return True


# checks unique file names
def check_unique_file_names(files):
    if len(files) == 1:
        return True

    for i in range(0, len(files) - 1):
        for j in range(i + 1, len(files) - 1):
            if files[i].name.lower() == files[j].name.lower():
                return False
    return True


# checks unique file names for an existing experiment
def check_files_names_experiment(files, experiment_id):
    if not check_unique_file_names(files):
        return False
    experiment_files = get_nix_files(experiment_id)
    for file in files:
        for experiment_file in experiment_files:
            if file.name.lower() == experiment_file:
                return False
    return True


# checks file extensions
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


# saves experiment files
def save_files(files, experiment_id):
    fs = FileSystemStorage()
    for file in files:
        fs.save('experiments/' + experiment_id + '/' + file.name.lower(), file)


# returns true if the experiment exists
def experiment_exists(experiment_id):
    fs = FileSystemStorage()
    if fs.exists('experiments/' + experiment_id + '/'):
        return True
    return False


# returns the NIX file names for the selected experiment
def get_nix_files(experiment_id):
    fs = FileSystemStorage()
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


# returns the json-ld file names for the selected experiment
def get_json_ld_files(experiment_id):
    fs = FileSystemStorage()
    all_files = fs.listdir('experiments/' + experiment_id + '/')[1]
    json_ld_files = list()
    # loop files in directory
    for file in all_files:
        if file.endswith('.jsonld'):
            json_ld_files.append(file)
    json_ld_files.sort()
    return json_ld_files


# returns a list of bool values ​​for the nix files of the experiment
def get_nix_transformed_bool_list(experiment_id):
    files = get_nix_files(experiment_id)
    nix_bool_list = list()
    for i in range(len(files)):
        if file_exists(experiment_id, files[i].split('.')[0] + '.jsonld'):
            nix_bool_list.append(True)
        else:
            nix_bool_list.append(False)
    return nix_bool_list


# returns the contents of the file
def read_file(experiment_id, file_name):
    fs = FileSystemStorage()
    file = fs.open('experiments/' + experiment_id + '/' + file_name)
    return file.read()


# returns an open nix file
def open_nix_file(experiment_id, file_name):
    directory = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(directory, '../media/experiments/' + experiment_id + '/' + file_name)
    nix_file = nix.File.open(file_path, nix.FileMode.ReadOnly)
    return nix_file


# creates a json-ld file and writes the contents to it
def create_json_ld_file(experiment_id, file_name, content):
    directory = os.path.dirname(__file__)  # get current directory
    file = open(os.path.join(directory, '../media/experiments/' + experiment_id + '/' + file_name), 'w+',
                encoding="utf-8")
    file.write(content)
