function submitUploadExperiment() {
        $('#spinner').css({'display': 'block'});
        $('#experimentUploadButton').prop('disabled', true);
        $("#uploadFileForm").submit();
    }
