import os

import nixio as nix
import uuid
from nix import utils
import rdflib
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, response
from django.shortcuts import render, redirect
from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph
import requests


def index(request):
    return render(request, 'nix/index.html')


def show_experiment(request, id):

    if not utils.is_experiment_exists(id):
        return render(request, '404.html')

    file_names = utils.get_file_names(id)

    return render(request, 'nix/experiment.html', {
        'experiment_id': id,
        'files': file_names
    })


def download_experiment(request, id):
    fs = FileSystemStorage()
    if not fs.exists('experiments/' + id + '/'):
        return render(request, '404.html')

    files = fs.listdir('experiments/' + id + '/')[1]

    # loop files in directory
    for file in files:
        if file.endswith(".nix") or file.endswith(".h5"):
            file_name = file
            break

    return FileResponse(fs.open('experiments/' + id + '/' + file_name, 'rb'), content_type='application/force-download')


def download_json_ld(request, id):
    fs = FileSystemStorage()
    if not fs.exists('experiments/' + id + '/'):
        return render(request, '404.html')

    files = fs.listdir('experiments/' + id + '/')[1]

    # loop files in directory
    for file in files:
        if file.endswith(".jsonld"):
            file_name = file
            break

    return FileResponse(fs.open('experiments/' + id + '/' + file_name, 'rb'), content_type='application/force-download')


def show_json_ld(request, id):
    fs = FileSystemStorage()
    file_name = ""
    file_created = False
    if not fs.exists('experiments/' + id + '/'):
        return render(request, '404.html')

    files = fs.listdir('experiments/' + id + '/')[1]

    # loop files in directory
    for file in files:
        if file.endswith(".jsonld"):
            file_name = file
            file_created = True
            break

    return render(request, 'nix/json-ld.html', {
        'file_name': file_name,
        'file_created': file_created,
        'experiment_id': id
    })


def show_graph(request, id):
    fs = FileSystemStorage()
    if not fs.exists('experiments/' + id + '/'):
        return render(request, '404.html')
    return render(request, 'nix/graph.html', {
        'experiment_id': id
    })


def show_sparql(request, id):
    fs = FileSystemStorage()
    if not fs.exists('experiments/' + id + '/'):
        return render(request, '404.html')
    return render(request, 'nix/sparql.html', {
        'experiment_id': id
    })


def upload_experiment(request):
    if request.method == 'POST' and request.FILES.getlist('myfile', False):
        files = request.FILES.getlist('myfile')

        # checks unique file names
        if not utils.check_unique_file_names(files):
            return render(request, 'nix/index.html', {
                'error_message': "The files do not have a unique name."
            })

        # checks file extensions
        if not utils.check_file_extensions(files):
            return render(request, 'nix/index.html', {
                'error_message': "The file can only have a .nix or .h5 extension."
            })

        # generates unique experiment id
        experiment_id = utils.generate_experiment_id()

        utils.save_files(files, experiment_id)
        return redirect('/experiment/' + experiment_id + '/experiment')
    return render(request, 'nix/index.html', {
        'error_message': "No file was selected or the post method was not selected."
    })


def convert_experiment(request, id):
    fs = FileSystemStorage()
    if not fs.exists('experiments/' + id + '/'):
        return render(request, '404.html')
    return render(request, 'nix/json-ld.html', {
        'experiment_id': id
    })


def process_query(request, id):
    error_message = ""
    query_result = ""
    file_created = False
    fs = FileSystemStorage()
    if not fs.exists('experiments/' + id + '/'):
        return render(request, '404.html')

    query = request.POST.get("query", "")

    files = fs.listdir('experiments/' + id + '/')[1]

    # loop files in directory
    for file in files:
        if file.endswith(".jsonld"):
            file_name = file
            file_created = True
            break

    if file_created:
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, '../media/experiments/' + id + '/' + file_name)
        g = Graph()
        try:
            result = g.parse(file_path, format="json-ld")
            query_result = g.query(query)
        except:
            error_message = "An error occurred while executing the query."
    else:
        error_message = "The JSON-LD file has not been created yet."

    return render(request, 'nix/sparql.html', {
        'error_message': error_message,
        'query': query,
        'experiment_id': id,
        'query_result': query_result
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
