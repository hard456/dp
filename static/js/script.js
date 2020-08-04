// verifies the size of the files to submit, displays the spinner, and submits the form
function submitUploadExperiment() {
        upload = document.getElementById('files');
        size = 0;
        for (i = 0; i < upload.files.length; i++) {
                size += upload.files[i].size;
        }
        if(size > 2147483648){
                alert("Total size exceeded 2 GiB.")
        }
        else{
           $('#spinner').css({'display': 'block'});
           $('#uploadExperimentButton').prop('disabled', true);
           $("#uploadExperimentForm").submit();
        }

}

// displays the spinner and submits the form
function submitFindMetadata() {
        $('#spinner').css({'display': 'block'});
        $('#findMetadataButton').prop('disabled', true);
        $("#findMetadataForm").submit();
}

// displays the spinner and submits the form
function submitShowMetadata() {
        $('#spinner').css({'display': 'block'});
        $('#showMetadataButton').prop('disabled', true);
        $("#showMetadataForm").submit();
}

// verifies the size of the files to submit, displays the spinner, and submits the form
function submitUploadFiles() {
        upload = document.getElementById('files');
        size = 0;
        for (i = 0; i < upload.files.length; i++) {
                size += upload.files[i].size;
        }
        if(size > 2147483648){
                alert("Total size exceeded 2 GiB.")
        }
        else {
                $('#spinner').css({'display': 'block'});
                $('#uploadFilesButton').prop('disabled', true);
                $("#uploadFilesForm").submit();
        }
}

//displays the modal window
function showModalWindow() {
        $('#spinnerModal').modal('show');
}