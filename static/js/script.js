function submitUploadExperiment() {
        $('#spinner').css({'display': 'block'});
        $('#experimentUploadButton').prop('disabled', true);
        $("#uploadExperimentForm").submit();
}

function submitQuery() {
        $('#spinner').css({'display': 'block'});
        $('#queryButton').prop('disabled', true);
        $("#queryForm").submit();
}

function submitConvertMetadata() {
        $('#spinner').css({'display': 'block'});
        $('#convertMetadataButton').prop('disabled', true);
        $("#convertMetadataForm").submit();
}
