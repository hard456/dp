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
