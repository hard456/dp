import os

import nixio as nix
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'nix/index.html')


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
    #     return render(request, 'core/simple_upload.html', {
    #         'uploaded_file_url': uploaded_file_url
    #     })
    # return render(request, 'core/simple_upload.html')
        return render(request, 'nix/test.html')


def testik(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, '../experiments/file_create_example.h5')
    nix_file = nix.File.open(file_path, nix.FileMode.ReadOnly)

    print(nix_file.format, nix_file.version, nix_file.created_at)
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
