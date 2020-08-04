import os

import nixio as nix
from idna import unicode
from nix import utils
from nix import converter
import rdflib
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, response
from django.shortcuts import render, redirect
from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph
import requests


# displays the main page of the application
def show_home_page(request):
    return render(request, 'nix/upload_experiment.html')


# displays the experiment management page
# id - experiment id
def show_experiment_page(request, id):
    if not utils.experiment_exists(id):
        return render(request, '404.html')

    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'transformed_files': utils.get_json_ld_files(id),
        'files': utils.get_nix_files(id)
    })


# downloads the selected file
# id - experiment id
# name - file name
def download_file(request, id, name):
    fs = FileSystemStorage()
    if not utils.file_exists(id, name):
        return render(request, '404.html')

    return FileResponse(fs.open('experiments/' + id + '/' + name, 'rb'), content_type='application/force-download')


# deletes the selected file
# id - experiment id
# name - file name
def delete_file(request, id, name):
    fs = FileSystemStorage()
    if not utils.file_exists(id, name):
        return render(request, '404.html')

    try:
        fs.delete('experiments/' + id + '/' + name)
    except:
        return render(request, 'nix/experiment.html', {
            'experiment_id': id,
            'error_message': "The file was not deleted.",
            'transformed_files': utils.get_json_ld_files(id),
            'files': utils.get_nix_files(id)
        })

    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'success_message': "The file was deleted.",
        'transformed_files': utils.get_json_ld_files(id),
        'files': utils.get_nix_files(id)
    })


# displays the experiment metadata page
# id - experiment id
def show_metadata_page(request, id):
    if not utils.experiment_exists(id):
        return render(request, '404.html')

    return render(request, 'nix/metadata.html', {
        'transformed_files': utils.get_json_ld_files(id),
        'experiment_id': id
    })


# displays the experiment metadata search page
# id - experiment id
def show_find_page(request, id):
    if not utils.experiment_exists(id):
        return render(request, '404.html')

    return render(request, 'nix/find.html', {
        'experiment_id': id,
        'transformed_files': utils.get_json_ld_files(id)
    })


# creates an experiment and uploads files
def upload_experiment(request):
    if request.FILES.getlist('upload_files', True):
        files = request.FILES.getlist('upload_files')
        file = files[0]
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


# shows the converted metadata of the experiment
# id - experiment id
def show_metadata(request, id):
    file_name = request.POST.get("transformed_file", "")

    if file_name == "" or not utils.file_exists(id, file_name):
        return render(request, '404.html')

    file_content = unicode(utils.read_file(id, file_name), "utf-8")
    return render(request, 'nix/metadata.html', {
        'experiment_id': id,
        'transformed_files': utils.get_json_ld_files(id),
        'selected_file': file_name,
        'file_content': file_content
    })


# processes the SPARQL query
# id - experiment id
def process_query(request, id):
    error_message = ""
    query_result = ""

    file_name = request.POST.get("transformed_file", "")
    if file_name == "" or not utils.file_exists(id, file_name):
        return render(request, '404.html')

    query = request.POST.get("query", "")

    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, '../media/experiments/' + id + '/' + file_name)
    g = Graph()

    try:
        result = g.parse(file_path, format="json-ld")
    except:
        error_message = "Invalid JSON-LD file."

    try:
        query_result = g.query(query)
    except:
        error_message = "An error occurred while executing the query."

    return render(request, 'nix/find.html', {
        'error_message': error_message,
        'query': query,
        'experiment_id': id,
        'query_result': query_result,
        'transformed_files': utils.get_json_ld_files(id),
        'selected_file': file_name
    })


# adds files to the experiment
# id - experiment id
def upload_files(request, id):
    if not utils.experiment_exists(id):
        return render(request, '404.html')

    if request.FILES.getlist('upload_files', False):
        files = request.FILES.getlist('upload_files')

        # checks file extensions
        if not utils.check_file_extensions(files):
            return render(request, 'nix/experiment.html', {
                'experiment_id': id,
                'error_message': "The file can only have a .nix or .h5 extension.",
                'transformed_files': utils.get_json_ld_files(id),
                'files': utils.get_nix_files(id)
            })

        # checks unique file names
        if not utils.check_files_names_experiment(files, id):
            return render(request, 'nix/experiment.html', {
                'experiment_id': id,
                'error_message': "Files do not contain unique names.",
                'transformed_files': utils.get_json_ld_files(id),
                'files': utils.get_nix_files(id)
            })

        utils.save_files(files, id)
        return render(request, 'nix/experiment.html', {
            'experiment_id': id,
            'success_message': "File upload successful.",
            'transformed_files': utils.get_json_ld_files(id),
            'files': utils.get_nix_files(id)
        })
    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'error_message': "No file selected.",
        'transformed_files': utils.get_json_ld_files(id),
        'files': utils.get_nix_files(id)
    })


# converts metadata for all experiments for the selected experiment.
# id - experiment id
def convert_all(request, id):
    error_message = ""
    success_message = ""
    if not utils.experiment_exists(id):
        return render(request, '404.html')

    files = utils.get_nix_files(id)

    for i in range(len(files)):
        new_name = files[i].split('.')[0] + '.jsonld'
        try:
            content = converter.convert_metadata(id, files[i])
            utils.create_json_ld_file(id, new_name, content)
            success_message = "All files have been converted."
        except:
            error_message = "An error occurred while converting the file named " + files[i] + "."

    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'error_message': error_message,
        'success_message': success_message,
        'transformed_files': utils.get_json_ld_files(id),
        'files': utils.get_nix_files(id)
    })


# converts metadata for the selected NIX file
# id - experiment id
# name - file name
def convert_file(request, id, name):
    error_message = ""
    success_message = ""
    if not utils.file_exists(id, name):
        return render(request, '404.html')

    new_name = name.split('.')[0]+'.jsonld'
    try:
        content = converter.convert_metadata(id, name)
        utils.create_json_ld_file(id, new_name, content)
        success_message = "The requested experiment has been converted."
    except:
        error_message = "An error occurred while converting the file."

    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'error_message': error_message,
        'success_message': success_message,
        'transformed_files': utils.get_json_ld_files(id),
        'files': utils.get_nix_files(id)
    })


# HTTP 404 page
def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


# HTTP 500 page
def error_500(request):
    data = {}
    return render(request, '500.html', data)


# HTTP 403 page
def error_403(request, exception):
    data = {}
    return render(request, '403.html', data)


# HTTP 404 page
def error_400(request, exception):
    data = {}
    return render(request, '400.html', data)
