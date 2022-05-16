function serverCtrl(url) {
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        complete: function (data) {
            let waitModal = bootstrap.Modal.getInstance(document.getElementById('waitModal'))
            console.log(data.responseJSON)
            setTimeout(function () {
                waitModal.hide()
            }, 1000);
        }
    });
}
