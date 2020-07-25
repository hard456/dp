function submitUploadExperiment() {
        $('#spinner').css({'display': 'block'});
        $('#uploadExperimentButton').prop('disabled', true);
        $("#uploadExperimentForm").submit();
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