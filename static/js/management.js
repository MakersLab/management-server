ajaxCallback = function (data) {

    data = JSON.parse(data);
    if (data['successful']) {
        alert('All data are backed up.');
    }
    else {
        alert('Unable to back up. Chceck logs on server.');
    }
};

function backup() {
    $.ajax({
        type: 'POST',
        url: '/management/backup',
        success: ajaxCallback,
        data: {backup: true}
    });
}
