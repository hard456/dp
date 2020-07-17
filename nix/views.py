import os

import nixio as nix
from idna import unicode
from nix import utils
import rdflib
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, response
from django.shortcuts import render, redirect
from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph
import requests


def show_home_page(request):
    return render(request, 'nix/upload_experiment.html')


def show_experiment_page(request, id):
    if not utils.is_experiment_exists(id):
        return render(request, '404.html')

    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'transformed_files': utils.get_transformed_names(id),
        'files': utils.get_file_names(id)
    })


def download_file(request, id, name):
    fs = FileSystemStorage()
    if not utils.is_file_exists(id, name):
        return render(request, '404.html')

    return FileResponse(fs.open('experiments/' + id + '/' + name, 'rb'), content_type='application/force-download')


def delete_file(request, id, name):
    fs = FileSystemStorage()
    if not utils.is_file_exists(id, name):
        return render(request, '404.html')

    try:
        fs.delete('experiments/' + id + '/' + name)
    except:
        return render(request, 'nix/experiment.html', {
            'experiment_id': id,
            'error_message': "The file was not deleted.",
            'transformed_files': utils.get_transformed_names(id),
            'files': utils.get_file_names(id)
        })

    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'success_message': "The file was deleted.",
        'transformed_files': utils.get_transformed_names(id),
        'files': utils.get_file_names(id)
    })


def show_metadata_page(request, id):
    if not utils.is_experiment_exists(id):
        return render(request, '404.html')

    return render(request, 'nix/metadata.html', {
        'transformed_files': utils.get_transformed_names(id),
        'experiment_id': id
    })


def show_find_page(request, id):
    if not utils.is_experiment_exists(id):
        return render(request, '404.html')

    return render(request, 'nix/find.html', {
        'experiment_id': id,
        'transformed_files': utils.get_transformed_names(id)
    })


def upload_experiment(request):
    if request.FILES.getlist('upload_files', True):
        files = request.FILES.getlist('upload_files')

        # checks unique file names
        if not utils.check_unique_file_names(files):
            return render(request, 'nix/upload_experiment.html', {
                'error_message': "The files do not have a unique name."
            })

        # checks file extensions
        if not utils.check_file_extensions(files):
            return render(request, 'nix/upload_experiment.html', {
                'error_message': "The file can only have a .nix or .h5 extension."
            })

        # generates unique experiment id
        experiment_id = utils.generate_experiment_id()

        utils.save_files(files, experiment_id)
        return redirect('/experiment/' + experiment_id + '/files')

    return render(request, 'nix/upload_experiment.html', {
        'error_message': "No file selected."
    })


def show_metadata(request, id):
    file_name = request.POST.get("transformed_file", "")

    if file_name == "" or not utils.is_file_exists(id, file_name):
        return render(request, '404.html')

    return render(request, 'nix/metadata.html', {
        'experiment_id': id,
        'transformed_files': utils.get_transformed_names(id),
        'selected_file': file_name,
        'file_content': unicode(utils.read_file(id, file_name), "utf-8")
    })


def process_query(request, id):
    error_message = ""
    query_result = ""

    file_name = request.POST.get("transformed_file", "")
    if file_name == "" or not utils.is_file_exists(id, file_name):
        return render(request, '404.html')

    query = request.POST.get("query", "")

    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, '../media/experiments/' + id + '/' + file_name)
    g = Graph()
    try:
        result = g.parse(file_path, format="json-ld")
        query_result = g.query(query)
    except:
        error_message = "An error occurred while executing the query."

    return render(request, 'nix/find.html', {
        'error_message': error_message,
        'query': query,
        'experiment_id': id,
        'query_result': query_result,
        'transformed_files': utils.get_transformed_names(id),
        'selected_file': file_name
    })


def upload_files(request, id):
    if not utils.is_experiment_exists(id):
        return render(request, '404.html')

    if request.FILES.getlist('upload_files', False):
        files = request.FILES.getlist('upload_files')

        # checks file extensions
        if not utils.check_file_extensions(files):
            return render(request, 'nix/experiment.html', {
                'experiment_id': id,
                'error_message': "The file can only have a .nix or .h5 extension.",
                'transformed_files': utils.get_transformed_names(id),
                'files': utils.get_file_names(id)
            })

        # checks unique file names
        if not utils.check_files_names_experiment(files, id):
            return render(request, 'nix/experiment.html', {
                'experiment_id': id,
                'error_message': "Files do not contain unique names.",
                'transformed_files': utils.get_transformed_names(id),
                'files': utils.get_file_names(id)
            })

        utils.save_files(files, id)
        return render(request, 'nix/experiment.html', {
            'experiment_id': id,
            'success_message': "File upload successful.",
            'transformed_files': utils.get_transformed_names(id),
            'files': utils.get_file_names(id)
        })
    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'error_message': "No file selected.",
        'transformed_files': utils.get_transformed_names(id),
        'files': utils.get_file_names(id)
    })


def convert_all(request, id):
    if not utils.is_experiment_exists(id):
        return render(request, '404.html')

    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'success_message': "All files have been converted.",
        'transformed_files': utils.get_transformed_names(id),
        'files': utils.get_file_names(id)
    })


def convert_file(request, id, name):
    if not utils.is_file_exists(id, name):
        return render(request, '404.html')

    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'success_message': "The file has been converted.",
        'transformed_files': utils.get_transformed_names(id),
        'files': utils.get_file_names(id)
    })


def testik(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, '../media/experiments/test3.nix')
    nix_file = nix.File.open(file_path, nix.FileMode.ReadOnly)

    # open nix file
    # module_dir = os.path.dirname(__file__)  # get current directory
    # file_path = os.path.join(module_dir, '../media/experiments/' + id + '/' + file_name)
    #
    # try:
    #     nix_file = nix.File.open(file_path, nix.FileMode.ReadOnly)
    #     file_format = nix_file.format
    #     version = nix_file.version
    #     nix.File.close(nix_file)
    # except:
    #     error_message = "An error occurred while opening the NIX file."

    print(nix_file.format, nix_file.version, nix_file.created_at)
    sections = nix_file.pprint()
    nix_file.close()
    return render(request, 'nix/test.html')


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_500(request):
    data = {}
    return render(request, '500.html', data)


def error_403(request, exception):
    data = {}
    return render(request, '403.html', data)


def error_400(request, exception):
    data = {}
    return render(request, '400.html', data)
