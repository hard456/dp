import os

import nixio as nix
import uuid
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.conf import settings


def index(request):
    return render(request, 'nix/index.html')


def show_file(request, id):
    return render(request, 'nix/file.html', {
        'error_message': id
    })


def upload_experiment(request):
    if request.method == 'POST' and request.FILES.get('myfile', False):
        file = request.FILES['myfile']
        file_name = file.name.lower()

        # check file extension
        if not file_name.endswith('.nix') and not file_name.endswith('.h5'):
            return render(request, 'nix/index.html', {
                'error_message': "The file can only have a .nix or .h5 extension."
            })

        fs = FileSystemStorage()

        # check unique experiment id
        while True:
            experiment_id = str(uuid.uuid1().int)
            print(settings.MEDIA_URL + 'experiments/' + '34990128788807444172295489484962121020' + '/')
            if not fs.exists('experiments/' + experiment_id + '/'):
                break

        fs.save('experiments/' + experiment_id + '/' + file_name, file)
        return redirect('/experiment/' + experiment_id + '/file')
    return render(request, 'nix/index.html', {
        'error_message': "No file was selected or the post method was not selected."
    })


def testik(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, '../media/experiments/test3.nix')
    nix_file = nix.File.open(file_path, nix.FileMode.ReadOnly)

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
