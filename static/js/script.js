function submitUploadExperiment() {
        upload = document.getElementById('files');
        size = 0;
        for (i = 0; i < upload.files.length; i++) {
                size += upload.files[i].size;
        }
        if(size > 2147483648){
                alert("Size of files is: " + size + "\nThe maximum size allowed is: 2147483648")
        }
        else{
           $('#spinner').css({'display': 'block'});
           $('#uploadExperimentButton').prop('disabled', true);
           $("#uploadExperimentForm").submit();
        }

}

function submitFindMetadata() {
        $('#spinner').css({'display': 'block'});
        $('#findMetadataButton').prop('disabled', true);
        $("#findMetadataForm").submit();
}

function submitShowMetadata() {
        $('#spinner').css({'display': 'block'});
        $('#showMetadataButton').prop('disabled', true);
        $("#showMetadataForm").submit();
}

function submitUploadFiles() {
        $('#spinner').css({'display': 'block'});
        $('#uploadFilesButton').prop('disabled', true);
        $("#uploadFilesForm").submit();
}

function showModalWindow() {
        $('#spinnerModal').modal('show');
}